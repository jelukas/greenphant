from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import  RequestContext
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from elearning.models import Status, Course, Subject, Lesson, Video, Attach, Enrollment, Comment
from elearning.forms import CourseForm, SubjectForm, LessonForm, VideoForm, AttachForm, CommentForm
from personal.decorators import owner_required
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from elearning.decorators import ajax_required
from django.http import HttpResponseNotFound, Http404
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from django.template.defaultfilters import slugify
from django.db import IntegrityError
from django.db.models import Q

""" BUILD COURSE ZONE """
@login_required()
def new_course(request):
    if request.method == 'POST': # If the form has been submitted...
        course_form = CourseForm(request.POST,request.FILES) # A form bound to the POST data
        if course_form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            course = course_form.save(commit=False)
            course.user = request.user
            course.slug = slugify(course.title)
            course.status = Status.objects.get(name="building")
            try:
                course.save()
            except IntegrityError:
                messages.error(request,_('Course failed to create: Title exits'))
                return HttpResponseRedirect(reverse('elearning.views.new_course',))
            messages.success(request,_('Course created successfully'))
            return HttpResponseRedirect(reverse('elearning.views.building_course', args=(course.id,))) # Redirect after POST
        else:
            messages.error(request,_('Course failed to create'))
    else:
        course_form = CourseForm() # An unbound form

    return render_to_response('elearning/new_course.html',{'course_form':course_form},context_instance = RequestContext(request))


@login_required()
@owner_required(Course)
def edit_course(request,course_id):
    course = get_object_or_404(Course,id=course_id)
    if request.method == 'POST': # If the form has been submitted...
        course_form = CourseForm(request.POST,request.FILES,instance=course) # A form bound to the POST data
        if course_form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            course = course_form.save(commit=False)
            course.user = request.user
            course.slug = slugify(course.title)
            try:
                course.save()
            except IntegrityError:
                messages.error(request,_('Course failed to create: Title exits'))
                return render_to_response('elearning/edit_course.html',{'course_form':course_form,'course':course},context_instance = RequestContext(request))
            messages.success(request,_('Course updated successfully'))
            return HttpResponseRedirect(reverse('elearning.views.building_course', args=(course.id,))) # Redirect after POST
        else:
            messages.error(request,_('Failed to update the course'))
    else:
        course_form = CourseForm(instance=course) # An unbound form
    return render_to_response('elearning/edit_course.html',{'course_form':course_form,'course':course},context_instance = RequestContext(request))


@login_required()
@owner_required(Course)
def building_course(request,course_id):
    course = get_object_or_404(Course,pk=course_id,status = Status.objects.get(name="building"))
    return render_to_response('elearning/building_course.html',{'course':course},context_instance = RequestContext(request))


@login_required()
@owner_required(Course)
def change_checking_status(request,course_id):
    course = get_object_or_404(Course,pk=course_id)
    course.status = Status.objects.get(name="checking")
    course.save()
    messages.success(request,_('Course sent to Checking process'))
    return HttpResponseRedirect(reverse('elearning.views.teaching'))

""" SUBJECT ZONE """
@login_required()
@owner_required(Course)
def add_subject(request,course_id):
    course = get_object_or_404(Course,pk = course_id,status__name = 'building')
    if request.method == 'POST': # If the form has been submitted...
        subject_form = SubjectForm(request.POST) # A form bound to the POST data
        if subject_form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            subject = subject_form.save(commit=False)
            subject.course = Course.objects.get(pk=course_id)
            subject.order = 1
            subject.save()
            messages.success(request,_('Subject added successfully'))
            return HttpResponseRedirect(reverse('elearning.views.building_course', args=(subject.course.id,))) # Redirect after POST
        else:
            messages.error(request,_('Failed to add the subject to the course'))
    else:
        subject_form = SubjectForm() # An unbound form

    return render_to_response('elearning/add_subject.html',{'subject_form':subject_form,'course_id': course.id},context_instance = RequestContext(request))


@login_required()
@owner_required(Subject)
def edit_subject(request,subject_id):
    subject = get_object_or_404(Subject,pk=subject_id)
    if request.method == 'POST': # If the form has been submitted...
        subject_form = SubjectForm(request.POST,instance=subject) # A form bound to the POST data
        if subject_form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            subject = subject_form.save(commit=False)
            subject.order = 1
            subject.save()
            messages.success(request,_('Subject updated successfully'))
            return HttpResponseRedirect(reverse('elearning.views.building_course', args=(subject.course.id,))) # Redirect after POST
        else:
            messages.error(request,_('Failed to update the subject'))
    else:
        subject_form = SubjectForm(instance=subject) # An unbound form
    return render_to_response('elearning/edit_subject.html',{'subject_form':subject_form},context_instance = RequestContext(request))


@login_required()
@owner_required(Subject)
def delete_subject(request,subject_id):
    subject = get_object_or_404(Subject,pk=subject_id)
    course = subject.course
    if course.status.name == 'building':
        subject.delete()
        messages.success(request,_('Subject deleted successfully'))
        return_dict = (reverse('elearning.views.building_course', args=(course.id,))) # Redirect after POST
    else:
        messages.error(request,_('Course is not in Building Status'))
        return_dict = (reverse('elearning.views.teaching',)) # Redirect after POST
    return HttpResponseRedirect(return_dict) # Redirect after POST


"""Move Up in Order One Subject"""
@login_required()
@owner_required(Subject)
def up_order_subject(request,subject_id):
    subject = get_object_or_404(Subject,pk=subject_id,course__status__name="building")
    course = subject.course
    subject.order = subject.order - 1
    subject.save()
    messages.success(request,_('Subject order changed successfully'))
    return_dict = (reverse('elearning.views.building_course', args=(course.id,))) # Redirect
    return HttpResponseRedirect(return_dict) # Redirect


"""Move Down in Order One Subject"""
@login_required()
@owner_required(Subject)
def down_order_subject(request,subject_id):
    subject = get_object_or_404(Subject,pk=subject_id,course__status__name="building")
    course = subject.course
    subject.order = subject.order + 1
    subject.save()
    messages.success(request,_('Subject order changed successfully'))
    return_dict = (reverse('elearning.views.building_course', args=(course.id,))) # Redirect
    return HttpResponseRedirect(return_dict) # Redirect

""" Lesson Zone """
@login_required()
@owner_required(Subject)
def add_lesson(request,subject_id):
    subject = get_object_or_404(Subject,pk=subject_id,course__status__name = 'building')
    if request.method == 'POST': # If the form has been submitted...
        lesson_form = LessonForm(request.POST) # A form bound to the POST data
        video_form = VideoForm(request.POST,request.FILES) # A form bound to the POST data
        if lesson_form.is_valid() and video_form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            lesson = lesson_form.save(commit=False)
            lesson.subject = subject
            lesson.order = 1
            lesson.save()
            video = video_form.save(commit=False)
            video.lesson = lesson
            video.save()
            messages.success(request,_('Lesson added successfully'))
            return HttpResponseRedirect(reverse('elearning.views.building_course', args=(lesson.subject.course.id,))) # Redirect after POST
        else:
            messages.error(request,_('Failed to add the lesson'))
    else:
        lesson_form = LessonForm() # An unbound form
        video_form = VideoForm() # An unbound form
    return render_to_response('elearning/add_lesson.html',{'lesson_form':lesson_form,'video_form': video_form,'subject': subject},context_instance = RequestContext(request))


@login_required()
@owner_required(Lesson)
def edit_lesson(request,lesson_id):
    lesson = get_object_or_404(Lesson,pk=lesson_id,subject__course__status__name = 'building')
    try:
        video = Video.objects.get(pk=lesson.video.id,lesson__subject__course__status__name = 'building')
    except ObjectDoesNotExist:
        video = None
    if request.method == 'POST': # If the form has been submitted...
        lesson_form = LessonForm(request.POST,instance=lesson) # A form bound to the POST data
        video_form = VideoForm(request.POST,request.FILES,instance=video)
        if lesson_form.is_valid() and video_form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            lesson = lesson_form.save(commit=False)
            lesson.order = 1
            lesson.save()
            video = video_form.save(commit=False)
            video.lesson = lesson
            video.save()
            messages.success(request,_('Lesson updated successfully'))
            return HttpResponseRedirect(reverse('elearning.views.building_course', args=(lesson.subject.course.id,))) # Redirect after POST
        else:
            messages.error(request,_('Failed to updated the lesson'))
    else:
        lesson_form = LessonForm(instance=lesson) # An unbound form
        video_form = VideoForm(instance=video) # An unbound form
    return render_to_response('elearning/edit_lesson.html',{'lesson_form':lesson_form,'video_form':video_form},context_instance = RequestContext(request))


@login_required()
@owner_required(Lesson)
def delete_lesson(request,lesson_id):
    lesson = get_object_or_404(Lesson,pk=lesson_id,subject__course__status__name = 'building')
    course = lesson.subject.course
    lesson.delete()
    messages.success(request,_('Lesson deleted successfully'))
    return HttpResponseRedirect(reverse('elearning.views.building_course', args=(course.id,))) # Redirect after POST

""" Video """
@login_required()
@owner_required(Lesson)
def add_video(request,lesson_id):
    if request.method == 'POST': # If the form has been submitted...
        video_form = VideoForm(request.POST,request.FILES) # A form bound to the POST data
        if video_form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            video = video_form.save(commit=False)
            video.lesson = get_object_or_404(Lesson,pk=lesson_id)
            video.save()
            messages.success(request,_('Video added successfully'))
            return HttpResponseRedirect(reverse('elearning.views.building_course', args=(video.lesson.subject.course.id,))) # Redirect after POST
        else:
            messages.error(request,_('Failed to add Video'))
    else:
        video_form = VideoForm() # An unbound form

    return render_to_response('elearning/add_video.html',{'video_form':video_form},context_instance = RequestContext(request))


@login_required()
@owner_required(Video)
def delete_video(request,video_id):
    video = get_object_or_404(Video,pk=video_id)
    course = video.lesson.subject.course
    video.delete()
    messages.success(request,_('Video deleted successfully'))
    return HttpResponseRedirect(reverse('elearning.views.building_course', args=(course.id,))) # Redirect after POST

#NO login Required:
@ajax_required
def free_video(request,video_id):
    video = get_object_or_404(Video,pk=video_id)
    return render_to_response('elearning/free_video.html',{'video':video},context_instance = RequestContext(request))

@login_required()
@owner_required(Video)
def test_video(request,video_id):
    video = get_object_or_404(Video,pk=video_id)
    return render_to_response('elearning/tests/test_video.html',{'video':video},context_instance = RequestContext(request))

""" Anadimos un Adjunto """
@login_required()
@owner_required(Lesson)
def add_attach(request,lesson_id):
    lesson =get_object_or_404(Lesson,pk=lesson_id)
    if request.method == 'POST': # If the form has been submitted...
        attach_form = AttachForm(request.POST,request.FILES) # A form bound to the POST data
        if attach_form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            attach = attach_form.save(commit=False)
            attach.lesson = Lesson.objects.get(pk=lesson_id)
            attach.save()
            messages.success(request,_('File attached successfully'))
            return HttpResponseRedirect(reverse('elearning.views.building_course', args=(attach.lesson.subject.course.id,))) # Redirect after POST
        else:
            messages.error(request,_('Failed to attach File'))
    else:
        attach_form = AttachForm() # An unbound form

    return render_to_response('elearning/add_attach.html',{'attach_form':attach_form,'course_id':lesson.subject.course_id},context_instance = RequestContext(request))


@login_required()
@owner_required(Attach)
def delete_attach(request,attach_id):
    attach = get_object_or_404(Attach,pk=attach_id)
    course = attach.lesson.subject.course
    attach.delete()
    messages.success(request,_('File attached deleted succesfully'))
    return HttpResponseRedirect(reverse('elearning.views.building_course', args=(course.id,))) # Redirect after POST



"""
---------------------------------------
DASHBOARD VIEWS
---------------------------------------
"""

@login_required()
def dashboard(request):
    return render_to_response('elearning/dashboard.html',{},context_instance = RequestContext(request))

@login_required()
def learning(request):
    enrollments = Enrollment.objects.filter(Q(user_id=request.user.id),Q(course__status__name="published") | Q(course__status__name="evaluation period"))
    return render_to_response('elearning/dashboard_learning.html',{'enrollments':enrollments},context_instance = RequestContext(request))

@login_required()
def teaching(request):
    courses = Course.objects.filter(user_id=request.user.id)
    return render_to_response('elearning/dashboard_teaching.html',{'courses':courses},context_instance = RequestContext(request))


""""
--------------------------
COURSE
--------------------------
"""

#@login_required() # No es necesario que este logueado para ver los detalles del curso , Si para comprarlo

def view_course(request,slug):
    from paypal.standard.forms import PayPalEncryptedPaymentsForm
    from django.conf import settings

    course = get_object_or_404(Course,Q(slug=slug),Q(status__name="published")|Q(status__name="evaluation period")|Q(status__name="building"))

    if request.user.is_authenticated():
        enrrollment = course.enrollments.filter(user_id=request.user.id)

        if not enrrollment:
            paypal_dict = {
                "business": settings.PAYPAL_RECEIVER_EMAIL,
                "amount": course.price,
                "currency_code": "EUR",
                "item_name": course.title,
                "item_number": course.id,
                "invoice": "unique-invoice-id",
                "notify_url": "%s%s" % (settings.SITE_NAME, reverse('paypal-ipn')),
                "return_url": "%s%s" % (settings.SITE_URL, reverse('elearning.views.buy_course',)),
                "cancel_return": "http://www.trainingme.net",
                }
            paypal_button = PayPalEncryptedPaymentsForm(initial=paypal_dict)
            context = {'course':course,'paypal_button':paypal_button.sandbox()}
        else:
            context = {'course':course,'enrrolled':True}
            return HttpResponseRedirect(reverse('elearning.views.learning_course', args=(course.id,)))
    else:
        context = {'course':course,'enrrolled':False}
    return render_to_response('elearning/course/view_course.html',context,context_instance = RequestContext(request))


"""
Vista de los contenidos del Curso una vez matriculado
"""
@login_required()
def learning_course(request,course_id):
    course = get_object_or_404(Course,Q(pk=course_id),Q(status__name="published") | Q(status__name="evaluation period"))
    enrrollment = course.enrollments.filter(user_id=request.user.id)
    if not enrrollment:
        return HttpResponseRedirect(reverse('elearning.views.view_course', args=(course.id,)))
    else:
        context = {'course':course,'enrrolled':True}
    return render_to_response('elearning/course/learning_course.html',context,context_instance = RequestContext(request))


"""
Vista de la Leccion una vez matriculado
"""
@login_required()
def learning_lesson(request,lesson_id):
    lesson = get_object_or_404(Lesson,Q(pk=lesson_id),Q(subject__course__status__name="published") | Q(subject__course__status__name="evaluation period"))
    enrrollment = lesson.subject.course.enrollments.filter(user_id=request.user.id)
    if not enrrollment:
        messages.warning(request,_('You are not enrroled in that course: ')+lesson.subject.course.title)
        return HttpResponseRedirect(reverse('elearning.views.view_course', args=(lesson.subject.course.id,)))
    else:
        comments = Comment.objects.filter(lesson_id=lesson.id).order_by('-created_at')
        if request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.user_id = request.user.id
                comment.created_at = datetime.now()
                comment.lesson_id = lesson_id
                comment.save()
                messages.success(request,_('Comment send sucesfully'))
                return HttpResponseRedirect(reverse('elearning.views.learning_lesson', args=(lesson_id,)))
        else:
            comment_form = CommentForm()
        context = {'lesson':lesson,'comments':comments,'comment_form':comment_form,'enrrolled':True}
    return render_to_response('elearning/course/learning_lesson.html',context,context_instance = RequestContext(request))

"""
Vista Previa de la Leccion con el curso en estado Bulding
"""
@login_required()
def preview_lesson(request,lesson_id):
    try:
        lesson = Lesson.objects.get(pk=lesson_id,subject__course__user_id = request.user.id,subject__course__status = Status.objects.get(name="building"))
    except ObjectDoesNotExist:
        raise Http404
    else:
        context = {'lesson':lesson,'enrrolled':True}
    return render_to_response('elearning/course/preview_lesson.html',context,context_instance = RequestContext(request))

"""
COMPRA DEL CURSO
"""
@require_POST
@login_required()
@csrf_exempt
def buy_course(request):
    if request.method == 'POST':
        post_data = request.POST
        if exists_paypal_txn_order(request.POST['item_number'],request.POST['txn_id']):
            messages.error(request,_('Duplicated Transaction'))
            return HttpResponseRedirect(reverse('elearning.views.home'))
        if post_data['payment_status'] == 'Completed':
            course = get_object_or_404(Course,pk=request.POST['item_number'],status__name="published")
            if float(post_data['mc_gross']) == float(course.price) :
                # Create the Order
                from financial.models import Order
                order = Order(user=request.user,course = course,created_at = datetime.now(),amount = post_data['mc_gross'],is_refund = False, paypal_txn_id = post_data['txn_id'])
                order.save()
                #All OK so Enrroll the Student into the Course
                enrollment = Enrollment(user = request.user, course = course, start_date = datetime.now())
                enrollment.save()
                messages.success(request,_('You had been enrolled into the Course ')+course.title)
                return HttpResponseRedirect(reverse('elearning.views.view_course', args=(course.slug,)))
    messages.error(request,_('Error on Transaction '))
    return HttpResponseRedirect(reverse('elearning.views.home'))


def exists_paypal_txn_order(course_id,txn_id):
    from financial.models import Order
    try:
        order = Order.objects.get(course_id=course_id,paypal_txn_id=txn_id)
        return_value = True
    except ObjectDoesNotExist:
        return_value = False
    return return_value


"""
VOTAMOS una LECCION:
Para votar la leccion debemos:
1- El curso debe estar en estado published o evaluation period
2- Estar matriculados en el curso de la leccion
3- No haberla votado antes
"""
@login_required()
def vote_lesson(request,lesson_id,points):
    lesson = get_object_or_404(Lesson,pk=lesson_id)
    if lesson.subject.course.status.name != 'published' and lesson.subject.course.status.name != 'evaluation period' :
        messages.error(request,_('This Course is not Published: ')+lesson.subject.course.title)
        return HttpResponseRedirect(reverse('elearning.views.learning',))
    else:
        enrollment = get_object_or_404(Enrollment,course_id=lesson.subject.course_id,user_id=request.user.id) # you can't vote if you re not enrroled in the course
        if not points or points < 0:
            points = 0

        if not lesson.vote(request.user.id,points):
            messages.error(request,_('You can not vote twice this lesson: ')+lesson.title)
        else:
            messages.success(request,_('You have Rated the lesson with ' + points + ' points'))
        back = request.META.get('HTTP_REFERER',None)
        return HttpResponseRedirect(back)


"""
VOTAMOS un CURSO
"""
@login_required()
def vote_course(request,course_id,points):
    course = Course.objects.get(Q(id=course_id),Q(status__name="published") | Q(status__name="evaluation period"))
    enrollment = get_object_or_404(Enrollment,course_id=course_id,user_id=request.user.id) # you can't vote if you re not enrroled in the course
    if not points or points < 0:
        points = 0

    if not course.rate(request.user.id,points):
        messages.error(request,_('You can not vote twice this course: ')+course.title)
    else:
        messages.success(request,_('You have Rated the course with ' + points + ' points'))
    back = request.META.get('HTTP_REFERER',None)
    return HttpResponseRedirect(back)

"""
HOME PAGE
"""

def home(request):
    if request.POST:
        courses = Course.objects.filter(Q(short_description__icontains=request.POST['query']) | Q(title__icontains=request.POST['query']),Q(status__name="published") | Q(status__name="evaluation period") | Q(status__name="building"))
    else:
        courses = Course.objects.filter(Q(status__name="published") | Q(status__name="evaluation period") | Q(status__name="building"))
    context = {'courses' : courses}
    return render_to_response('elearning/home.html',context,context_instance = RequestContext(request))


"""
---------------------------------------
PAYPAL TESTING
---------------------------------------
"""

from paypal.standard.forms import PayPalEncryptedPaymentsForm
from django.conf import settings

def paypal(request):

    # What you want the button to do.

    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": "10.00",
        "item_name": "Curso de Algo",
        "invoice": "unique-invoice-id",
        "notify_url": "%s%s" % (settings.SITE_NAME, reverse('paypal-ipn')),
        "return_url": "http://www.google.es",
        "cancel_return": "http://www.marca.com",
        }

    # Create the instance.
    form = PayPalEncryptedPaymentsForm(initial=paypal_dict)
    return render_to_response('elearning/tests/paypal.html',{"form": form.sandbox()},context_instance = RequestContext(request))
