from distutils.log import error
from email.mime import application
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.views import APIView
from Users.models import Applicant, Employee
import json

from Referrals.serializers import ReferralSerializer
from Referrals.models import Referral
from Jobs.models import Job

from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
# Create your views here.


class ListAllReferrals(generics.ListCreateAPIView):
    serializer_class = ReferralSerializer
    filter_fields = ('ref_emp', 'applicant', 'job', 'status')
    permission_classes = (IsAdminUser,)

    def get_queryset(self):
        return Referral.objects.all()

class ReferralsCreateView(APIView):
    methods = ['POST']
    permission_classes = (IsAuthenticated,)
    def post(self, request, jobid):
        user = self.request.user
        if user.groups.first().name != 'APP':
            return Response({'error':'Employee cannot apply. Applicants have to aply'}, status=status.HTTP_401_UNAUTHORIZED)          
        # body_unicode = request.body.decode('utf-8')
        body = json.loads(request.body)  
        print(body)
        ref_link = body['referral_link']
        print(ref_link)
        job = Job.objects.get(id = jobid)
        applicant = Applicant.objects.get(user = user)
        ref_emp = Employee.objects.get(referral_link=ref_link)
        referral = Referral(job = job, ref_emp = ref_emp, applicant = applicant, status = "In-Process")
        referral.save()
        return Response(status=status.HTTP_200_OK)

class GetReferralLink(APIView):
    methods = ['GET']
    permission_classes = (IsAuthenticated,)
    def get(self, request, jobid):
        user = self.request.user
        if user.groups.first().name == 'APP':
            return Response({'error':'Applicants cannot refer'}, status=status.HTTP_401_UNAUTHORIZED)   
        emp = Employee.objects.get(user=user)       
        return Response({'referral_link': emp.referral_link},
                            status=status.HTTP_200_OK)

class TrackMyReferral(APIView):
    methods = ['GET']
    permission_classes = (IsAuthenticated,)
    serializer_class = ReferralSerializer
    filter_fields = ('ref_emp', 'applicant', 'job', 'status')
    def get(self, request, jobid):
        user = self.request.user
        queryset = None
        if user.groups.first().name != 'APP':
            queryset = Referral.objects.get(ref_emp = user)
        else:
            queryset = Referral.objects.get(Applicant = user)
        return queryset
    