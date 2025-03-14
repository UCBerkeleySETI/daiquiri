import daiquiri.core.env as env

QUERY_DOWNLOAD_DIR = env.get_abspath('QUERY_DOWNLOAD_DIR')
QUERY_UPLOAD_DIR = env.get_abspath('QUERY_UPLOAD_DIR')

QUERY_ANONYMOUS = False
QUERY_USER_SCHEMA_PREFIX = 'daiquiri_user_'
QUERY_QUOTA = {
    'anonymous': '100Mb',
    'user': '10000Mb',
    'users': {},
    'groups': {}
}
QUERY_SYNC_TIMEOUT = 5
QUERY_MAX_ACTIVE_JOBS = {
    'anonymous': '1'
}
QUERY_QUEUES = [
    {
        'key': 'default',
        'label': 'Default',
        'timeout': 10,
        'priority': 1,
        'access_level': 'PUBLIC',
        'groups': []
    }
]
QUERY_LANGUAGES = [
    {
        'key': 'adql',
        'version': 2.0,
        'label': 'ADQL',
        'description': '',
        'quote_char': '"'
    }
]
QUERY_DROPDOWNS = [
    {
        'key': 'simbad',
        'service': 'query/js/dropdowns/simbad.js',
        'template': 'query/query_dropdown_simbad.html',
        'options': {
            'url': 'http://simbad.u-strasbg.fr/simbad/sim-id'
        }
    },
    {
        'key': 'vizier',
        'service': 'query/js/dropdowns/vizier.js',
        'template': 'query/query_dropdown_vizier.html',
        'options': {
            'url': 'http://vizier.u-strasbg.fr/viz-bin/votable',
            'catalogs': ['I/322A', 'I/259']
        }
    }
]
QUERY_DEFAULT_DOWNLOAD_FORMAT = 'votable'
QUERY_DOWNLOAD_FORMATS = [
    {
        'key': 'votable',
        'extension': 'xml',
        'content_type': 'application/xml',
        'label': 'IVOA VOTable XML file - TABLEDATA serialization',
        'help': 'A XML file using the IVOA VOTable format. Use this option if you intend to use VO compatible software to further process the data.'
    },
    {
        'key': 'csv',
        'extension': 'csv',
        'content_type': 'text/csv',
        'label': 'Comma separated Values',
        'help': 'A text file with a line for each row of the table. The fields are delimited by a comma and quoted by double quotes. Use this option for a later import into a spreadsheed application or a custom script. Use this option if you are unsure what to use.'
    },
    {
        'key': 'fits',
        'extension': 'fits',
        'content_type': 'application/fits',
        'label': 'FITS',
        'help': 'Flexible Image Transport System (FITS) file format.'
    }
]
QUERY_UPLOAD = True
QUERY_UPLOAD_LIMIT = {
    'anonymous': '10Mb',
    'user': '100Mb',
    'users': {},
    'groups': {}
}
QUERY_PROCESSOR_CACHE = True
