from django.shortcuts import render

def home(request):
    return render(request, 'pages/index.html')

def sitemap(request):
    return render(request, 'pages/site_map.html')