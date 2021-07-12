from django.db import models
from products.models import Product
from users.models import Account
from django.shortcuts import reverse
import string
import secrets
# class ClubCard(models.Model):
#     code = models.CharField(max_length=50)
#     discount = models.IntegerField()

#     class Meta:
#         verbose_name = "Club Card"
#         verbose_name_plural = "Club Cards"

#     def __str__(self):
#         return self.name


class Coupon(models.Model):
    STATUS_CHOICES = [
        ('generated', 'Generated'),
        ('exported', 'Exported'),
        ('claimed', 'Claimed'),
    ]

    code = models.CharField(max_length=20,unique=True, blank=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    is_active = models.BooleanField()

    class Meta:
        verbose_name = "Coupon"
        verbose_name_plural = "Coupons"

    def save(self, *args, **kwargs):
        if self.code is None or self.code == "":
            alphabet = string.ascii_letters + string.digits
            self.code = ''.join(secrets.choice(alphabet) for i in range(20))
        super(Coupon, self).save(*args, **kwargs)

    def __str__(self):
        return self.code
    

class Order(models.Model):
    number = models.IntegerField()
    date = models.DateField()
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    price = models.IntegerField()
    discount = models.IntegerField()
    delivery_price = models.IntegerField()
    final_price = models.IntegerField()
    payment_status = models.CharField(max_length=50)
    progress_status = models.CharField(max_length=50)
    delivery_status = models.CharField(max_length=50)
    down_payment = models.IntegerField()
    amount_payments = models.IntegerField()
    
    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self):
        return self.number

    def get_absolute_url(self):
        return reverse("Order_detail", kwargs={"pk": self.pk})

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    item = models.ForeignKey(Product,on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.IntegerField()

