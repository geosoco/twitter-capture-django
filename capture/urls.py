from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
	# Examples:
	# url(r'^$', 'capture.views.home', name='home'),
	# url(r'^blog/', include('blog.urls')),
	#url(r'^$', 'main.views.test', name='test'),

	url(r'', include('main.urls')),
	url(r'^worker/', include('worker.urls')),
	url(r'^accounts/', include('django.contrib.auth.urls')),
	url(r'^api/', include('api_auth.urls')),
	url(r'^admin/', include(admin.site.urls)),
)
