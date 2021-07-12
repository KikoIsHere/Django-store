from django.forms import ModelForm
from django import forms
from .models import PromotionPacket, Product
from django.core.exceptions import ValidationError

class PromotionPacketForm(forms.ModelForm):
    class Meta:
        model = PromotionPacket
        fields = '__all__'

    def clean(self):
        products = self.cleaned_data.get('products')
        if products and products.count() > 5:
            raise ValidationError('Maximum five products are allowed.')

        return self.cleaned_data

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def clean(self):
        bought_together = self.cleaned_data.get('bought_together')
        related_products = self.cleaned_data.get('related_products')
        
        if bought_together and bought_together.count() > 5:
            raise ValidationError('Maximum five products are allowed.')

        if related_products and related_products.count() > 5:
            raise ValidationError('Maximum five products are allowed.')

        return self.cleaned_data