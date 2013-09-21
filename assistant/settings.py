import os
from django.conf import settings

WHOOSH_PATH = getattr(settings, "TEST_ASSISTANT_WHOOSH_PATH", '.')

INSTALLED_APPS = settings.INSTALLED_APPS + (
    'concurrent_server',

    'taggit',
    'taggit_machinetags',
    'django_nvd3',
    'haystack',

    'assistant',
)

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(WHOOSH_PATH, 'whoosh_index'),
    },
}

SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
