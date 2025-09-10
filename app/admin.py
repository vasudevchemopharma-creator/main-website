# admin.py
from django.contrib import admin
from .models import DownloadEmail

from django.contrib import admin
from .models import Contact

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
    


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'company', 'product', 'created_at', 'is_read']
    list_filter = ['product', 'is_read', 'created_at']
    search_fields = ['name', 'email', 'company', 'message']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'company', 'phone')
        }),
        ('Inquiry Details', {
            'fields': ('product', 'message')
        }),
        ('System Information', {
            'fields': ('created_at', 'is_read'),
            'classes': ('collapse',)
        }),
    )
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
        self.message_user(request, f"{queryset.count()} messages marked as read.")
    mark_as_read.short_description = "Mark selected messages as read"
    
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
        self.message_user(request, f"{queryset.count()} messages marked as unread.")
    mark_as_unread.short_description = "Mark selected messages as unread"
    
    actions = [mark_as_read, mark_as_unread]
    
    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }