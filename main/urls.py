from django.conf.urls import patterns, include, url

urlpatterns = patterns('main.views',
    url(r'^$', 'index', name='index'),
    url(r'^(?P<reference>\d+)/$', 'detail', name='detail'),
    url(r'^(?P<reference>\d+)/edit/$', 'edit', name='detail_edit'),
)
