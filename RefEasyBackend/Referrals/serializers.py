from dataclasses import fields
from pyexpat import model
from rest_framework import serializers

from .models import Referral
from Jobs.serializers import JobSerializer
from Users.serializers import ApplicantSerializer, EmployeeSerializer

STATUS_MAPPING = {i: j for i, j in Referral.STATUS_CHOICES}


class ReferralSerializer(serializers.ModelSerializer):
    job = JobSerializer()
    ref_emp = EmployeeSerializer()
    applicant = ApplicantSerializer()

    class Meta:
        model = Referral
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'slug', 'job', 'ref_emp', 'applicant')


class ReferralViewingSerializer(serializers.ModelSerializer):
    job = JobSerializer()
    ref_emp = EmployeeSerializer()
    applicant = ApplicantSerializer()
    status = serializers.SerializerMethodField()

    class Meta:
        model = Referral
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'slug', 'job', 'ref_emp', 'applicant')

    def get_status(self, obj):
        return STATUS_MAPPING[obj.status]
