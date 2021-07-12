from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart, name='cart'),
    path('add-<slug>', views.cart_add, name='cart-add'),
    path('remove-<slug>', views.cart_remove, name='cart-remove'),
    path('update', views.cart_update, name='cart-update'),
    path('step2', views.cart_step2, name='cart-step2'),
    path('step3', views.cart_step3, name='cart-step3'),
    path('step3-unicredit', views.cart_step3_unicredit, name='cart-step3-unicredit'),

    path('coupon', views.cart_add_coupon, name='add-coupon')
]

