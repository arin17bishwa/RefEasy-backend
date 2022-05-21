from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User

from .models import Job

DEPT_MAPPING = {i: j for i, j in Job.DEPT_CHOICES}
LOC_MAPPING = {i: j for i, j in Job.LOC_CHOICES}
POS_MAPPING = {i: j for i, j in Job.POS_CHOICES}


class JobSerializer(serializers.ModelSerializer):
    department = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()
    position_type = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = '__all__'
        read_only_fields = ('created_at', 'last_edit', 'slug')

    def get_department(self, obj):
        return DEPT_MAPPING[obj.department]

    def get_location(self, obj):
        return LOC_MAPPING[obj.location]

    def get_position_type(self, obj):
        return POS_MAPPING[obj.position_type]
