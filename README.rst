tests-assistant
===============

:lisence: agplv3+
:django: 1.5


Install
-------

Setting up test assistant for your project is so easy.
It's just 3 step process. 

Install django-tests-assistant from pypi

``pip install django-tests-assistant``

Edit settings.py of your project and add:

``from assistant.settings import *``

Edit your urls.py and add followingi in your urlpatterns:

``url(r'^', include('assistant.urls')),``

That is it & enjoy :) 
Oh, don't forget to do a ``python manage.py syncdb``
