from django.db import models
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from .models import Regulation, QA, QC
from .forms import QACreateForm

# Create your views here.
@login_required (login_url='/login/')
def index(request):
    return render(request, 'management/index.html')

@method_decorator(login_required, name='dispatch')
class RegulationCreateView(CreateView):
    model = Regulation
    fields = ['name','code','revision','issued_date','issued_by','link',]
    template_name = 'management/CreateRegulation.html'
    def get_initial(self):
        initial = super(RegulationCreateView,self).get_initial()
        initial['issued_by'] = self.request.user.id
        return initial
    def get_success_url(self):
        if self.request.user.username == "QA":
            return reverse('QACreate',args=(self.object.id,))
        if self.request.user.username == "QC":
            return reverse('QCCreate',args=(self.object.id,))

@method_decorator(login_required, name='dispatch')
class QACreateView(CreateView):
    model = QA
    form_class = QACreateForm
    template_name = 'management/CreateQA.html'
    success_url = '/ListQA'
    def get_initial(self):
        initial = super(QACreateView,self).get_initial()
        initial['document'] = Regulation.objects.get(pk=self.args)
        #initial['id'] = self.args
        return initial
    def form_valid(self, form):
        #self.object.document = Regulation.objects.get(id=self.args)
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

@method_decorator(login_required, name='dispatch')
class QAListView(ListView):
    model = QA
    context_object_name = 'QA_list'
    queryset = QA.objects.all()
    template_name = 'management/ListQA.html' 

@method_decorator(login_required, name='dispatch')
class QCCreateView(CreateView):
    model = QC
    fields = ['document','user',]
    template_name = 'management/CreateQC.html'
    success_url = '/ListQC'
    def get_initial(self):
        initial = super(QCCreateView,self).get_initial()
        initial['document'] = self.args[0]
        return initial

@method_decorator(login_required, name='dispatch')
class QCListView(ListView):
    model = QC
    context_object_name = 'QC_list'
    queryset = QC.objects.all()
    template_name = 'management/ListQC.html' 