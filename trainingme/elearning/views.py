from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import  RequestContext
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from elearning.models import Status, Course, Subject, Lesson
from elearning.forms import CourseForm,SubjectForm,LessonForm
from elearning.decorators import owner_required


@login_required()
def new_course(request):
    if request.method == 'POST': # If the form has been submitted...
        course_form = CourseForm(request.POST,request.FILES) # A form bound to the POST data
        if course_form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            course = course_form.save(commit=False)
            course.user = request.user
            course.status = Status.objects.get(name="building")
            course.save()
            return HttpResponseRedirect(reverse('elearning.views.edit_course', args=(course.id,))) # Redirect after POST
    else:
        course_form = CourseForm() # An unbound form

    return render_to_response('elearning/new_course.html',{'course_form':course_form},context_instance = RequestContext(request))

@login_required()
#@owner_required(Course)
def edit_course(request,course_id):
    course = Course.objects.get(id=course_id)
    if request.method == 'POST': # If the form has been submitted...
        course_form = CourseForm(request.POST,request.FILES,instance=course) # A form bound to the POST data
        if course_form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            course = course_form.save(commit=False)
            course.user = request.user
            course.save()
            return HttpResponseRedirect(reverse('elearning.views.building_course', args=(course.id,))) # Redirect after POST
    else:
        course_form = CourseForm(instance=course) # An unbound form
    return render_to_response('elearning/edit_course.html',{'course_form':course_form},context_instance = RequestContext(request))


@login_required()
def building_course(request,course_id):
    course = get_object_or_404(Course,pk=course_id,status = Status.objects.get(name="building"))
    return render_to_response('elearning/building_course.html',{'course':course},context_instance = RequestContext(request))


@login_required()
def add_subject(request,course_id):
    if request.method == 'POST': # If the form has been submitted...
        subject_form = SubjectForm(request.POST) # A form bound to the POST data
        if subject_form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            subject = subject_form.save(commit=False)
            subject.course = Course.objects.get(pk=course_id)
            subject.order = 1
            subject.save()
            return HttpResponseRedirect(reverse('elearning.views.building_course', args=(subject.course.id,))) # Redirect after POST
    else:
        subject_form = SubjectForm() # An unbound form

    return render_to_response('elearning/add_subject.html',{'subject_form':subject_form},context_instance = RequestContext(request))

@login_required()
def edit_subject(request,subject_id):
    subject = Subject.objects.get(pk=subject_id)
    if request.method == 'POST': # If the form has been submitted...
        subject_form = SubjectForm(request.POST,instance=subject) # A form bound to the POST data
        if subject_form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            subject = subject_form.save(commit=False)
            subject.order = 1
            subject.save()
            return HttpResponseRedirect(reverse('elearning.views.building_course', args=(subject.course.id,))) # Redirect after POST
    else:
        subject_form = SubjectForm(instance=subject) # An unbound form
    return render_to_response('elearning/edit_subject.html',{'subject_form':subject_form},context_instance = RequestContext(request))

@login_required()
def delete_subject(request,subject_id):
    subject = Subject.objects.get(pk=subject_id)
    course = subject.course
    subject.delete()
    return HttpResponseRedirect(reverse('elearning.views.building_course', args=(course.id,))) # Redirect after POST


@login_required()
def add_lesson(request,subject_id):
    if request.method == 'POST': # If the form has been submitted...
        lesson_form = LessonForm(request.POST) # A form bound to the POST data
        if lesson_form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            lesson = lesson_form.save(commit=False)
            lesson.subject = Subject.objects.get(pk=subject_id)
            lesson.order = 1
            lesson.save()
            return HttpResponseRedirect(reverse('elearning.views.building_course', args=(lesson.subject.course.id,))) # Redirect after POST
    else:
        lesson_form = LessonForm() # An unbound form

    return render_to_response('elearning/add_lesson.html',{'lesson_form':lesson_form},context_instance = RequestContext(request))

@login_required()
def edit_lesson(request,lesson_id):
    lesson = Lesson.objects.get(pk=lesson_id)
    if request.method == 'POST': # If the form has been submitted...
        lesson_form = LessonForm(request.POST,instance=lesson) # A form bound to the POST data
        if lesson_form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            lesson = lesson_form.save(commit=False)
            lesson.order = 1
            lesson.save()
            return HttpResponseRedirect(reverse('elearning.views.building_course', args=(lesson.subject.course.id,))) # Redirect after POST
    else:
        lesson_form = LessonForm(instance=lesson) # An unbound form
    return render_to_response('elearning/edit_lesson.html',{'lesson_form':lesson_form},context_instance = RequestContext(request))

@login_required()
def delete_lesson(request,lesson_id):
    lesson = Lesson.objects.get(pk=lesson_id)
    course = lesson.subject.course;
    lesson.delete()
    return HttpResponseRedirect(reverse('elearning.views.building_course', args=(course.id,))) # Redirect after POST