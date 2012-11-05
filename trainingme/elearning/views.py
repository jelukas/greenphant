from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import  RequestContext
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from elearning.models import Status, Course, Subject, Lesson, Video, Attach
from elearning.forms import CourseForm, SubjectForm, LessonForm, VideoForm, AttachForm
from personal.decorators import owner_required


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
@owner_required(Course)
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
@owner_required(Course)
def building_course(request,course_id):
    course = get_object_or_404(Course,pk=course_id,status = Status.objects.get(name="building"))
    return render_to_response('elearning/building_course.html',{'course':course},context_instance = RequestContext(request))


@login_required()
@owner_required(Course)
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
@owner_required(Subject)
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
@owner_required(Subject)
def delete_subject(request,subject_id):
    subject = Subject.objects.get(pk=subject_id)
    course = subject.course
    subject.delete()
    return HttpResponseRedirect(reverse('elearning.views.building_course', args=(course.id,))) # Redirect after POST


@login_required()
@owner_required(Subject)
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
@owner_required(Lesson)
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
@owner_required(Lesson)
def delete_lesson(request,lesson_id):
    lesson = Lesson.objects.get(pk=lesson_id)
    course = lesson.subject.course
    lesson.delete()
    return HttpResponseRedirect(reverse('elearning.views.building_course', args=(course.id,))) # Redirect after POST


@login_required()
@owner_required(Lesson)
def add_video(request,lesson_id):
    if request.method == 'POST': # If the form has been submitted...
        video_form = VideoForm(request.POST,request.FILES) # A form bound to the POST data
        if video_form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            video = video_form.save(commit=False)
            video.lesson = Lesson.objects.get(pk=lesson_id)
            video.save()
            return HttpResponseRedirect(reverse('elearning.views.building_course', args=(video.lesson.subject.course.id,))) # Redirect after POST
    else:
        video_form = VideoForm() # An unbound form

    return render_to_response('elearning/add_video.html',{'video_form':video_form},context_instance = RequestContext(request))


@login_required()
@owner_required(Video)
def delete_video(request,video_id):
    video = Video.objects.get(pk=video_id)
    course = video.lesson.subject.course
    video.delete()
    return HttpResponseRedirect(reverse('elearning.views.building_course', args=(course.id,))) # Redirect after POST

@login_required()
@owner_required(Video)
def test_video(request,video_id):
    video = Video.objects.get(pk=video_id)
    return render_to_response('elearning/tests/test_video.html',{'video':video},context_instance = RequestContext(request))

@login_required()
@owner_required(Lesson)
def add_attach(request,lesson_id):
    if request.method == 'POST': # If the form has been submitted...
        attach_form = AttachForm(request.POST,request.FILES) # A form bound to the POST data
        if attach_form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            attach = attach_form.save(commit=False)
            attach.lesson = Lesson.objects.get(pk=lesson_id)
            attach.save()
            return HttpResponseRedirect(reverse('elearning.views.building_course', args=(attach.lesson.subject.course.id,))) # Redirect after POST
    else:
        attach_form = AttachForm() # An unbound form

    return render_to_response('elearning/add_attach.html',{'attach_form':attach_form},context_instance = RequestContext(request))


@login_required()
@owner_required(Attach)
def delete_attach(request,video_id):
    attach = Attach.objects.get(pk=video_id)
    course = attach.lesson.subject.course
    attach.delete()
    return HttpResponseRedirect(reverse('elearning.views.building_course', args=(course.id,))) # Redirect after POST