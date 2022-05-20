from django.shortcuts import render
from rest_framework import generics
from rest_framework.serializers import ValidationError
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import JobSerializer
from .models import Job


# Create your views here.

class ListCreateJobView(generics.ListCreateAPIView):
    serializer_class = JobSerializer
    filter_fields = ('department', 'location', 'position_type', 'is_open')

    def get_queryset(self):
        """returns all jobs for internal members, open jobs only for others"""
        user = self.request.user
        if not user.is_authenticated:
            return Job.objects.filter(is_open=True)
        grp_name = user.groups.first().name
        if grp_name == 'APP':
            return Job.objects.filter(is_open=True)
        return Job.objects.all()

    def filter_queryset(self, queryset):
        filters = {}
        req = self.request
        for field in self.filter_fields:
            if req.query_params.get(field):  # Ignore empty fields.
                filters[field] = req.query_params.get(field)
        return queryset.filter(**filters)

    def check_create_permissions(self, *args, **kwargs):
        user = self.request.user
        if (not user.is_authenticated) or user.groups.first().name != 'HR':
            raise ValidationError("Not authorised to create job post")
        return True

    def post(self, request, *args, **kwargs):
        _ = self.check_create_permissions()
        return self.create(request, *args, **kwargs)


class JobRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    lookup_url_kwarg = 'slug'
    lookup_field = 'slug'

    def get_serializer_context(self):
        context = super(JobRetrieveUpdateDestroyView, self).get_serializer_context()
        context.update({"request": self.request})
        return context

    def check_update_permissions(self, request, *args, **kwargs):
        user = request.user
        obj = self.get_object()
        if user.groups.first().name != 'HR':
            raise ValidationError('Not authorised for the action. Only HR can do!')
        return True

    def check_view_permission(self, request, *args, **kwargs):
        obj = self.get_object()
        user = request.user
        is_open = obj.is_open
        if is_open:
            return True

        return user.groups.first().name != 'APP'

    def put(self, request, *args, **kwargs):
        _ = self.check_update_permissions(request, *args, **kwargs)
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        _ = self.check_update_permissions(request, *args, **kwargs)
        return self.partial_update(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        _ = self.check_view_permission(request, *args, **kwargs)
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        _ = self.check_update_permissions(request, *args, **kwargs)
        return self.destroy(request, *args, **kwargs)
