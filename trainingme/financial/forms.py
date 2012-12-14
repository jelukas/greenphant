from django.forms import ModelForm
from financial.models import Withdraw,Billing,Order


class BillingForm(ModelForm):
    class Meta:
        model = Billing
        exclude = ('user','balance')
