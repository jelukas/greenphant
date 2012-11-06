from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$','financial.views.view_billing', name='view_billing' ),
    url(r'^edit/$','financial.views.edit_billing', name='edit_billing' ),
)

