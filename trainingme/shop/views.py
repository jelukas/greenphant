from django.shortcuts import render_to_response,get_object_or_404
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from paypal.pro.views import PayPalPro
from elearning.models import Course,Enrollment
from django.core.exceptions import ObjectDoesNotExist

@csrf_exempt
def buy_course(request,course_id):
    course = get_object_or_404(Course,pk=course_id,status__name="published")
    if Enrollment.objects.filter(user_id = request.user.id,course_id = course_id):
        messages.warning(request,_('You can not buy this course twice'))
        return HttpResponseRedirect(reverse('learning_course',args=[course_id])) # Redirect

    item = {
        "currency": "EUR",
        'currencycode':  'EUR',
        "amt": course.price,             # amount to charge for item
        "inv": "inventory",         # unique tracking variable paypal
        "course_id": course_id,       # custom tracking variable for you
        "l_desc0": course.title,
        "L_AMT0": course.price,
        "L_QTY0": 1,
        "cancelurl": settings.SITE_URL+reverse('buy_course',args=[course_id]),  # Express checkout cancel url
        "returnurl": settings.SITE_URL+reverse('buy_course',args=[course_id])
    } # Express checkout return url

    kw = {"item": item,                            # what you're selling
          "payment_template": "shop/payment.html",      # template name for payment
          "confirm_template": "shop/confirmation.html", # template name for confirmation
          "context" : { "course":course },
          "success_url": settings.SITE_URL+reverse('success',args=[course_id])}              # redirect location after success

    ppp = PayPalPro(**kw)
    return ppp(request)


@login_required()
def success(request,course_id):
    course = get_object_or_404(Course,pk=course_id,status__name="published")
    enrrolment = get_object_or_404(Enrollment,user_id = request.user.id,course_id = course_id)
    messages.success(request,_('Thank you! Your purchase was successful. You can now watch the course'))
    return HttpResponseRedirect(reverse('learning_course',args=[course_id])) # Redirect