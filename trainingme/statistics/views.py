from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from elearning.models import Category
from .models import Interest
from .forms import InterestList



def interest_form(request):
    interest_form = InterestList()
    interest_form.fields['category'].choices = [(x.id, x) for x in Category.objects.all()]
    if request.method == 'POST':
        interest_form = InterestList(request.POST)
        categories =request.POST.getlist('category')
        for cat in categories:
            interest = Interest()
            interest.user = request.user
            interest.category_id = cat
            interest.save()
        return HttpResponseRedirect(reverse('elearning.views.home',))

    return render_to_response('statistics/interest_form.html', {'interest_form': interest_form},context_instance = RequestContext(request))