from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$','elearning.views.home', name='home'),
    url(r'', include('social_auth.urls')),
    url(r'^personal/', include('personal.urls')),
    url(r'^elearning/', include('elearning.urls')),
    url(r'^financial/', include('financial.urls')),


    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    #For Paypal
    (r'^paypal/paymeny/23pok420osijos/danoentrain/', include('paypal.standard.ipn.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
