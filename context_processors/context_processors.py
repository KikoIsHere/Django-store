from products.models import ProductCategory, Product
from orders.cart import Cart

def products_query(request):
    cart_length = Cart(request).__len__()
    return {
        'categories': ProductCategory.objects.all(),
        'products': Product.objects.all(),
        'cart_length': cart_length
    }