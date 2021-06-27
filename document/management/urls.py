from django.urls import path, include
from . import views
from .views import RegulationCreateView

urlpatterns = [
    path('',include('django.contrib.auth.urls')),
    path('',views.index,name='index'),
    path('RegulationCreate',RegulationCreateView.as_view(),name='RegulationCreate'),
    path('Create/<int:pk>',views.Create,name='Create'),
    path('ListOwner',views.ListOwner,name='ListOwner'),
    path('ListAll',views.ListAll,name='ListAll'),
    path('Recall/<int:pk>',views.Recall,name='Recall'),
]