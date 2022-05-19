from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *

# Register your models here.


# class EmployeeAdmin(UserAdmin):
#     list_display = ('name', 'email', 'uuid', 'role')  # What to display as columns
#     search_fields = ('email', 'name', '')  # what to search by
#     readonly_fields = ('last_login', 'date_joined')  # Non-editable fields
#     ordering = ['name']
#
#     filter_horizontal = ()
#     list_filter = ('role',)
#     fieldsets = ()


admin.site.register((Employee, Applicant))
