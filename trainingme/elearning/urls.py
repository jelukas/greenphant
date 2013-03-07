from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^course/new/$','elearning.views.new_course', name='new_course' ),
    url(r'^course/edit/(\d+)/$','elearning.views.edit_course', name='edit_course' ),
    url(r'^course/build/(\d+)/$','elearning.views.building_course', name='building_course' ),
    url(r'^course/send-to-checking-process/(\d+)/$','elearning.views.change_checking_status', name='change_checking_status' ),
    #Subjects
    url(r'^course/subject/add/(\d+)/$','elearning.views.add_subject', name='add_subject' ),
    url(r'^course/subject/edit/(\d+)/$','elearning.views.edit_subject', name='edit_subject' ),
    url(r'^course/subject/delete/(\d+)/$','elearning.views.delete_subject', name='delete_subject' ),
    url(r'^course/subject/up/(\d+)/$','elearning.views.up_order_subject', name='up_order_subject' ),
    url(r'^course/subject/down/(\d+)/$','elearning.views.down_order_subject', name='down_order_subject' ),
    #Lessons
    url(r'^course/lesson/add/(\d+)/$','elearning.views.add_lesson', name='add_lesson' ),
    url(r'^course/lesson/edit/(\d+)/$','elearning.views.edit_lesson', name='edit_lesson' ),
    url(r'^course/lesson/delete/(\d+)/$','elearning.views.delete_lesson', name='delete_lesson' ),
    #Video
    url(r'^course/video/add/(\d+)/$','elearning.views.add_video', name='add_video' ),
    url(r'^course/video/free/(\d+)/$','elearning.views.free_video', name='free_video' ),
    url(r'^course/video/delete/(\d+)/$','elearning.views.delete_video', name='delete_video' ),
    #Attach
    url(r'^course/attach/add/(\d+)/$','elearning.views.add_attach', name='add_attach' ),
    #url(r'^course/attach/edit/(\d+)/$','elearning.views.edit_attach', name='edit_attach' ),
    url(r'^course/attach/delete/(\d+)/$','elearning.views.delete_attach', name='delete_attach' ),

    #Dashboard
    url(r'^$','elearning.views.dashboard', name='dashboard_home' ),
    url(r'^dashboard/$','elearning.views.dashboard', name='dashboard' ),
    url(r'^dashboard/learning/$','elearning.views.learning', name='learning' ),
    url(r'^dashboard/teaching/$','elearning.views.teaching', name='teaching' ),

    #Course

    url(r'^course/learning/(\d+)/$','elearning.views.learning_course', name='learning_course' ),
    url(r'^course/(?P<slug>[-\w]+)/$','elearning.views.view_course', name='view_course' ),
    url(r'^course/(\d+)/(\d+)?$','elearning.views.vote_course', name='vote_course' ),
    url(r'^course/enrroll-tester/(\d+)/$','elearning.views.enrroll_tester', name='enrroll_tester'),

    #url(r'^course/(\d+)/$','elearning.views.view_course', name='view_course' ),

    #Lesson
    url(r'^lesson/(\d+)/(\d+)?$','elearning.views.vote_lesson', name='vote_lesson' ),
    url(r'^course/lesson/learning/(\d+)/$','elearning.views.learning_lesson', name='learning_lesson' ),
    url(r'^course/lesson/preview/(\d+)/$','elearning.views.preview_lesson', name='preview_lesson' ),
    #Comment
    url(r'^course/lesson/reply/(\d+)/(\d+)/$','elearning.views.reply_comment', name='reply_comment' ),

)

