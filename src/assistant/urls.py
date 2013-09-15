from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'assistant.views.home'),
    url(r'^test/add$', 'assistant.views.test_edit', {'pk': None}),
    url(r'^test/edit/(?P<pk>\d+)$', 'assistant.views.test_edit'),
    url(r'^test/detail/(\d+)$', 'assistant.views.test_detail'),
    url(r'^test/delete/(\d+)$', 'assistant.views.test_delete'),
    url(r'^test/filter$', 'assistant.views.test_filter'),
    url(r'^run/add$', 'assistant.views.run_edit', {'pk': None}),
    url(r'^run/detail/(\d+)$', 'assistant.views.run_detail'),
    url(r'^run/list/$', 'assistant.views.run_list'),
    url(r'^run/detail/(\d+)/running$', 'assistant.views.run_run'),
    url(r'^run/stats', 'assistant.views.stats'),
    url(r'^search/', include('haystack.urls')),

)
