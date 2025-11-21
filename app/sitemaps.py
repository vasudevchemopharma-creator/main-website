from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Product, CompanyBlog, ProductBlog


class ProductSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return Product.objects.filter(is_active=True)

    def location(self, obj):
        return reverse('product_detail', args=[obj.slug])


class CompanyBlogSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.6

    def items(self):
        return CompanyBlog.objects.all()

    def location(self, obj):
        return reverse('blog_detail', args=[obj.slug])


class ProductBlogSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.6

    def items(self):
        return ProductBlog.objects.all()

    def location(self, obj):
        return reverse('product_blog_detail', args=[obj.slug])
