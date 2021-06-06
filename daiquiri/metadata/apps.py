from django.apps import AppConfig


class MetadataConfig(AppConfig):
    name = 'daiquiri.metadata'
    label = 'daiquiri_metadata'
    verbose_name = 'Metadata'
    default_auto_field = 'django.db.models.AutoField'

    def ready(self):
        from . import handlers
