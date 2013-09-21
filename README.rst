tests-assistant
===============

:lisence: agplv3+
:django: 1.5
:pypi: https://pypi.python.org/pypi/django-tests-assistant


Install
-------

Setting up test assistant for your project is so easy.
It's just 3 step process. 

Install django-tests-assistant from pypi::

  pip install django-tests-assistant

Give path to the search indexes::

  TEST_ASSISTANT_WHOOSH_PATH = "/path/to/whoosh/index/directory"

Edit settings.py of your project and add following at the end::

  from assistant.settings import *

Edit your urls.py and add a url mapping in your urlpatterns::

  url(r'tests/', include('assistant.urls')),

That is it & enjoy :) 

Oh, don't forget to do a ``python manage.py syncdb``
