from django import forms
from .models import Coupon, Order
from django.core.validators import MinValueValidator, ValidationError

class CouponForm(forms.ModelForm):
    amount = forms.IntegerField(required=True,initial=1,validators=[MinValueValidator(1)])

    class Meta:
        model = Coupon
        fields = ("valid_from","valid_to","discount","is_active")

    def save(self, commit=True):
        for i in range(1,self.cleaned_data['amount']):
            extra = Coupon(
                valid_from=self.cleaned_data['valid_from'],
                valid_to=self.cleaned_data['valid_to'],
                discount=self.cleaned_data['discount'],
                is_active=self.cleaned_data['is_active']
            )
            extra.save()

        return super(CouponForm, self).save(commit=commit)
        
# class InformationForm(forms.Form):
#     name = forms.CharField(max_length=255, required=True)
#     email = forms.EmailField(required=True)
#     phone = forms.CharField(max_length=255, required=True)
#     adress = forms.CharField(max_length=255, required=True)
