from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Product, ProductCategory, ProductCharacteristic
from django.core.paginator import Paginator
from django.http import Http404, HttpResponse
from itertools import chain

class Products(ListView):
    template_name = 'pages/products.html'
    model = Product
    paginate_by = 2

    def get_category(self):
        category = ProductCategory.objects.filter(slug=self.kwargs['category']).first()
        return category

    def get_child_products(self, category, lst):
        children = category.get_children()
        if not children:
            query = Product.objects.filter(category=category)
            if query:
                lst.append(query)
        for child in children:
            query = Product.objects.filter(category=child)
            if query:
                lst.append(query)
            self.get_child_products(child, lst)
        return lst

    def get_queryset(self):
        queryset = Product.objects.filter(category=self.get_category())
        if self.get_category().get_children(): 
            results = self.get_child_products(self.get_category(), lst=[])
            for item in results:
                queryset = queryset | item

        if self.request.GET.get('new-products'):
            queryset = queryset.filter(is_new_product=True)

        if self.request.GET.get('avaliable'):
            queryset = queryset.filter(in_stock__gt=0)

        if self.request.GET.get('promo-products'):
            queryset = queryset.filter(promo_price__isnull=False)

        if self.request.GET.get('color'):
            pks = [product.id for product in ProductCharacteristic.objects.filter(color=self.request.GET.get('color'))]
            queryset = queryset.filter(pk__in=pks) 

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_category"] = self.get_category()
        context["characteristics"] = ProductCharacteristic.objects.all()
        context["manufactur"]
        context["current_color"] = self.request.GET.getlist('color')
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = "pages/product-details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if context['product'].category.slug != self.kwargs['category']:
            raise Http404()

        if context['product'].category.parent.slug != self.kwargs['parent']:
            raise Http404()

        if context['product'].category.parent.parent.slug != self.kwargs['parent2']:
            raise Http404()


        return context
    

def product_manufacturer(request):
    return render(request, 'pages/manufacturers.html')

def promo_packs(request):
    return render(request, 'pages/promo-packs.html')

def promo_pack_details(request):
    return render(request, 'pages/promo-pack-details.html')