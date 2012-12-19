from django.contrib import admin
from financial.models import Billing,Withdraw,Order


class BillingAdmin(admin.ModelAdmin):
    list_display = ('user','balance','paypal_account','name','surname','id_number')


class WithdrawAdmin(admin.ModelAdmin):
    list_display = ('user','datetime','amount','sent_to',)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('user','course','created_at','amount','is_refund','datetime_cleared','paypal_txn_id')


admin.site.register(Billing,BillingAdmin)
admin.site.register(Withdraw,WithdrawAdmin)
admin.site.register(Order,OrderAdmin)