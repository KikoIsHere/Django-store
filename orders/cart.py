from decimal import Decimal
from django.conf import settings
from products.models import Product

class Cart(object):

    def __init__(self, request):
        """
        Initialize the cart.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart


    def add(self, product, quantity=1, override_quantity=False):
        """
        Add a product to the cart or update its quantity.
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            if product.promo_price:
                self.cart[product_id] = {'quantity': 0,
                'price': str(product.promo_price)}
            else:
                self.cart[product_id] = {'quantity': 0,
                'price': str(product.old_price)}
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

        
    def save(self):
        # mark the session as "modified" to make sure it gets saved
        self.session.modified = True

    def remove(self, product):
        """
        Remove a product from the cart.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
        self.save()


    def __len__(self):
        """
        Count all items in the cart.
        """

        return sum(item['quantity'] for product_id, item in self.cart.items() if product_id != 'discount')

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for product_id, item in self.cart.items() if product_id != 'discount')


    def discount_code(self, discount):
        self.cart['discount'] = discount
        self.save()

    def get_discount(self):
        try:
            return (Decimal(self.cart['discount']) * self.get_total_price()) / 100
        except KeyError:
            return None


    def get_final_price(self):
        if self.get_discount() == None:
            return self.get_total_price()
        return self.get_total_price() - self.get_discount()


    def clear(self):
        # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def __iter__(self):
        """
        Iterate over the items in the cart and get the products
        from the database.
        """
        product_ids = [key for key in self.cart.keys() if key != 'discount']
        print(product_ids)
        # get the product objects and add them to the cart
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
            cart[str(product.id)]['image'] = product.main_image
            cart[str(product.id)]['weight'] = product.weight
        for product_id, item in cart.items():
            if product_id == 'discount':
                pass
            else:
                item['price'] = int(item['price'])
                item['total_price'] = item['price'] * item['quantity']
                yield item

