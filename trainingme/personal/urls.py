from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^profile/edit/','personal.views.edit', name='edit_profile' ),
    url(r'^profile/','personal.views.view_profile', name='view_profile' ),
    url(r'^update_email/$','personal.views.update_email_form', name='update_email_form' ),
    url(r'^messages/list/$','personal.views.list_messages', name='list_messages' ),
    url(r'^messages/conversation/(\d+)/(\d+)?$','personal.views.view_conversation', name='view_conversation' ),
    url(r'^logout/','personal.views.logout_view', name='logout' ),
)

