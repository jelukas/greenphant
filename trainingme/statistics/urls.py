from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^interests/$','statistics.views.interest_form', name='interest_form' ),

)

