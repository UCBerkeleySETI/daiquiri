import logging
import os

from collections import OrderedDict

from celery.app.control import Control

from django.conf import settings
from django.contrib.auth.models import Group
from django.db import models
from django.db.utils import OperationalError, ProgrammingError, InternalError, DataError
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now

from rest_framework.exceptions import ValidationError

from jsonfield import JSONField

from daiquiri.core.adapter import DatabaseAdapter, DownloadAdapter
from daiquiri.core.constants import ACCESS_LEVEL_CHOICES
from daiquiri.core.generators import generate_votable
from daiquiri.jobs.models import Job
from daiquiri.jobs.managers import JobManager
from daiquiri.jobs.exceptions import JobError
from daiquiri.files.utils import check_file
from daiquiri.stats.models import Record

from .managers import QueryJobManager, ExampleManager
from .utils import (
    get_format_config,
    get_job_sources,
    get_job_columns
)
from .process import (
    check_quota,
    check_number_of_active_jobs,
    process_schema_name,
    process_table_name,
    process_query_language,
    process_queue,
    process_response_format,
    translate_query,
    process_query,
    process_display_columns,
    check_permissions,
)
from .tasks import (
    run_query,
    run_ingest,
    create_download_file,
    create_archive_file,
    rename_table,
    drop_table,
    abort_query
)

logger = logging.getLogger(__name__)
query_logger = logging.getLogger('query')


class QueryJob(Job):

    objects = QueryJobManager()

    schema_name = models.CharField(max_length=256)
    table_name = models.CharField(max_length=256)
    queue = models.CharField(max_length=16, blank=True)

    query_language = models.CharField(max_length=16, blank=True)
    query = models.TextField(blank=True)
    native_query = models.TextField(blank=True)
    actual_query = models.TextField(blank=True)

    queue = models.CharField(max_length=16, blank=True)
    nrows = models.BigIntegerField(null=True, blank=True)
    size = models.BigIntegerField(null=True, blank=True)

    metadata = JSONField(null=True, blank=True)
    uploads = JSONField(null=True, blank=True)

    pid = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ('start_time', )

        verbose_name = _('QueryJob')
        verbose_name_plural = _('QueryJobs')

    @property
    def parameters(self):
        return {
            'schema_name': self.schema_name,
            'table_name': self.table_name,
            'query_language': self.query_language,
            'query': self.query,
            'native_query': self.native_query,
            'actual_query': self.actual_query,
            'queue': self.queue,
            'nrows': self.nrows,
            'size': self.size
        }

    @property
    def formats(self):
        return OrderedDict((item['key'], item['content_type']) for item in settings.QUERY_DOWNLOAD_FORMATS)

    @property
    def result_status(self):
        return 'OK' if self.max_records is None else 'OVERFLOW'

    @property
    def quote(self):
        return None

    @property
    def time_queue(self):
        if self.start_time and self.creation_time:
            return (self.start_time - self.creation_time).total_seconds()
        else:
            return None

    @property
    def time_query(self):
        if self.end_time and self.start_time:
            return (self.end_time - self.start_time).total_seconds()
        else:
            return None

    @property
    def timeout(self):
        if self.queue:
            return next((queue['timeout'] for queue in settings.QUERY_QUEUES if queue['key'] == self.queue))
        else:
            return 10

    @property
    def priority(self):
        return next((queue['priority'] for queue in settings.QUERY_QUEUES if queue['key'] == self.queue))

    @cached_property
    def column_names(self):
        return [column['name'] for column in self.metadata['columns']]

    def process(self, upload=False):
        # log the query to the query log
        query_logger.info('"%s" %s %s', self.query, self.query_language, self.owner or 'anonymous')

        # check quota and number of active jobs
        check_quota(self)
        check_number_of_active_jobs(self)

        # process schema_name, table_name and response format
        self.schema_name = process_schema_name(self.owner, self.schema_name)
        self.table_name = process_table_name(self.table_name)
        self.response_format = process_response_format(self.response_format)

        if upload:
            self.query = ''
            self.query_language = ''
            self.queue = ''
            self.execution_duration = 0.0

        else:
            self.query_language = process_query_language(self.owner, self.query_language)
            self.queue = process_queue(self.owner, self.queue)
            self.response_format = process_response_format(self.response_format)

            # set the execution_duration to the queues timeout
            self.execution_duration = self.timeout

            # log the input query to the debug log
            logger.debug('query = "%s"', self.query)

            # translate the query from adql
            translated_query = translate_query(self.query_language, self.query)

            # log the translated query to the debug log
            logger.debug('translated_query = "%s"', translated_query)

            processor = process_query(translated_query)

            # log the processor output to the debug log
            logger.debug('native_query = "%s"', processor.query)
            logger.debug('processor.keywords = %s', processor.keywords)
            logger.debug('processor.tables = %s', processor.tables)
            logger.debug('processor.columns = %s', processor.columns)
            logger.debug('processor.functions = %s', processor.functions)

            # check permissions
            permission_messages = check_permissions(
                self.owner,
                processor.keywords,
                processor.tables,
                processor.columns,
                processor.functions
            )
            if permission_messages:
                raise ValidationError({
                    'query': permission_messages
                })

            # initialize metadata and store map of aliases
            self.metadata = {
                'display_columns': process_display_columns(processor.display_columns),
                'tables': processor.tables
            }

            # get the native query from the processor (without trailing semicolon)
            self.native_query = processor.query.rstrip(';')

            # set clean flag
            self.is_clean = True

    def run(self):
        if not self.is_clean:
            raise Exception('job.process() was not called.')

        if self.phase == self.PHASE_PENDING:
            self.phase = self.PHASE_QUEUED
            self.save()

            # start the submit_query task in a syncronous or asuncronous way
            job_id = str(self.id)
            if not settings.ASYNC:
                logger.info('job %s submitted (sync)' % self.id)
                run_query.apply((job_id, ), task_id=job_id, throw=True)

            else:
                logger.info('job %s submitted (async, queue=query, priority=%s)' % (self.id, self.priority))
                run_query.apply_async((job_id, ), task_id=job_id, queue='query', priority=self.priority)

        else:
            raise ValidationError({
                'phase': ['Job is not PENDING.']
            })

    def run_sync(self):
        adapter = DatabaseAdapter()

        self.actual_query = adapter.build_sync_query(
            self.native_query,
            settings.QUERY_SYNC_TIMEOUT,
            self.max_records
        )

        job_sources = get_job_sources(self)

        # create a stats record for this job
        Record.objects.create(
            time=now(),
            resource_type='QUERY',
            resource={
                'job_id': None,
                'job_type': self.job_type,
                'query': self.query,
                'query_language': self.query_language,
                'sources': job_sources
            },
            client_ip=self.client_ip,
            user=self.owner
        )

        try:
            download_adapter = DownloadAdapter()

            yield from generate_votable(adapter.fetchall(self.actual_query), get_job_columns(self),
                                        table=download_adapter.get_table_name(self.schema_name, self.table_name),
                                        infos=download_adapter.get_infos('OK', self.query, self.query_language, job_sources),
                                        links=download_adapter.get_links(job_sources))
            self.drop_uploads()

        except (OperationalError, ProgrammingError, InternalError, DataError) as e:
            raise StopIteration()

    def ingest(self, file_path):
        if self.phase == self.PHASE_PENDING:
            self.phase = self.PHASE_QUEUED
            self.save()

            if not settings.ASYNC:
                run_ingest.apply((self.id, file_path), throw=True)
            else:
                run_ingest.apply_async((self.id, file_path), queue='download')

        else:
            raise ValidationError({
                'phase': ['Job is not PENDING.']
            })

    def abort(self):
        if settings.ASYNC:
            # first, revoke the task in celery, regardless the phase
            Control().revoke(str(self.id))

        current_phase = self.phase

        if current_phase in self.PHASE_ACTIVE:
            # next, set the phase to ABORTED
            self.phase = self.PHASE_ABORTED
            self.save()

            # finally, abort query, this will trigger OperationalError in the run_query task
            if current_phase == self.PHASE_EXECUTING:
                self.abort_query()

    def archive(self):
        self.abort()
        self.drop_table()
        self.drop_uploads()
        self.phase = self.PHASE_ARCHIVED
        self.nrows = None
        self.size = None
        self.save()

    def rename_table(self, new_table_name):
        if self.table_name != new_table_name:
            self.metadata['name'] = new_table_name
            self.save()

            task_args = (self.schema_name, self.table_name, new_table_name)

            if not settings.ASYNC:
                rename_table.apply(task_args, throw=True)
            else:
                rename_table.apply_async(task_args)

    def drop_table(self):
        task_args = (self.schema_name, self.table_name)

        if not settings.ASYNC:
            drop_table.apply(task_args, throw=True)
        else:
            drop_table.apply_async(task_args)

    def drop_uploads(self):
        if self.uploads:
            for table_name, file_path in self.uploads.items():
                task_args = (settings.TAP_UPLOAD, table_name)

                if not settings.ASYNC:
                    drop_table.apply(task_args, throw=True)
                else:
                    drop_table.apply_async(task_args)

    def abort_query(self):
        task_args = (self.pid, )

        if not settings.ASYNC:
            abort_query.apply(task_args, throw=True)
        else:
            abort_query.apply_async(task_args)

    def stream(self, format_key):
        if self.phase == self.PHASE_COMPLETED:
            return DownloadAdapter().generate(
                format_key,
                self.metadata.get('columns', []),
                sources=self.metadata.get('sources', []),
                schema_name=self.schema_name,
                table_name=self.table_name,
                nrows=self.nrows,
                query_status=self.result_status,
                query=self.query,
                query_language=self.query_language
            )
        else:
            raise ValidationError({
                'phase': ['Job is not COMPLETED.']
            })

    def rows(self, column_names, ordering, page, page_size, search, filters):
        if self.phase == self.PHASE_COMPLETED:
            # check if the columns are actually in the jobs table
            errors = {}

            for column_name in column_names:
                if column_name not in self.column_names:
                    errors[column_name] = _('Column not found.')

            if errors:
                raise ValidationError(errors)

            # get database adapter
            adapter = DatabaseAdapter()

            try:
                # query the database for the total number of rows
                count = adapter.count_rows(self.schema_name, self.table_name, column_names, search, filters)

                # query the paginated rowset
                rows = adapter.fetch_rows(self.schema_name, self.table_name, column_names, ordering, page, page_size, search, filters)

                # flatten the list if only one column is retrieved
                if len(column_names) == 1:
                    return count, [element for row in rows for element in row]
                else:
                    return count, rows

            except ProgrammingError:
                return 0, []

        else:
            raise ValidationError({
                'phase': ['Job is not COMPLETED.']
            })

    def columns(self):
        if self.metadata:
            return self.metadata.get('columns', [])
        else:
            return []


class DownloadJob(Job):

    objects = JobManager()

    job = models.ForeignKey(
        QueryJob, related_name='downloads', on_delete=models.CASCADE,
        verbose_name=_('QueryJob'),
        help_text=_('QueryJob this DownloadJob belongs to.')
    )
    format_key = models.CharField(
        max_length=32,
        verbose_name=_('Format key'),
        help_text=_('Format key for this download.')
    )

    class Meta:
        ordering = ('start_time', )

        verbose_name = _('DownloadJob')
        verbose_name_plural = _('DownloadJobs')

    @property
    def file_path(self):
        if not self.owner:
            username = 'anonymous'
        else:
            username = self.owner.username

        format_config = get_format_config(self.format_key)

        if format_config:
            directory_name = os.path.join(settings.QUERY_DOWNLOAD_DIR, username)
            return os.path.join(directory_name, '%s.%s' % (self.job.table_name, format_config['extension']))
        else:
            return None

    def process(self):
        if self.job.phase == self.PHASE_COMPLETED:
            self.owner = self.job.owner
        else:
            raise ValidationError({
                'phase': ['Job is not COMPLETED.']
            })

        # set clean flag
        self.is_clean = True

    def run(self):
        if not self.is_clean:
            raise Exception('download_job.process() was not called.')

        if self.phase == self.PHASE_PENDING:
            self.phase = self.PHASE_QUEUED
            self.save()

            download_id = str(self.id)
            if not settings.ASYNC:
                logger.info('download_job %s submitted (sync)' % download_id)
                create_download_file.apply((download_id, ), task_id=download_id, throw=True)

            else:
                logger.info('download_job %s submitted (async, queue=download)' % download_id)
                create_download_file.apply_async((download_id, ), task_id=download_id, queue='download')

        else:
            raise ValidationError({
                'phase': ['Job is not PENDING.']
            })

    def delete_file(self):
        try:
            if self.file_path is not None:
                os.remove(self.file_path)
        except OSError:
            pass


class QueryArchiveJob(Job):

    objects = JobManager()

    job = models.ForeignKey(
        QueryJob, related_name='archives', on_delete=models.CASCADE,
        verbose_name=_('QueryJob'),
        help_text=_('QueryJob this ArchiveJob belongs to.')
    )
    column_name = models.CharField(
        max_length=32,
        verbose_name=_('Column name'),
        help_text=_('Column name for this download.')
    )
    files = JSONField(
        verbose_name=_('Files'),
        help_text=_('List of files in the archive.')
    )

    class Meta:
        ordering = ('start_time', )

        verbose_name = _('QueryArchiveJob')
        verbose_name_plural = _('QueryArchiveJob')

    @property
    def file_path(self):
        if not self.owner:
            username = 'anonymous'
        else:
            username = self.owner.username

        directory_name = os.path.join(settings.QUERY_DOWNLOAD_DIR, username)
        return os.path.join(directory_name, '%s.%s.zip' % (self.job.table_name, self.column_name))

    def process(self):
        if self.job.phase == self.PHASE_COMPLETED:
            self.owner = self.job.owner
        else:
            raise ValidationError({
                'phase': ['Job is not COMPLETED.']
            })

        if not self.column_name:
            raise ValidationError({
                'column_name': [_('This field may not be blank.')]
            })

        if self.column_name not in self.job.column_names:
            raise ValidationError({
                'column_name': [_('Unknown column "%s".') % self.column_name]
            })

        # get database adapter and query the paginated rowset
        rows = DatabaseAdapter().fetch_rows(self.job.schema_name, self.job.table_name, [self.column_name], page_size=0)

        # prepare list of files for this job
        files = []
        for row in rows:
            file_path = row[0]

            # append the file to the list of files  if it exists
            if file_path and check_file(self.owner, file_path):
                files.append(file_path)
            else:
                raise ValidationError({
                    'files': [_('One or more of the files cannot be found.')]
                })

        # set files for this job
        self.files = files

        # set clean flag
        self.is_clean = True

    def run(self):
        if not self.is_clean:
            raise Exception('download_job.process() was not called.')

        if self.phase == self.PHASE_PENDING:
            self.phase = self.PHASE_QUEUED
            self.save()

            archive_id = str(self.id)
            if not settings.ASYNC:
                logger.info('archive_job %s submitted (sync)' % archive_id)
                create_archive_file.apply((archive_id, ), task_id=archive_id, throw=True)

            else:
                logger.info('archive_job %s submitted (async, queue=download)' % archive_id)
                create_archive_file.apply_async((archive_id, ), task_id=archive_id, queue='download')

        else:
            raise ValidationError({
                'phase': ['Job is not PENDING.']
            })

    def delete_file(self):
        try:
            os.remove(self.file_path)
        except OSError:
            pass


class Example(models.Model):

    objects = ExampleManager()

    order = models.IntegerField(
        null=True, blank=True,
        verbose_name=_('Order'),
        help_text=_('Position in lists.')
    )
    name = models.CharField(
        max_length=256,
        verbose_name=_('Name'),
        help_text=_('Identifier of the example.')
    )
    description = models.TextField(
        null=True, blank=True,
        verbose_name=_('Description'),
        help_text=_('A brief description of the example to be displayed in the user interface.')
    )
    query_language = models.CharField(
        max_length=16,
        verbose_name=_('Query language'),
        help_text=_('The query language for this example.')
    )
    query_string = models.TextField(
        verbose_name=_('Query string'),
        help_text=_('The query string (SQL) for this example.')
    )
    access_level = models.CharField(
        max_length=8, choices=ACCESS_LEVEL_CHOICES,
        verbose_name=_('Access level')
    )
    groups = models.ManyToManyField(
        Group, blank=True,
        verbose_name=_('Groups'),
        help_text=_('The groups which have access to the examples.')
    )

    class Meta:
        ordering = ('order',)

        verbose_name = _('Example')
        verbose_name_plural = _('Examples')

    def __str__(self):
        return self.name
