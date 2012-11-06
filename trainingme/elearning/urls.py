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
    url(r'^course/video/add/(\d+)/$','elearning.views.add_video', name='add_video' ),
    #url(r'^course/video/edit/(\d+)/$','elearning.views.edit_video', name='edit_video' ),
    url(r'^course/video/delete/(\d+)/$','elearning.views.delete_video', name='delete_video' ),
    url(r'^course/attach/add/(\d+)/$','elearning.views.add_attach', name='add_attach' ),
    #url(r'^course/attach/edit/(\d+)/$','elearning.views.edit_attach', name='edit_attach' ),
    url(r'^course/attach/delete/(\d+)/$','elearning.views.delete_attach', name='delete_attach' ),
    url(r'^course/video/test/(\d+)/$','elearning.views.test_video', name='test_video' ),

    #Dashboard
    url(r'^dashboard/$','elearning.views.dashboard', name='dashboard' ),
    url(r'^dashboard/learning/$','elearning.views.learning', name='learning' ),
    url(r'^dashboard/teaching/$','elearning.views.teaching', name='teaching' ),

    #Testing Paypal
    url(r'^paypal/$','elearning.views.paypal', name='paypal' ),
)

