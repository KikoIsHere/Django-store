from django.contrib import admin
from .models import Order, OrderItem
from .models import Coupon
from .forms import CouponForm
from import_export.admin import ImportExportModelAdmin

@admin.register(Coupon)
class CouponAdmin(ImportExportModelAdmin):
    list_display = ['code','valid_from','valid_to','discount','status','is_active']
    list_filter = ['is_active','valid_from','valid_to']
    search = ['code']
    form = CouponForm

    
class OrderItemInline(admin.TabularInline):
    model = OrderItem

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    display_field = ['number']
    inlines = [OrderItemInline]
