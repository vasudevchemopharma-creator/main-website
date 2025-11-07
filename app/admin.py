from django.contrib import admin
from .models import (
    DownloadEmail,
    Contact,
    ProductCategory,
    Product,
    ProductFAQ,
    ProductApplication
)


# -------------------------------------------------------------------
# Inlines for Product
# -------------------------------------------------------------------
class ProductFAQInline(admin.TabularInline):
    model = ProductFAQ
    extra = 1


class ProductApplicationInline(admin.TabularInline):
    model = ProductApplication
    extra = 1


# -------------------------------------------------------------------
# Product Admin
# -------------------------------------------------------------------
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'category', 'purity', 'grade', 'form',
        'priority', 'is_active'
    )
    list_filter = ('category', 'is_active')
    search_fields = ('name', 'category__name', 'cas_number')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('is_active', 'priority')
    inlines = [ProductFAQInline, ProductApplicationInline]

    fieldsets = (
        ('Basic Info', {
            'fields': (
                'priority', 'category', 'name', 'slug',
                'short_description', 'detailed_description',
                'is_active'
            )
        }),
        ('Specifications', {
            'fields': (
                'purity', 'packaging', 'grade', 'form',
                'cas_number', 'formula', 'appearance',
                'assay', 'molecular_weight', 'density',
                'boiling_point', 'melting_point', 'application'
            )
        }),
        ('Media & Downloads', {
            'fields': (
                'image_url', 'main_image', 'gallery_image_1', 'gallery_image_2',
                'video', 'coa_pdf', 'tds_pdf'
            )
        }),
        ('Certifications & SEO', {
            'fields': (
                'iso_certifications', 'meta_title',
                'meta_description', 'meta_keywords'
            )
        }),
    )


# -------------------------------------------------------------------
# Category Admin
# -------------------------------------------------------------------
@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


# -------------------------------------------------------------------
# Contact Admin
# -------------------------------------------------------------------
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'company', 'product', 'created_at', 'is_read')
    list_filter = ('product', 'is_read', 'created_at')
    search_fields = ('name', 'email', 'company', 'message')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)


# -------------------------------------------------------------------
# DownloadEmail Admin
# -------------------------------------------------------------------
@admin.register(DownloadEmail)
class DownloadEmailAdmin(admin.ModelAdmin):
    list_display = ('email', 'document_name', 'downloaded_at')
    search_fields = ('email', 'document_name')
    readonly_fields = ('downloaded_at',)
    ordering = ('-downloaded_at',)


# -------------------------------------------------------------------
# FAQ & Application Admin (optional direct view)
# -------------------------------------------------------------------
@admin.register(ProductFAQ)
class ProductFAQAdmin(admin.ModelAdmin):
    list_display = ('product', 'question')
    search_fields = ('product__name', 'question')


@admin.register(ProductApplication)
class ProductApplicationAdmin(admin.ModelAdmin):
    list_display = ('product', 'title')
    search_fields = ('product__name', 'title')
