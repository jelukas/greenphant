from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import  RequestContext
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from elearning.models import Status, Course
from elearning.forms import CourseForm

@login_required()
def new_course(request):
    if request.method == 'POST': # If the form has been submitted...
        course_form = CourseForm(request.POST,request.FILES) # A form bound to the POST data
        if course_form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            course = course_form.save(commit=False)
            course.user = request.user
            course.status = Status.objects.get(name="checking")
            course.save()
            return HttpResponseRedirect(reverse('elearning.views.edit_course', args=(course.id,))) # Redirect after POST
    else:
        course_form = CourseForm() # An unbound form

    return render_to_response('elearning/new_course.html',{'course_form':course_form},context_instance = RequestContext(request))

@login_required()
def edit_course(request,course_id):
    course = Course.objects.get(id=course_id)
    if request.method == 'POST': # If the form has been submitted...
        course_form = CourseForm(request.POST,request.FILES,instance=course) # A form bound to the POST data
        if course_form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            course = course_form.save(commit=False)
            course.user = request.user
            course.save()
            return HttpResponseRedirect(reverse('elearning.views.edit_course', args=(course.id,))) # Redirect after POST
    else:
        course_form = CourseForm(instance=course) # An unbound form
    return render_to_response('elearning/edit_course.html',{'course_form':course_form},context_instance = RequestContext(request))