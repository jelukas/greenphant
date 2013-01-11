from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^profile/edit/','personal.views.edit', name='edit_profile' ),
    url(r'^profile/','personal.views.view_profile', name='view_profile' ),
    url(r'^logout/','personal.views.logout_view', name='logout' ),
)

