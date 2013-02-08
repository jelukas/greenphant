from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$','elearning.views.home', name='home'),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'', include('social_auth.urls')),
    url(r'^personal/', include('personal.urls')),
    url(r'^elearning/', include('elearning.urls')),
    url(r'^financial/', include('financial.urls')),


    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    #Static pages
    (r'^pages/terms_and_conditions/$',TemplateView.as_view(template_name="pages/terms.html")),
    (r'^pages/privacy_policy/$',TemplateView.as_view(template_name="pages/privacy.html")),
    (r'^pages/enjoy-learning/$',TemplateView.as_view(template_name="pages/aprendiendo.html")),
    (r'^pages/enjoy-teaching/$',TemplateView.as_view(template_name="pages/ensenando.html")),
    (r'^pages/enjoy-helping/$',TemplateView.as_view(template_name="pages/ayudando.html")),
    (r'^pages/social-projects/$',TemplateView.as_view(template_name="pages/social_projects.html")),

    #For Paypal
    (r'^paypal/paymeny/23pok420osijos/danoentrain/', include('paypal.standard.ipn.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT,show_indexes=False)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)