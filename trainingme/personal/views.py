from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import  RequestContext
from django.contrib.auth.decorators import login_required
from personal.forms import ProfileForm
from django.core.urlresolvers import reverse

@login_required
def edit(request):
    profile = request.user.get_profile()
    if request.method == 'POST': # If the form has been submitted...
        profile_form = ProfileForm(request.POST,request.FILES,instance=profile) # A form bound to the POST data
        if profile_form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            profile_form.save()
            return HttpResponseRedirect('edit_profile') # Redirect after POST
    else:
        profile_form = ProfileForm(instance=profile) # An unbound form

    return render_to_response('personal/edit_profile.html',{'profile_form':profile_form},context_instance = RequestContext(request))