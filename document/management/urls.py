from django.urls import path, include
from . import views
from .views import SOPListView, SOPCreateView, PermissionListView, ClassificationListView, AllListView

urlpatterns = [
    path('',include('django.contrib.auth.urls')),
    path('',views.index, name='index'),
    path('ViewOwner',SOPListView.as_view(),name='ViewOwner'),
    path('CreateSOP',SOPCreateView.as_view(),name='CreateSOP'),
    path('ViewPermission',PermissionListView.as_view(),name='ViewPermission'),
    path('Recall/<int:pk>',views.Recall,name='Recall'),
    path('ViewClassification',ClassificationListView.as_view(),name='ViewClassification'),
    path('Classification/<int:pk>',views.Classify,name='Classification'),
    path('ViewAll',AllListView.as_view(),name='ViewAll'),
]