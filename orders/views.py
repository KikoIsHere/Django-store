from django.shortcuts import render
from .cart import Cart
from users.models import Account, LegalAccount
from products.models import Product
from .models import Coupon
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import string
import secrets


@login_required
def cart(request):
    cart = Cart(request)
    context = {
        'cart':cart,
    }
    return render(request, 'pages/shopping-cart.html', context)

@login_required
def cart_add(request, slug):
    product = Product.objects.get(slug=slug)
    Cart(request).add(product=product)
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def cart_remove(request, slug):
    product = Product.objects.get(slug=slug)
    Cart(request).remove(product=product)
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
@csrf_exempt
def cart_update(request):
    cart = Cart(request)
    data = {}
    if request.is_ajax():
        value = request.POST.get('value')
        slug = request.POST.get('slug')
        product = Product.objects.get(slug=slug)
        cart.cart[str(product.id)]['quantity'] = int(value)
        data['quantity'] = cart.cart[str(product.id)]['quantity']
        data['total_price'] = cart.get_total_price()
        try:
            data['discount'] = cart.get_discount()
            data['final_price'] = cart.get_final_price()
        except Exception:
            pass 
        print(cart.cart)
        request.session.save()
    return JsonResponse(data)

@login_required
def cart_add_coupon(request):
    if request.method == 'POST':
        code = request.POST.get('promo')
        if request.user.is_normal == True:
            user = Account.objects.get(user=request.user)
        else:
            user = LegalAccount.objects.get(user=request.user)

        cart = Cart(request)

        if user.club_card == code:
            request.session['discount'] = cart.discount_code(user.club_card)
        else:
            coupon = Coupon.objects.filter(code=code).first()
            request.session['discount'] = cart.discount_code(coupon.discount)
        request.session.save()
        return redirect('cart')

    return redirect('cart')


def cart_step2(request):
    return render(request, 'pages/shopping-cart-step2.html')

def cart_step3(request):
    return render(request, 'pages/shopping-cart-step3.html')

def cart_step3_unicredit(request):
    return render(request, 'pages/shopping-cart-step3-unicredit.html')