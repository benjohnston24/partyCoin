from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^funds_tracker/', include('funds_tracker.urls',
        namespace='funds'),
        )
)
