from django.conf import settings

from daiquiri.core.utils import import_class


def ConeSearchAdapter():
    return import_class(settings.CONESEARCH_ADAPTER)()


class BaseConeSearchAdapter(object):

    def clean(self, request, resource):
        raise NotImplementedError()

    def stream(self):
        raise NotImplementedError()
