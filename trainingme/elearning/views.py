from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import  RequestContext
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from elearning.models import Course
from elearning.forms import CourseForm

@login_required()
def new_course(request):
    if request.method == 'POST': # If the form has been submitted...
        course_form = CourseForm(request.POST,request.FILES) # A form bound to the POST data
        if course_form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            course_form.save()
            return HttpResponseRedirect('edit_profile') # Redirect after POST
    else:
        course_form = CourseForm() # An unbound form

    return render_to_response('elearning/new_course.html',{'course_form':course_form},context_instance = RequestContext(request))