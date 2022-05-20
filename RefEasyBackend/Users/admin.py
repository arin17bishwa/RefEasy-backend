from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *


# Register your models here.


class EmployeeAdmin(UserAdmin):
    list_display = ('email', 'uuid', 'referral_link', 'role')  # What to display as columns
    search_fields = ('email',)  # what to search by
    readonly_fields = ('last_login', 'date_joined')  # Non-editable fields
    ordering = ['date_joined']

    filter_horizontal = ()
    list_filter = ('role',)
    fieldsets = ()


class ApplicantAdmin(UserAdmin):
    list_display = ('email', 'role')  # What to display as columns
    search_fields = ('email',)  # what to search by
    readonly_fields = ('last_login', 'date_joined')  # Non-editable fields
    ordering = ['date_joined']

    filter_horizontal = ()
    list_filter = ('role',)
    fieldsets = ()


admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Applicant, ApplicantAdmin)
