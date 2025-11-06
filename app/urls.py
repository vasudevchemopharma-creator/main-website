"""
URL configuration for devapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('aboutus', views.about, name='aboutus'),
    path('ourservices', views.ourservices, name='ourservices'),
    path('products', views.products, name='products'),
    path('MEA-Triazine', views.triazine, name='MEA-Triazine'),
    path('save-email/', views.save_email_for_download, name='save_email'),
    path('contact/', views.handle_contact_form, name='contact'),
    path('contact/ajax/', views.contact_ajax, name='contact_ajax'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),

]

