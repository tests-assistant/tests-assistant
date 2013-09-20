import os

TEST_ASSISTANT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

INSTALLED_APPS += (
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
        'PATH': os.path.join(TEST_ASSISTANT_ROOT, 'whoosh_index'),
    },
}

SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
