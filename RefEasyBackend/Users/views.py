from django.contrib.auth.models import User
from django.contrib.auth.models import User
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
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


@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
def userDetailsView(request):
    user = request.user
    grp_name = user.groups.first().name
    if grp_name == 'APP':
        profile = Applicant.objects.get(user=user)
        serializer_class = ApplicantSerializer
    else:
        profile = Employee.objects.get(user=user)
        serializer_class = EmployeeSerializer
    res = serializer_class(profile).data

    return Response(data=res)


class AllUsersView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)


class AllEmployeesView(ListAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = (IsAdminUser,)


class AllApplicantsView(ListAPIView):
    queryset = Applicant.objects.all()
    serializer_class = ApplicantSerializer
    permission_classes = (IsAdminUser,)
