from django.contrib import admin
from financial.models import Billing,Withdraw,Order

admin.site.register(Billing)
admin.site.register(Withdraw)
admin.site.register(Order)