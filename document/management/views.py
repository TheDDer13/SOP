from django.forms import fields
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse
from django import forms
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.forms.models import ModelChoiceField, ModelMultipleChoiceField
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic.edit import CreateView
from .models import Classification, SOP
from django.views.generic.list import ListView
import django_filters
from django.template.loader import render_to_string

# Create your views here.
@login_required (login_url='/login/')
def index(request):
    return render(request, 'management/index.html')

## Xem danh sách đã ban hành
class SOPFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(label="Tên tài liệu",lookup_expr='icontains')
    code = django_filters.CharFilter(label="Mã tài liệu",lookup_expr='iexact')
    dept_classified = django_filters.CharFilter(label="Phân loại",lookup_expr='icontains')
    class Meta:
        model = SOP
        fields = ['name','code','dept_classified']

@method_decorator(login_required, name='dispatch')
class SOPListView(ListView):
    model = SOP
    template_name = 'management/sop_owner_view.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = SOP.objects.filter(issued_by=self.request.user,recall=False).order_by('dept_classified','code')
        SOPlist = SOPFilter(self.request.GET, queryset=qs)
        context['SOPlist'] = SOPlist
        return context

## Ban hành SOP
class SOPForm(forms.ModelForm):
    class Meta:
        model = SOP
        fields = ['name','code','revision','issued_date','issued_by','recall','link','dept_classified','permission']
        widgets = {'issued_date': forms.SelectDateWidget(years=range(2000, 2050)),
                #'issued_date': forms.DateInput(),
                'issued_by': forms.HiddenInput(),
                'recall': forms.HiddenInput(),
                'permission': forms.CheckboxSelectMultiple(),
                }
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(SOPForm, self).__init__(*args, **kwargs)
        self.fields['permission'].queryset = User.objects.filter(is_superuser=False).exclude(id=self.request.user.id)    

@method_decorator(login_required, name='dispatch')
class SOPCreateView(CreateView):
    model = SOP
    form_class = SOPForm
    template_name = 'management/partial_sop_create.html'
    success_url = 'CreateSOP'
    def get_form_kwargs(self):
        kwargs = super(SOPCreateView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs
    def get_initial(self):
        initial = super(SOPCreateView,self).get_initial()
        initial['issued_by'] = self.request.user.id
        initial['recall'] = False
        return initial
    def form_valid(self, form):
        newcode = self.request.POST.get('code')
        newrevision = self.request.POST.get('revision')
        if SOP.objects.filter(code=newcode).exists():
            ExpiredList = SOP.objects.filter(code=newcode).exclude(revision=newrevision)
            for expired in ExpiredList:
                expired.recall = True
                expired.save()
        self.object = form.save()
        return HttpResponseRedirect(reverse('ViewOwner'))
    # def render_to_response(self, context, **response_kwargs):
    #     if self.request.is_ajax():
    #         html_form = render_to_string('management/partial_sop_create.html',{
    #             'form': SOPForm(),
    #         })
    #         return JsonResponse({'html_form': html_form})
    #     else:
    #         return super(CreateView,self).render_to_response(context, **response_kwargs)

## Xem danh sách được phân quyền
class PermissionFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(label="Tên tài liệu",lookup_expr='icontains')
    code = django_filters.CharFilter(label="Mã tài liệu",lookup_expr='iexact')
    issued_by = django_filters.CharFilter(field_name='issued_by__username',label="Phòng ban",lookup_expr='icontains')
    class Meta:
        model = SOP
        fields = ['name','code','issued_by']

@method_decorator(login_required, name='dispatch')
class PermissionListView(ListView):
    model = SOP
    template_name = 'management/sop_permission_view.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = SOP.objects.filter(permission=self.request.user,recall=False).order_by('issued_by','dept_classified','code')
        SOPlist = PermissionFilter(self.request.GET, queryset=qs)
        context['SOPlist'] = SOPlist
        return context

## Thu hồi SOP
@login_required (login_url='/login/')
def Recall(request, pk):
    recall = SOP.objects.get(id=pk)
    recall.recall = True
    recall.save()
    return HttpResponseRedirect(reverse('ViewOwner'))

## Phân loại SOP của QLCL
@method_decorator(login_required, name='dispatch')
class PermissionListView(ListView):
    model = SOP
    template_name = 'management/sop_permission_view.html'

@method_decorator(login_required, name='dispatch')
class ClassificationListView(ListView):
    model = SOP
    queryset = SOP.objects.filter(sys_classified=None,recall=False).order_by('issued_by','code')
    context_object_name = 'SOPlist'
    template_name = 'management/sop_classification_view.html'

@login_required (login_url='/login/')
def Classify(request,pk):
    classified = request.GET.getlist('classified')
    sop = SOP.objects.get(pk=pk)
    for i in classified:
        sop.sys_classified.add(Classification.objects.get(classified=i))
        sop.save()
    return HttpResponseRedirect(reverse('ViewClassification'))

## Xem danh sách theo phân loại QLCL
class AllFilter(django_filters.FilterSet):
    issued_by = django_filters.CharFilter(field_name='issued_by__username',label="Phòng ban",lookup_expr='icontains')
    sys_classified = django_filters.CharFilter(field_name='sys_classified__classified',label="Phân loại",lookup_expr='icontains')
    class Meta:
        model = SOP
        fields = ['issued_by','sys_classified']

@method_decorator(login_required, name='dispatch')
class AllListView(ListView):
    model = SOP
    template_name = 'management/sop_all_view.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = SOP.objects.filter(recall=False).order_by('code')
        SOPlist = AllFilter(self.request.GET, queryset=qs)
        context['SOPlist'] = SOPlist
        return context

## QA Department 'Đảm bảo chất lượng'
## RD Department 'Nghiên cứu phát triển'
## QC Department 'Kiểm tra chất lượng'
## Production Department 'Xưởng sản xuất'
## Warehouse Department  'Kho vận'
## PPIC Department  'Kế hoạch'
## Technical Department 'Cơ điện'
## HR Department   'Tổ chức Hành chính',
## Finance Department  'Tài chính Kế toán'
## DKT   'Đăng ký thuốc'
## HN branch   'Chi nhánh Hà Nội'
## DN branch 'Chi nhánh Đà Nẵng'
## HCM branch   'Chi nhánh Hồ Chí Minh'