from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User

from .models import Employee, Applicant
from .utils import LowerEmailField


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    email = LowerEmailField(
        required=True,
        allow_blank=False,
        label='Email address',
        max_length=30,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    first_name = serializers.CharField(
        required=True,
        max_length=60,
        allow_blank=False
    )
    last_name = serializers.CharField(
        required=False,
        max_length=60,
        allow_blank=True,
        default=''
    )

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'confirm_password': 'Passwords must match'})
        email = self.validated_data['email'].lower()
        account = User(
            username=email,
            email=email,
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            is_active=True  # TO BE CHANGED TO FALSE
        )
        account.set_password(password)
        account.save()
        # send email from here
        return account


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'groups', 'id']


class EmployeeRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        exclude = ['user', ]


class EmployeeSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Employee
        fields = '__all__'


class ApplicantRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        exclude = ['user', ]


class ApplicantSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Applicant
        fields = '__all__'
