from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^course/new/$','elearning.views.new_course', name='new_course' ),
    url(r'^course/edit/(\d+)/$','elearning.views.edit_course', name='edit_course' ),
    url(r'^course/build/(\d+)/$','elearning.views.building_course', name='building_course' ),
    url(r'^course/subject/add/(\d+)/$','elearning.views.add_subject', name='add_subject' ),
    url(r'^course/subject/edit/(\d+)/$','elearning.views.edit_subject', name='edit_subject' ),
    url(r'^course/subject/delete/(\d+)/$','elearning.views.delete_subject', name='delete_subject' ),
    url(r'^course/lesson/add/(\d+)/$','elearning.views.add_lesson', name='add_lesson' ),
    url(r'^course/lesson/edit/(\d+)/$','elearning.views.edit_lesson', name='edit_lesson' ),
    url(r'^course/lesson/delete/(\d+)/$','elearning.views.delete_lesson', name='delete_lesson' ),

)

