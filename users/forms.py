from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import Account, User, LegalAccount
from django.contrib.auth import authenticate, login
from django.db import transaction
from django.contrib.auth.forms import AuthenticationForm

class AccountForm(UserCreationForm):
    name = forms.CharField(max_length=50)
    adress = forms.CharField(max_length=50,)
    region = forms.CharField(max_length=50,)
    city = forms.CharField(max_length=50,)
    zip_code = forms.CharField(max_length=50,) 
    phone = forms.CharField(max_length=50)
    club_card = forms.CharField(max_length=50, required=False)    

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "password1", "password2")

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_normal = True
        user.is_active = False
        user.save()
        Account.objects.create(
            user=user,
            name=self.cleaned_data['name'],
            adress=self.cleaned_data['adress'],
            region=self.cleaned_data['region'],
            city=self.cleaned_data['city'],
            zip_code=self.cleaned_data['zip_code'],
            phone=self.cleaned_data['phone'],
            club_card=self.cleaned_data['club_card'],
        )
        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Username'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Email'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirm Password'})
        self.fields['name'].widget.attrs.update({'placeholder': 'Name'})
        self.fields['adress'].widget.attrs.update({'placeholder': 'Adress'})
        self.fields['city'].widget.attrs.update({'placeholder': 'City'})
        self.fields['region'].widget.attrs.update({'placeholder': 'Region'})
        self.fields['zip_code'].widget.attrs.update({'placeholder': 'Zip Code'})
        self.fields['phone'].widget.attrs.update({'placeholder': 'Phone'})
        self.fields['club_card'].widget.attrs.update({'placeholder': 'Club Card'})


class LegalAccountForm(UserCreationForm):
    name = forms.CharField(max_length=50)
    adress = forms.CharField(max_length=50,)
    region = forms.CharField(max_length=50,)
    city = forms.CharField(max_length=50,)
    zip_code = forms.CharField(max_length=50,) 
    phone = forms.CharField(max_length=50)
    club_card = forms.CharField(max_length=50, required=False)    
    mol = forms.CharField(max_length=50)
    eik = forms.CharField(max_length=50)
    dds_number = forms.CharField(max_length=50)
    tax_address = forms.CharField(max_length=50) 

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "password1", "password2")

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_legal = True
        user.is_active = False
        user.save()
        LegalAccount.objects.create(
            user=user,
            name=self.cleaned_data['name'],
            adress=self.cleaned_data['adress'],
            region=self.cleaned_data['region'],
            city=self.cleaned_data['city'],
            zip_code=self.cleaned_data['zip_code'],
            phone=self.cleaned_data['phone'],
            club_card=self.cleaned_data['club_card'],
            mol=self.cleaned_data['mol'],
            eik=self.cleaned_data['eik'],
            dds_number=self.cleaned_data['dds_number'],
            tax_address=self.cleaned_data['tax_address'],       
        )
        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'id':'legal_username','placeholder': 'Username'})
        self.fields['email'].widget.attrs.update({'id':'legal_email','placeholder': 'Email'})
        self.fields['password1'].widget.attrs.update({'id':'legal_password1','placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'id':'legal_password2','placeholder': 'Confirm Password'})
        self.fields['name'].widget.attrs.update({'id':'legal_name','placeholder': 'Name'})
        self.fields['adress'].widget.attrs.update({'id':'legal_adress','placeholder': 'Adress'})
        self.fields['city'].widget.attrs.update({'id':'legal_city','placeholder': 'City'})
        self.fields['region'].widget.attrs.update({'id':'legal_region','placeholder': 'Region'})
        self.fields['zip_code'].widget.attrs.update({'id':'legal_zip_code','placeholder': 'Zip Code'})
        self.fields['phone'].widget.attrs.update({'id':'legal_phone','placeholder': 'Phone'})
        self.fields['club_card'].widget.attrs.update({'id':'legal_club_card','placeholder': 'Club Card'})

        self.fields['mol'].widget.attrs.update({'placeholder': 'MOL'})
        self.fields['eik'].widget.attrs.update({'placeholder': 'EIK'})
        self.fields['dds_number'].widget.attrs.update({'placeholder': 'DDS Number'})
        self.fields['tax_address'].widget.attrs.update({'placeholder': 'Tax Adress'})


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Username'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Password'})


class PasswordResetForm(forms.Form):
    email = forms.CharField(max_length=255, required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'placeholder': 'Email'})


class EditUserForm(PasswordChangeForm):
    username = forms.CharField(max_length=255, required=True)

    def __init__(self, user, *args, **kwargs):
        super(EditUserForm, self).__init__(user, *args, **kwargs)
        self.user = user
        self.fields['username'].widget.attrs.update({'placeholder': 'Username'})
        self.fields['old_password'].widget.attrs.update({'placeholder': 'Old Password'})
        self.fields['new_password1'].widget.attrs.update({'placeholder': 'New Password'})
        self.fields['new_password2'].widget.attrs.update({'placeholder': 'Confirm New Password'})

    def save(self, commit=True):
        username = self.cleaned_data["username"]
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        self.username = username
        if commit:
            self.user.save()
        return self.user

class EditAccountForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = Account
        exclude = ['user',]


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'placeholder': 'Name'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Email'})
        self.fields['adress'].widget.attrs.update({'placeholder': 'Adress'})
        self.fields['city'].widget.attrs.update({'placeholder': 'City'})
        self.fields['region'].widget.attrs.update({'placeholder': 'Region'})
        self.fields['zip_code'].widget.attrs.update({'placeholder': 'Zip Code'})
        self.fields['phone'].widget.attrs.update({'placeholder': 'Phone'})
        self.fields['club_card'].widget.attrs.update({'placeholder': 'Club Card', 'required': 'false' })


class EditLegalAccountForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = Account
        exclude = ['user',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'placeholder': 'Name'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Email'})
        self.fields['adress'].widget.attrs.update({'placeholder': 'Adress'})
        self.fields['city'].widget.attrs.update({'placeholder': 'City'})
        self.fields['region'].widget.attrs.update({'placeholder': 'Region'})
        self.fields['zip_code'].widget.attrs.update({'placeholder': 'Zip Code'})
        self.fields['phone'].widget.attrs.update({'placeholder': 'Phone'})
        self.fields['club_card'].widget.attrs.update({'placeholder': 'Club Card'})

        self.fields['mol'].widget.attrs.update({'placeholder': 'MOL'})
        self.fields['eik'].widget.attrs.update({'placeholder': 'EIK'})
        self.fields['dds_number'].widget.attrs.update({'placeholder': 'DDS Number'})
        self.fields['tax_address'].widget.attrs.update({'placeholder': 'Tax Adress'})