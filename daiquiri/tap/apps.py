from django.apps import AppConfig


class TapConfig(AppConfig):
    name = 'daiquiri.tap'
    label = 'daiquiri_tap'
    verbose_name = 'Tap'
    default_auto_field = 'django.db.models.AutoField'

    def ready(self):
        from . import handlers
