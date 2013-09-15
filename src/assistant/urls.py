from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', 'assistant.views.home', name="assistant-home"),
    url(r'^test/add$', 'assistant.views.test_edit', {'pk': None}, name="test-add"),
    url(r'^test/edit/(?P<pk>\d+)$', 'assistant.views.test_edit', name="test-edit"),
    url(r'^test/detail/(\d+)$', 'assistant.views.test_detail', name="test-detail"),
    url(r'^test/delete/(\d+)$', 'assistant.views.test_delete', name="test-delete"),
    url(r'^test/filter$', 'assistant.views.test_filter', name="test-filter"),
    url(r'^run/add$', 'assistant.views.run_edit', {'pk': None}, name="run-add"),
    url(r'^run/detail/(\d+)$', 'assistant.views.run_detail', name="run-detail"),
    url(r'^run/list/$', 'assistant.views.run_list', name="run-list"),
    url(r'^run/detail/(\d+)/running$', 'assistant.views.run_run', name='run-running'),
    url(r'^run/stats', 'assistant.views.stats', name='run-stats'),
    url(r'^search/', include('haystack.urls')),

)
