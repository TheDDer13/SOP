from django.forms import fields
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse
from django import forms
from django.contrib.auth.models import User
from django.forms.models import ModelChoiceField, ModelMultipleChoiceField
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic.edit import CreateView
from .models import Permission,Regulation
import django_filters

# Create your views here.
@login_required (login_url='/login/')
def index(request):
    return render(request, 'management/index.html')

class RegulationForm(forms.ModelForm):
    class Meta:
        model = Regulation
        fields = ['name','code','revision','issued_date','issued_by','recall','link','classified']
        widgets = {'issued_date': forms.SelectDateWidget(years=range(2000, 2050)),
                'issued_by': forms.HiddenInput(),
                'recall': forms.HiddenInput(),}

@method_decorator(login_required, name='dispatch')
class RegulationCreateView(CreateView):
    model = Regulation
    form_class = RegulationForm
    template_name = 'management/CreateRegulation.html'
    def get_initial(self):
        initial = super(RegulationCreateView,self).get_initial()
        initial['issued_by'] = self.request.user.id
        initial['recall'] = False
        return initial
    def get_success_url(self):
            return reverse('Create',args=[self.object.id,])
    def form_valid(self, form):
        self.object = form.save()
        if Regulation.objects.filter(code=self.object.code).exists():
            ExpiredList = Regulation.objects.filter(code=self.object.code).order_by('revision')[1:]
            for expired in ExpiredList:
                expired.recall = True
                expired.save()
        return HttpResponseRedirect(self.get_success_url())

@login_required (login_url='/login/')
def Create(request,pk):
    class CreateForm(forms.ModelForm):
        document = ModelChoiceField(queryset=Regulation.objects.all(),
                                    widget=forms.HiddenInput,)
        user = ModelMultipleChoiceField(label="Phòng ban tiếp nhận",
                                        queryset=User.objects.filter(is_superuser=False).exclude(id=request.user.id),
                                        widget=forms.CheckboxSelectMultiple,)
        class Meta:
            model = Permission
            fields = ['document','user']
    if request.method == 'POST':
        thongtin = CreateForm(request.POST)
        if thongtin.is_valid():
            thongtin.save
            return HttpResponse('Nhập hồ sơ mới thành công')
        return render(request, 'management/Create.html',{
            "form": thongtin,
        })
    return render(request, 'management/Create.html',{
        "form": CreateForm(initial = {"document": Regulation.objects.get(pk=pk)}),
    })

class RegulationFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(label="Tên tài liệu",lookup_expr='icontains')
    classified = django_filters.CharFilter(label="Phân loại",lookup_expr='icontains')
    class Meta:
        model = Regulation
        fields = ['name','classified']

def ListOwner(request):
    user = request.user
    listowner = Regulation.objects.filter(issued_by=user,recall=False).order_by('classified','code')
    regulationlist = RegulationFilter(request.GET, queryset = listowner)
    return render(request, 'management/ListOwner.html', {
        'listowner' : regulationlist, 
    })

@login_required (login_url='/login/')
def ListAll(request):
    user_id = request.user.id
    departments = [{'User':'QA', 'Name':'Đảm bảo chất lượng', 'Docs':None},
                {'User':'RD', 'Name':'Nghiên cứu phát triển', 'Docs':None},
                {'User':'QC', 'Name':'Kiểm tra chất lượng', 'Docs':None},
                {'User':'SX', 'Name':'Xưởng sản xuất', 'Docs':None},
                {'User':'KV', 'Name':'Kho vận', 'Docs':None},
                {'User':'KH', 'Name':'Kế hoạch', 'Docs':None},
                {'User':'CD', 'Name':'Cơ điện', 'Docs':None},
                {'User':'HC', 'Name':'Tổ chức Hành chính', 'Docs':None},
                {'User':'KT', 'Name':'Tài chính Kế toán', 'Docs':None},
                {'User':'DKT', 'Name':'Đăng ký thuốc', 'Docs':None},
                {'User':'HN', 'Name':'Chi nhánh Hà Nội', 'Docs':None},
                {'User':'DN', 'Name':'Chi nhánh Đà Nẵng', 'Docs':None},
                {'User':'HCM', 'Name':'Chi nhánh Hồ Chí Minh', 'Docs':None},]
    for department in departments:
        department['Docs'] = Permission.objects.filter(user=user_id,
                                                    document__issued_by__username=department['User'],
                                                    document__recall=False).order_by('user','document')
    return render(request,'management/ListAll.html',{
        'departments': departments,
    })

@login_required (login_url='/login/')
def Recall(request, pk):
    recall = Regulation.objects.get(id=pk)
    recall.recall = True
    recall.save()
    return HttpResponseRedirect(reverse('ListOwner'))


## QA Department
## RD Department
## QC Department
## Production Department
## Warehouse Department
## PPIC Department
## Technical Department
## HR Department
## Finance Department
## DKT 
## HN branch
## DN branch
## HCM branch