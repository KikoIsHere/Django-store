from django.shortcuts import render
from django.views.generic import ListView
from .models import Product, ProductCategory
from django.core.paginator import Paginator

class Products(ListView):
    template_name = 'pages/products.html'
    model = Product
    paginate_by = 2
    

def product_detail(request):
    return render(request, 'pages/product-details.html')

def product_manufacturer(request):
    return render(request, 'pages/manufacturers.html')

def promo_packs(request):
    return render(request, 'pages/promo-packs.html')

def promo_pack_details(request):
    return render(request, 'pages/promo-pack-details.html') 
