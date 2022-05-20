from django.urls import path
from . import views

app_name = 'Users'

urlpatterns = [
    path('register/', views.UserRegistrationView.as_view(), name='user_registration'),

]
