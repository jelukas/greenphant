from financial.models import Billing

billing = Billing.objects.get(pk=1)

billing.name = 'paco malu'

billing.save()