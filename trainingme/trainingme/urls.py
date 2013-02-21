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
    url(r'^shop/', include('shop.urls')),


    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    #Static pages
    (r'^pages/faqs/$',TemplateView.as_view(template_name="pages/faqs.html")),
    (r'^pages/mission/$',TemplateView.as_view(template_name="pages/mission.html")),
    (r'^pages/team/$',TemplateView.as_view(template_name="pages/team.html")),
    (r'^pages/terms_and_conditions/$',TemplateView.as_view(template_name="pages/terms.html")),
    (r'^pages/privacy_policy/$',TemplateView.as_view(template_name="pages/privacy_policy.html")),
    (r'^pages/enjoy-learning/$',TemplateView.as_view(template_name="pages/aprendiendo.html")),
    (r'^pages/enjoy-teaching/$',TemplateView.as_view(template_name="pages/ensenando.html")),
    (r'^pages/enjoy-helping/$',TemplateView.as_view(template_name="pages/ayudando.html")),
    (r'^pages/social-projects/$',TemplateView.as_view(template_name="pages/social_projects.html")),

    #Internationalization
    (r'^i18n/', include('django.conf.urls.i18n')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT,show_indexes=False)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)