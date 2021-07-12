from django.contrib import admin
from .models import Product, ProductCategory, PromotionPacket, ProductCharacteristic
from mptt.admin import MPTTModelAdmin
from .forms import PromotionPacketForm

class ProductCharacteristicAdmin(admin.TabularInline):
    model = ProductCharacteristic

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    display_fields = ['name']
    inlines = [ProductCharacteristicAdmin]

@admin.register(PromotionPacket)
class PromotionPacketAdmin(admin.ModelAdmin):
    form = PromotionPacketForm
    display_fields = ['name']

admin.site.register(ProductCategory, MPTTModelAdmin)