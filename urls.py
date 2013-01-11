from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
	url(r'^$', direct_to_template, {'template': 'index.html'}),
	(r'^public/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'public'}),
	url(r'^api/get_trends/$', 'views.get_trends'),
)
