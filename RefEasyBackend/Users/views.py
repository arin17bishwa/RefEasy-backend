from django.contrib.auth.models import User
from django.contrib.auth.models import User
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.throttling import AnonRateThrottle
from rest_framework.response import Response
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveUpdateAPIView,
)
from rest_framework.serializers import ValidationError
from .serializers import (
    UserRegistrationSerializer,
    EmployeeRegistrationSerializer,
    ApplicantRegistrationSerializer,
    UserSerializer,
    EmployeeSerializer,
    ApplicantSerializer,

)

from .models import Employee, Applicant


# Create your views here.


class UserRegistrationView(CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        # current_site = get_current_site(self.request)
        # _ = sendVerificationEmail(domain=current_site.domain, user=user)
        # auto creation of profile
        grp_name = user.groups.first().name
        email = user.email
        if grp_name != 'APP':
            profile = Employee(user=user, role=grp_name, email=email)
        else:
            profile = Applicant(user=user, role=grp_name, email=email)
        profile.save()
