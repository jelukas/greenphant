from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import  RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from financial.models import Withdraw,Billing,Order
from financial.forms import BillingForm


@login_required()
def view_billing(request):
    billing = get_object_or_404(Billing,pk=request.user.id)
    #Show Messages if Empty:
    if not billing.paypal_account:
        messages.warning(request,_('You can\'t receive payments because your Paypal Adress is not set'))
    if not billing.name:
        messages.warning(request,_('You should set your Name for Invoices'))
    if not billing.surname:
        messages.warning(request,_('You should set your Lastname for Invoices'))
    if not billing.id_number:
        messages.warning(request,_('You must set your National ID number or Passport in order to receive payments from Trainingme.net'))
    withdraws = Withdraw.objects.filter(user_id=request.user.id)
    purchases = Order.objects.filter(user_id=request.user.id)#Your pruchases
    sells = Order.objects.filter(course__user_id=request.user.id)#Your sells
    waiting_clear_amount = Order.get_waiting_clear_amount(request.user.id)
    return render_to_response('financial/view_billing.html',{'billing':billing, 'withdraws':withdraws, 'purchases':purchases,'sells':sells,'waiting_clear_amount':waiting_clear_amount},context_instance = RequestContext(request))


@login_required()
def edit_billing(request):
    billing = get_object_or_404(Billing,user_id=request.user.id)
    if request.method == 'POST': # If the form has been submitted...
        billing_form = BillingForm(request.POST,instance=billing) # A form bound to the POST data
        if billing_form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            billing = billing_form.save(commit=False)
            billing.user = request.user
            billing.save()
            messages.success(request,_('Billing details updated successfully'))
            return HttpResponseRedirect(reverse('financial.views.view_billing')) # Redirect after POST
        else:
            messages.error(request,_('Failed to update the Billing details'))
    else:
        billing_form = BillingForm(instance=billing) # An unbound form
    return render_to_response('financial/edit_billing.html',{'billing_form':billing_form},context_instance = RequestContext(request))
