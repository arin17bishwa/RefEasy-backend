from django.urls import path
from . import views

app_name = 'Referrals'

urlpatterns = [
    path('', views.GetReferralLink.as_view(), name='referral_link_for_employee'),
    path('myreferrals/', views.TrackMyReferral.as_view(), name='my-referrals'),
    path('allreferrals', views.ListAllReferrals.as_view(), name='list-referrals'),
    path('apply/<str:jobid>/', views.ReferralsCreateView.as_view(), name='list-create-jobs'),
]
