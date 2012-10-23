from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # Examples:

    # url(r'^$', 'trainingme.views.home', name='home'),
    url(r'^course/new/$','elearning.views.new_course', name='new_course' ),
    url(r'^course/edit/(\d+)/$','elearning.views.edit_course', name='edit_course' ),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
)

