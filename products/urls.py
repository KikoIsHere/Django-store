from django.urls import path
from . import views

urlpatterns = [
    path('', views.Products.as_view(), name='products'),
    path('detail', views.product_detail, name='products-detail'),
    path('manufacturer',views.product_manufacturer, name='products-manufacturers')
]
