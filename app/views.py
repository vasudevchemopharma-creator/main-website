from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'aboutus.html')

def ourservices(request):
    return render(request, 'ourservices.html')

def products(request):
    return render(request, 'products.html')