from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
import json
from .models import DownloadEmail
import logging

logger = logging.getLogger(__name__)


def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'aboutus.html')

def ourservices(request):
    return render(request, 'ourservices.html')

def products(request):
    return render(request, 'products.html')

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
