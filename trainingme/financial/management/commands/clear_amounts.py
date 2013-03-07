from django.core.management.base import BaseCommand, CommandError
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from financial.models import Order, Billing
from datetime import datetime, timedelta
from decimal import Decimal

class Command(BaseCommand):
    help = 'Clear the amount of the Orders to the Seller Account if the date of the purschase is equal or more than 30 days'

    def handle(self, *args, **options):
        now = datetime.now()
        #orders = Order.objects.filter(datetime_cleared=None)
        orders = Order.objects.filter(created_at__lte= now - timedelta(days=30),datetime_cleared=None)
        teachers = {}
        if orders.count() > 0:
            for order in orders:
                teacher = order.get_seller()
                billing = teacher.billing
                amount = Decimal(order.amount)*Decimal(str(0.7))
                billing.balance += amount
#                billing.save()
                order.datetime_cleared = now
#                order.save()
                if not teachers.has_key(str(teacher.id)):
                    teachers[str(teacher.id)] = { 'updated_balance': amount }
                else:
                    teachers[str(teacher.id)]['updated_balance'] += amount

        self.send_mail_teachers(teachers)
        self.stdout.write( str(orders.count()) + ' Orders cleared \n')


    def send_mail_teachers(self, teachers):
        for id in teachers.keys():
            teacher = User.objects.get(pk=id)
            ctx_dict = {'teacher': teacher,'updated_amount': teachers[id]['updated_balance']}
            #Send Email to the Teacher
            message = render_to_string('financial/clear_amount_email.html',ctx_dict)
            subject = _('TrainingMe.net - Notice: Amount Cleared to your balance')
            msg = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, [teacher.email])
            msg.content_subtype = "html"  # Main content is now text/html
            msg.send()