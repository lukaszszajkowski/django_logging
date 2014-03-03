# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render
from main.models import Pensioner
from main.audit import tas_view_audit

import logging
l = logging.getLogger(__name__)

def home(request):
    l.info("home")
    request.session['team'] = "my_team"
    pensioner = Pensioner.objects.filter(surname="Smith")[0]
    return render(request, 'index.html', {'pensioner': pensioner})

@tas_view_audit(operation_label="VIEW")
def index(request):
    l.info("index")
    list = Pensioner.objects.all().order_by('-surname')[:5] #  List 5 members
    return render(request, 'list.html', {'list': list})

def detail(request, reference):
    l.info("detail")
    pensioner = Pensioner.objects.filter(reference=reference)[0]
    return render(request, 'detail.html', {'pensioner': pensioner})

@tas_view_audit(operation_label="VIEW")
def edit(request, reference):
    l.info("edit")
    pensioner = Pensioner.objects.filter(reference=reference)[0]

    if request.method == 'POST':
        pensioner.title = request.POST['title']
        pensioner.forename = request.POST['forename']
        pensioner.surname = request.POST['surname']
        pensioner.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('main.views.home'))

    return render(request, 'detail_edit.html', {'pensioner': pensioner})