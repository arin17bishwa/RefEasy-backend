from django.urls import path
from . import views

app_name = 'Jobs'

urlpatterns = [
    path('', views.ListJobView.as_view(), name='list-jobs'),
    path('create/', views.CreateJobView.as_view(), name='create-jobs'),
    path('details/<slug:slug>/', views.JobRetrieveUpdateDestroyView.as_view(), name='list-create-jobs'),
]
