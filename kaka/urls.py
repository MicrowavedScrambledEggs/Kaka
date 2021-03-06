from django.conf.urls import patterns, include, url

from django.conf import settings

from django.contrib import admin
admin.autodiscover()


urlpatterns = [
    # Examples:
    # url(r'^$', 'kaka.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^inplaceeditform/', include('inplaceeditform.urls')),
    url(r'^api/genotype/$', 'web.views.genotype_report', name='genotype_report'),
    url(r'^api/(?P<report>[0-9a-zA-Z_]*)/$', 'web.views.page_report' ),
    url(r'^api/(?P<report>[0-9a-zA-Z_]*)/(?P<fmt>[a-z]*)/$', 'web.views.page_report'),
    url(r'^api/(?P<report>[0-9a-zA-Z_]*)/(?P<fmt>[a-z]*)/(?P<conf>.*)$', 'web.views.page_report'),
    url(r'^experimentsearch/', include('experimentsearch.urls', namespace='experimentsearch')),
]

if settings.DEBUG and False:
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )


