from django.urls import path
from . import views

app_name = 'Jobs'

urlpatterns = [
    path('', views.ListCreateJobView.as_view(), name='list-create-jobs'),
]
