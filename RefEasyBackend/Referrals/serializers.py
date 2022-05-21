from dataclasses import fields
from pyexpat import model
from rest_framework import serializers

from .models import Referral
from Jobs.serializers import JobSerializer
from Users.serializers import ApplicantSerializer, EmployeeSerializer


class ReferralSerializer(serializers.ModelSerializer):
    job = JobSerializer()
    ref_emp = EmployeeSerializer()
    applicant = ApplicantSerializer()

    class Meta:
        model = Referral
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'slug', 'job', 'ref_emp', 'applicant')
