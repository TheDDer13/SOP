from django import forms
from django.forms.widgets import HiddenInput, Textarea
from .models import Regulation, QA, QC

class QACreateForm(forms.ModelForm):
    class Meta:
        model = QA
        fields = ['document','user',]
        #widgets = {'document': forms.HiddenInput,}
                #'trangthai': forms.HiddenInput,
                #'thoihan': forms.SelectDateWidget(years=range(2000, 2050)),}
