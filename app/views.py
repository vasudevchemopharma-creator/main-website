from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
import json
from .models import DownloadEmail
import logging
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm
from .models import (
    Contact, Product, ProductCategory, CompanyInformation, 
    CompanyFAQ, ProductBlog, CompanyBlog
)
from django.db import OperationalError, ProgrammingError

logger = logging.getLogger(__name__)


def about(request):
    return render(request, 'aboutus.html')


def ourservices(request):
    return render(request, 'ourservices.html')


def products(request):
    categories = ProductCategory.objects.all()
    products = Product.objects.select_related('category').all()
    
    context = {
        'categories': categories,
        'products': products,
    }
    return render(request, 'products.html', context)


def triazine(request):
    try:
        pro = Product.objects.get(name='MEA TRIAZINE 78%')
        
        if pro.image_url:
            image_link = pro.image_url
        else:
            image_link = '/static/img/default_product_image.png' 
        context = {
            'product': pro,
            'triazine_image_url': image_link, 
        }
    except Product.DoesNotExist:
        context = {
            'error_message': 'Product not found.',
            'triazine_image_url': '/static/img/product_not_found.png',
        }
    return render(request, 'products/MEA-Triazine.html', context)


@csrf_exempt
@require_http_methods(["POST"])
def save_email_for_download(request):
    try:
        data = json.loads(request.body)
        email = data.get('email', '').strip()
        file_url = data.get('file_url', '')
        
        if not email:
            return JsonResponse({
                'success': False, 
                'error': 'Email is required'
            }, status=400)
        
        document_name = file_url.split('/')[-1] if file_url else 'Unknown'
        
        DownloadEmail.objects.create(
            email=email,
            document_name=document_name,
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Email saved successfully'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False, 
            'error': str(e)
        }, status=500)


def index(request):
    """Main index view that handles both GET and POST requests"""
    Faqs = CompanyFAQ.objects.all()
    # CompanyInformation may not have new columns until migrations run
    try:
        Com_info = CompanyInformation.objects.first()
    except (OperationalError, ProgrammingError) as e:
        logger.warning('CompanyInformation not available yet: %s', e)
        Com_info = None
    
    # Get recent blogs for homepage
    recent_company_blogs = CompanyBlog.objects.all()[:3]
    
    if request.method == 'POST':
        return handle_contact_form(request)
    
    form = ContactForm()
    context = {
        'form': form,
        'faqs': Faqs,
        'company_info': Com_info,
        'recent_blogs': recent_company_blogs,
    }
    return render(request, 'index.html', context)


def handle_contact_form(request):
    """Handle contact form submission"""
    if request.method == 'POST':
        if request.headers.get('Content-Type') == 'application/json':
            try:
                data = json.loads(request.body)
                form = ContactForm(data)
            except json.JSONDecodeError:
                return JsonResponse({
                    'success': False,
                    'message': 'Invalid JSON data'
                }, status=400)
        else:
            form = ContactForm(request.POST)
        
        if form.is_valid():
            contact = form.save()
            
            try:
                send_contact_email(contact)
            except Exception as e:
                print(f"Email sending failed: {e}")
            
            if request.headers.get('Content-Type') == 'application/json':
                return JsonResponse({
                    'success': True,
                    'message': 'Thank you for your message! We will get back to you soon.'
                })
            else:
                messages.success(request, 'Thank you for your message! We will get back to you soon.')
                return redirect('index')
        
        else:
            if request.headers.get('Content-Type') == 'application/json':
                return JsonResponse({
                    'success': False,
                    'message': 'Please correct the errors below.',
                    'errors': form.errors
                }, status=400)
            else:
                messages.error(request, 'Please correct the errors below.')
    
    context = {
        'form': form if 'form' in locals() else ContactForm(),
    }
    return render(request, 'index.html', context)


def send_contact_email(contact):
    """Send email notification when new contact form is submitted"""
    subject = f"New Contact Form Submission from {contact.name}"
    
    message = f"""
    New contact form submission received:
    
    Name: {contact.name}
    Email: {contact.email}
    Company: {contact.company or 'Not provided'}
    Phone: {contact.phone or 'Not provided'}
    Product Interest: {contact.get_product_display_name or 'Not specified'}
    
    Message:
    {contact.message}
    
    Submitted on: {contact.created_at.strftime('%Y-%m-%d %H:%M:%S')}
    """
    
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = ['info@vasudevchemopharma.com']
    
    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=recipient_list,
        fail_silently=False,
    )


@require_http_methods(["POST"])
def contact_ajax(request):
    """Dedicated AJAX endpoint for contact form"""
    try:
        data = json.loads(request.body)
        form = ContactForm(data)

        if form.is_valid():
            contact = form.save()
            
            try:
                send_contact_email(contact)
            except Exception as e:
                print(f"Email sending failed: {e}")
            
            return JsonResponse({
                'success': True,
                'message': 'Thank you for your message! We will get back to you soon.'
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Please correct the errors below.',
                'errors': form.errors
            }, status=400)
    
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'An error occurred. Please try again.'
        }, status=500)


def product_detail(request, slug):    
    product = get_object_or_404(Product, slug=slug)
    
    product_applications = product.applications.all() 
    product_faqs = product.faqs.all()
    
    # Get blogs related to this product
    product_blogs = product.Blogs.all()
    
    related_products = Product.objects.filter(
        category=product.category
    ).exclude(id=product.id)[:3]
    
    context = {
        'product': product,
        'related_products': related_products,
        'applications': product_applications,
        'faqs': product_faqs,
        'product_blogs': product_blogs,
    }
    return render(request, 'products/product_detail.html', context)


# New Blog Views
def blog_list(request):
    """Display all company blogs"""
    try:
        company_info = CompanyInformation.objects.first()
    except (OperationalError, ProgrammingError) as e:
        logger.warning('CompanyInformation not available yet: %s', e)
        company_info = None
    blogs = CompanyBlog.objects.all()
    
    context = {
        'blogs': blogs,
        'company_info': company_info,
    }
    return render(request, 'blog_list.html', context)


def blog_detail(request, slug):
    """Display individual blog post"""
    try:
        company_info = CompanyInformation.objects.first()
    except (OperationalError, ProgrammingError) as e:
        logger.warning('CompanyInformation not available yet: %s', e)
        company_info = None
    blog = get_object_or_404(CompanyBlog, slug=slug)
    
    # Get related blogs
    related_blogs = CompanyBlog.objects.exclude(id=blog.id)[:3]
    
    context = {
        'blog': blog,
        'related_blogs': related_blogs,
        'company_info': company_info,
    }
    return render(request, 'blog_detail.html', context)


def product_blog_detail(request, slug):
    """Display individual product blog post"""
    blog = get_object_or_404(ProductBlog, slug=slug)
    
    # Get related product blogs
    related_blogs = ProductBlog.objects.filter(
        product=blog.product
    ).exclude(id=blog.id)[:3]
    
    context = {
        'blog': blog,
        'product': blog.product,
        'related_blogs': related_blogs,
    }
    return render(request, 'product_blog_detail.html', context)


def robots_txt(request):
    """Serve a robots.txt dynamically including sitemap location."""
    lines = [
        "User-agent: *",
        "Disallow: /admin/",
        "Allow: /",
        f"Sitemap: {request.build_absolute_uri('/sitemap.xml')}",
    ]
    return HttpResponse('\n'.join(lines), content_type='text/plain')