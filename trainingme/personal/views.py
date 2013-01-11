from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import  RequestContext
from django.contrib.auth.decorators import login_required
from personal.forms import ProfileForm
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.contrib.auth import logout

@login_required
def edit(request):
    profile = request.user.get_profile()
    if request.method == 'POST': # If the form has been submitted...
        profile_form = ProfileForm(request.POST,request.FILES,instance=profile) # A form bound to the POST data
        if profile_form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            profile = profile_form.save(commit=False)
            profile.is_first_login = False
            profile.save()
            messages.success(request,_('Profile updated sucessfully'))
            return HttpResponseRedirect(reverse('personal.views.view_profile')) # Redirect after POST
        else:
            messages.error(request,_('Profile failed to update'))
    else:
        profile_form = ProfileForm(instance=profile) # An unbound form
    return render_to_response('personal/edit_profile.html',{'profile_form':profile_form},context_instance = RequestContext(request))

@login_required
def view_profile(request):
    profile = request.user.get_profile()
    return render_to_response('personal/view_profile.html',{'profile':profile},context_instance = RequestContext(request))

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))