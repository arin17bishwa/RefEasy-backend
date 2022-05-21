from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Job


# Register your models here.


class JobAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'department', 'location', 'position_type', 'is_open')  # What to display as columns
    search_fields = ('title', 'department', 'location', 'position_type')  # what to search by
    readonly_fields = ('created_at', 'last_edit')  # Non-editable fields
    ordering = ['department']

    filter_horizontal = ()
    list_filter = ('department', 'location', 'position_type', 'is_open')
    fieldsets = ()


admin.site.register(Job, JobAdmin)
