from datetime import datetime
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from paypal.pro.signals import payment_was_successful
from paypal.pro.models import PayPalNVP
from elearning.models import Enrollment, Course
from financial.models import Order


def course_has_been_purchased(sender, **kwargs):
    ipn_obj = sender
    ppnvp = PayPalNVP.objects.get(method='DoExpressCheckoutPayment',ack='Success',token=ipn_obj['token'])

    # Generate Order
    order = Order(user_id=ppnvp.user_id,course_id=ipn_obj['course_id'],created_at=datetime.now(),amount=ipn_obj['amt'],is_refund = False, paypal_txn_id = ipn_obj['token'])
    order.save()
    #Enrroll in the course
    enrollment = Enrollment(user_id=ppnvp.user_id,course_id=ipn_obj['course_id'], start_date = datetime.now())
    enrollment.save()

    #Send Email to Teacher
    course = Course.objects.get(pk=ipn_obj['course_id'])
    teacher = User.objects.get(pk = course.user_id)
    student = User.objects.get(pk = ppnvp.user_id)

    ctx_dict = {'course': course,'teacher': teacher, 'student': student}

    message = render_to_string('shop/buy_email.html',ctx_dict)
    subject = _('Someone has purchased your course: ')+course.title
    msg = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, [teacher.email])
    msg.content_subtype = "html"  # Main content is now text/html
    msg.send()

    #Send Email to the New Student
    message = render_to_string('shop/enrroled_email.html',ctx_dict)
    subject = _('You has been enrrolled in ')+course.title
    msg = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, [student.email])
    msg.content_subtype = "html"  # Main content is now text/html
    msg.send()


payment_was_successful.connect(course_has_been_purchased ,dispatch_uid="someone-purchased-course-paypal")