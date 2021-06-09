from django.urls import path, include
from . import views
from .views import RegulationCreateView, QACreateView, QCCreateView
urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('', views.index, name='index'),
    path('regulationcreate', RegulationCreateView.as_view(), name='regulationcreate'),
    path('QACreate/<int:pk>', QACreateView.as_view(), name='QACreate'),
    path('ListQA', views.QAListView.as_view(), name='ListQA'),
    path('QCCreate/<int:pk>', QCCreateView.as_view(), name='QCCreate'),
    path('ListQC', views.QCListView.as_view(), name='ListQC'),
]