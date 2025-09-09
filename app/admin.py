# admin.py
from django.contrib import admin
from .models import DownloadEmail

@admin.register(DownloadEmail)
class DownloadEmailAdmin(admin.ModelAdmin):
    list_display = ('email', 'document_name', 'downloaded_at')  # Removed 'ip_address'
    list_filter = ('downloaded_at', 'document_name')
    search_fields = ('email', 'document_name')  # Removed 'ip_address'
    readonly_fields = ('downloaded_at',)
    ordering = ('-downloaded_at',)
    
    def has_add_permission(self, request):
        return False  # Prevent manual addition through admin
    
    def has_change_permission(self, request, obj=None):
        return False  # Make records read-only
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser  # Only superusers can delete