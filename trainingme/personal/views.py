from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import  RequestContext
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.db.models import Q
from .forms import ProfileForm, UserForm, EmailForm
from .models import Message

@login_required
def edit(request):
    profile = request.user.get_profile()
    profile_form = ProfileForm(instance=profile) # An unbound form
    user_form = UserForm(instance=request.user) # An unbound form
    if request.method == 'POST': # If the form has been submitted...
        profile_form = ProfileForm(request.POST,request.FILES,instance=profile) # A form bound to the POST data
        user_form = UserForm(request.POST,instance=request.user) # A form bound to the POST data
        if user_form.is_valid():
            user_form.save()
        else:
            messages.warning(request,_('Error updating Email Address'))
        if profile_form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            profile = profile_form.save(commit=False)
            profile.is_first_login = False
            profile.save()
            messages.success(request,_('Profile updated sucessfully'))
            return HttpResponseRedirect(reverse('personal.views.view_profile')) # Redirect after POST
        else:
            context = {'profile_form':profile_form,'user_form':user_form}
            messages.error(request,_('Profile failed to update'))
    else:
        context = {'profile_form':profile_form,'user_form':user_form}

    return render_to_response('personal/edit_profile.html',context,context_instance = RequestContext(request))


@login_required
def view_profile(request):
    profile = request.user.get_profile()
    return render_to_response('personal/view_profile.html',{'profile':profile},context_instance = RequestContext(request))


@login_required
def update_email_form(request):
    user = request.user
    email_form = EmailForm(instance=user) # An unbound form
    if request.method == 'POST': # If the form has been submitted...
        email_form = EmailForm(request.POST,request.FILES,instance=user) # A form bound to the POST data
        if email_form.is_valid():
            email_form.save()
            return HttpResponseRedirect(reverse('home'))
        else:
            messages.error(request,_('Error updating Email Address'))
            context = {'email_form':email_form,}
            return render_to_response('personal/update_email_form.html',context,context_instance = RequestContext(request))

    else:
        context = {'email_form':email_form,}
        return render_to_response('personal/update_email_form.html',context,context_instance = RequestContext(request))


@login_required
def list_messages(request):
    msgs = request.user.messages_received.all().order_by('-created_at')
    context = {'msgs': msgs}
    return render_to_response('personal/list_messages.html', context, context_instance = RequestContext(request))


@login_required
def view_conversation(request,with_user_id,msg_id=None):
    msgs = Message.objects.filter(Q(from_user_id=with_user_id) | Q(to_user_id=with_user_id),).order_by('-created_at')
    conversation_with_user = get_object_or_404(User,pk=with_user_id)
    if msg_id:
        msg = get_object_or_404(Message,pk=msg_id)
        msg.is_read = True
        msg.save()
    context = {'msgs': msgs, 'conversation_with_user': conversation_with_user }
    return render_to_response('personal/view_conversation.html', context, context_instance = RequestContext(request))


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))