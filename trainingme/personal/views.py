from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import  RequestContext
from django.contrib.auth.decorators import login_required


@login_required
def edit(request):
    profile = request.user.get_profile()
    return render_to_response('personal/edit_profile.html',{'profile':profile},context_instance = RequestContext(request))
