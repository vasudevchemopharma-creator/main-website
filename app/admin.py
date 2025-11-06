# admin.py
from django.contrib import admin
from .models import DownloadEmail, Contact, Product, ProductCategory

@admin.register(DownloadEmail)
class DownloadEmailAdmin(admin.ModelAdmin):
    list_display = ('email', 'document_name', 'downloaded_at')
    list_filter = ('downloaded_at', 'document_name')
    search_fields = ('email', 'document_name')
    readonly_fields = ('downloaded_at',)
    ordering = ('-downloaded_at',)
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

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
    
    actions = ['mark_as_read', 'mark_as_unread']
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
        self.message_user(request, f"{queryset.count()} messages marked as read.")
    mark_as_read.short_description = "Mark selected messages as read"
    
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
        self.message_user(request, f"{queryset.count()} messages marked as unread.")
    mark_as_unread.short_description = "Mark selected messages as unread"

@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'priority', 'category', 'purity', 'cas_number', 'has_files')
    list_filter = ('category', 'grade', 'form')
    search_fields = ('name', 'short_description', 'cas_number')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('priority',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'category', 'priority', 'short_description')
        }),
        ('Specifications', {
            'fields': ('purity', 'packaging', 'application', 'grade', 'form', 'cas_number')
        }),
        ('Media Files', {
            'fields': ('image_url', 'video', 'coa_pdf', 'tds_pdf'),
            'description': 'Upload product related files and images'
        })
    )

    def has_files(self, obj):
        """Check if product has any associated files"""
        return bool(obj.image_url or obj.video or obj.coa_pdf or obj.tds_pdf)
    has_files.boolean = True
    has_files.short_description = 'Has Files'

    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }