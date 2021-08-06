from django.contrib import admin
from .models import Product, ProductCategory, PromotionPacket, ProductCharacteristic, Manufacturer, ProductImage
from mptt.admin import MPTTModelAdmin
from .forms import PromotionPacketForm, ProductForm

class ProductCharacteristicInline(admin.TabularInline):
    model = ProductCharacteristic
    extra = 1


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    display_fields = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    display_fields = ['name']
    inlines = [ProductCharacteristicInline, ProductImageInline]

    def render_change_form(self, request, context, *args, kwargs):
        context['adminform'].form.fields['category'].queryset = ProductCategory.objects.filter(children__isnull=True)
        return super(ProductAdmin, self).render_change_form(request, context, *args, kwargs)


class MPTTModelAdmin(MPTTModelAdmin):

    def render_change_form(self, request, context, *args, kwargs):
        context['adminform'].form.fields['parent'].queryset = ProductCategory.objects.filter(level__lte=1)
        return super(MPTTModelAdmin, self).render_change_form(request, context, *args, kwargs)


@admin.register(PromotionPacket)
class PromotionPacketAdmin(admin.ModelAdmin):
    form = PromotionPacketForm
    display_fields = ['name']

admin.site.register(ProductCategory, MPTTModelAdmin)