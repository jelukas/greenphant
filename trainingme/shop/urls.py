from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^course/buy/(\d+)/$','shop.views.buy_course', name='buy_course' ),
    url(r'^course/success/(\d+)/$','shop.views.success', name='success' ),
    url(r'^paypal/o6as892348yucidy892730927354eihdvhxocibib/', include('paypal.standard.ipn.urls'))
)

