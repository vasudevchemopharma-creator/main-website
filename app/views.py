from django.http import JsonResponse
from django.shortcuts import render,redirect,get_object_or_404
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
from .models import Contact, Product, ProductCategory
from django.shortcuts import render, get_object_or_404
from .models import Product



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

    return render(request, 'MEA-Triazine.html')

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
        
        # Extract document name from file URL
        document_name = file_url.split('/')[-1] if file_url else 'Unknown'
        
        # Save to database
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
    if request.method == 'POST':
        return handle_contact_form(request)
    
    # For GET requests, just render the page with empty form
    form = ContactForm()
    context = {
        'form': form,
    }
    return render(request, 'index.html', context)

def handle_contact_form(request):
    """Handle contact form submission"""
    if request.method == 'POST':
        # Check if it's an AJAX request
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
            # Save the contact message to database
            contact = form.save()
            
            # Send email notification (optional)
            try:
                send_contact_email(contact)
            except Exception as e:
                # Log the error but don't fail the form submission
                print(f"Email sending failed: {e}")
            
            # Return appropriate response
            if request.headers.get('Content-Type') == 'application/json':
                return JsonResponse({
                    'success': True,
                    'message': 'Thank you for your message! We will get back to you soon.'
                })
            else:
                messages.success(request, 'Thank you for your message! We will get back to you soon.')
                return redirect('index')
        
        else:
            # Form has errors
            if request.headers.get('Content-Type') == 'application/json':
                return JsonResponse({
                    'success': False,
                    'message': 'Please correct the errors below.',
                    'errors': form.errors
                }, status=400)
            else:
                messages.error(request, 'Please correct the errors below.')
    
    # For non-POST requests or form errors, render the page
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
    recipient_list = ['info@vasudevchemopharma.com']  # Replace with your email
    
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
            
            # Send email notification
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
    return render(request, 'product_detail.html', {'product': product})



def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'products/product_detail.html', {'product': product})


