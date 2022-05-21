from django.contrib import admin
from .models import Referral


# Register your models here.

class ReferralAdmin(admin.ModelAdmin):
    list_display = ('job', 'ref_emp', 'applicant', 'slug', 'status')  # What to display as columns
    search_fields = ('slug',)  # what to search by
    readonly_fields = ('created_at', 'updated_at')  # Non-editable fields
    ordering = ['updated_at']

    filter_horizontal = ()
    list_filter = ('status',)
    fieldsets = ()


admin.site.register(Referral, ReferralAdmin)
