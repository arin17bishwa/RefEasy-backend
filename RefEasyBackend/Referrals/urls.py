from django.urls import path
from . import views

app_name = 'Referrals'

urlpatterns = [
    path('', views.GetReferralLink.as_view(), name='referral_link_for_employee'),
    path('generatereferral/<slug:job_slug>/', views.GenLinkJob.as_view(), name='referral_link_with_job_id'),
    path('myreferrals/', views.TrackMyReferral.as_view(), name='my-referrals'),
    path('all-referrals/', views.ListAllReferrals.as_view(), name='list-referrals'),
    path('apply/<slug:slug>/', views.ReferralsCreateView.as_view(), name='list-create-jobs'),
    path('updatestatus/', views.ReferralsUpdateView.as_view(), name='update-status'),
]
