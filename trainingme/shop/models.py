from datetime import datetime
from paypal.pro.signals import payment_was_successful
from paypal.pro.models import PayPalNVP
from elearning.models import Enrollment
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
    print "TODO OK ! >> Te vamos a matricular en el curso"


payment_was_successful.connect(course_has_been_purchased ,dispatch_uid="someone-purchased-course-paypal")