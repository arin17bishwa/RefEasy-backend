from django.urls import path
from . import views

app_name = 'Users'

urlpatterns = [
    path('register/', views.UserRegistrationView.as_view(), name='user_registration'),
    
    path('list/', views.AllUsersView.as_view(), name='all_users_list'),
    path('employee/all/', views.AllEmployeesView.as_view(), name='all_employees_list'),
    path('applicant/all/', views.AllApplicantsView.as_view(), name='all_applicants'),

]
