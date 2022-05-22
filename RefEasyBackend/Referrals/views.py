from distutils.log import error
from email.mime import application
from django.http import HttpResponse
from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from rest_framework import generics, status
from rest_framework.views import APIView
from Users.models import Applicant, Employee
import json

from Referrals.serializers import ReferralSerializer
from Referrals.models import Referral
from Jobs.models import Job

from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from django.core.mail import send_mail
from RefEasyBackend.settings import MID_PATH, FRONTEND_HOST

# Create your views here.


class ListAllReferrals(generics.ListAPIView):
    serializer_class = ReferralSerializer
    filter_fields = ('ref_emp', 'applicant', 'job', 'status')
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        if user.groups.first().name != 'HR':
            raise PermissionDenied("You are not authorized to view the content.")
        return Referral.objects.all()


class ReferralsCreateView(APIView):
    methods = ['POST']
    permission_classes = (IsAuthenticated,)

    def post(self, request, slug):
        user = self.request.user
        if user.groups.first().name != 'APP':
            return Response({'error': 'Employee cannot apply. Applicants have to apply'},
                            status=status.HTTP_401_UNAUTHORIZED)
        # body_unicode = request.body.decode('utf-8')
        body = request.data
        ref_link = body['referral_link']
        print(ref_link)
        job = Job.objects.get(slug=slug)
        applicant = Applicant.objects.get(user=user)
        ref_emp = Employee.objects.get(referral_link=ref_link)
        referral = Referral(job=job, ref_emp=ref_emp, applicant=applicant, status="L01")
        referral.save()
        return Response({'msg': 'Referred successfully'}, status=status.HTTP_200_OK)


class GetReferralLink(APIView):
    methods = ['GET']
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = self.request.user
        if user.groups.first().name == 'APP':
            return Response({'error': 'Applicants cannot refer'}, status=status.HTTP_401_UNAUTHORIZED)
        emp = Employee.objects.get(user=user)
        return Response({'referral_link': emp.referral_link},
                        status=status.HTTP_200_OK)


class GenLinkJob(APIView):
    methods = ['GET']
    permission_classes = (IsAuthenticated,)

    def get(self, request, job_slug):
        user = self.request.user
        if user.groups.first().name == 'APP':
            return Response({'error': 'Applicants cannot refer'}, status=status.HTTP_401_UNAUTHORIZED)
        emp = Employee.objects.get(user=user)
        referral_link = request.get_host()
        if referral_link == 'localhost:3000':
            referral_link = 'http://' + FRONTEND_HOST
        else:
            referral_link = 'https://' + FRONTEND_HOST
        # mid_path = '/refer/apply/'
        # now defined in settings.py
        referral_link = referral_link + MID_PATH + job_slug + '/' + emp.referral_link + '/'
        print(referral_link)
        return Response({'referral_link': referral_link},
                        status=status.HTTP_200_OK)


class TrackMyReferral(APIView):
    methods = ['GET']
    permission_classes = (IsAuthenticated,)
    serializer_class = ReferralSerializer
    filter_fields = ('ref_emp', 'applicant', 'job', 'status')

    def get(self, request):
        user = self.request.user
        queryset = None
        if user.groups.first().name != 'APP':
            queryset = Referral.objects.filter(ref_emp__user=user)
        else:
            queryset = Referral.objects.filter(applicant__user=user)
        serialized = ReferralSerializer(queryset, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)


class ReferralsUpdateView(APIView):
    methods = ['POST']
    permission_classes = (IsAuthenticated,)
    serializer_class = ReferralSerializer

    def post(self, request):
        user = self.request.user
        if user.groups.first().name != 'HR':
            return Response({"error": "Since not a HR, cannot update status"})
        body = json.loads(request.body)
        job_slug = body['job_slug']
        app_email = body['app_email']
        sts = body['status']
        print(app_email)

        job = Job.objects.get(slug=job_slug)
        app = Applicant.objects.get(email=app_email)
        referral = Referral.objects.get(job=job, applicant=app)
        print(referral.status)
        print(sts)

        # if referral.status == sts:
        #     return Response(status=status.HTTP_200_OK)

        # TODO: Send email to ref_emp and applicant that their status is updated
        referral.status = sts
        referral.save()

        send_mail(
            f"Hi {app.user.username} proceeded to the next round of TI!",
            'Here is the message.',
            'tiitc2022@gmail.com',
            [referral.ref_emp.email],
            fail_silently=False,
        )

        send_mail(
            'Hi you proceeded to the next round of TI!',
            'Here is the message.',
            'tiitc2022@gmail.com',
            [app.email],
            fail_silently=False,
        )
        print(referral.ref_emp.email)
        print(app.email)
        return Response({"msg": "updated"}, status=status.HTTP_200_OK)
