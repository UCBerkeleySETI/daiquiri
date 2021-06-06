from allauth.account.apps import AccountConfig
from allauth.socialaccount.apps import SocialAccountConfig

# See https://github.com/pennersr/django-allauth/issues/2826

class ModifiedAccountConfig(AccountConfig):
    default_auto_field = 'django.db.models.AutoField'

class ModifiedSocialAccountConfig(SocialAccountConfig):
    default_auto_field = 'django.db.models.AutoField'

