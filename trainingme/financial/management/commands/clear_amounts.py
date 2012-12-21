from django.core.management.base import BaseCommand, CommandError
from financial.models import Order, Billing
from datetime import datetime, timedelta
from decimal import Decimal

class Command(BaseCommand):
    help = 'Clear the amount of the Orders to the Seller Account if the date of the purschase is equal or more than 30 days'

    def handle(self, *args, **options):
        now = datetime.now()
        orders = Order.objects.filter(created_at__lte= now - timedelta(days=30),datetime_cleared=None)
        if orders.count() > 0:
            for order in orders:
                billing = order.get_seller().billing
                billing.balance += Decimal(order.amount)*Decimal(str(0.7))
                billing.save()
                order.datetime_cleared = now
                order.save()
                print order
                #An email should be sent
        self.stdout.write( str(orders.count()) + ' Orders cleared \n')