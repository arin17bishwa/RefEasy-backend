from dataclasses import fields
from pyexpat import model
from rest_framework import serializers

from .models import Referral


class ReferralSerializer(serializers.ModelSerializer):
    class Meta:
        model = Referral
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'slug')