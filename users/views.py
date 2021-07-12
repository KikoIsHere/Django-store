from django.shortcuts import render, redirect, HttpResponseRedirect, reverse
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
from django.views.generic.edit import FormView
from .forms import LegalAccountForm, LoginForm, AccountForm, PasswordResetForm, EditAccountForm, EditLegalAccountForm, EditUserForm
from .models import Account, User
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import update_session_auth_hash
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template, render_to_string
from django.contrib.sites.shortcuts import get_current_site
from .tokens import account_activation_token
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode    

def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home'))
    form = LoginForm()
    success = None
    if request.META.get('HTTP_REFERER') == request.build_absolute_uri('/auth/reset/Mw/set-password/'):
        success = True
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('home')
        else:
            print(form.errors)
    context = {
        'form':form,
        'success':success,
    }
    return render(request, 'pages/login.html', context)

def register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home'))
    normal_form = AccountForm()
    legal_form = LegalAccountForm()
    success = None

    if 'submit-legal' in request.POST:
        legal_form = LegalAccountForm(request.POST)
        print(request.POST)
        if legal_form.is_valid():
            user = legal_form.save()
            activation_email(request, user, legal_form.cleaned_data['email'])
            success = True        
        print(legal_form.errors)
    if 'submit-normal' in request.POST:
        normal_form = AccountForm(request.POST)
        if normal_form.is_valid():
            user = normal_form.save()    
            activation_email(request, user, normal_form.cleaned_data['email']) 
            success = True;
        print(normal_form.errors)

    context = {
        'normal_form':normal_form,
        'legal_form':legal_form,
        'success':success,
    }

    return render(request, 'pages/registration.html', context)


def activation_email(request, user, email):
    current_site = get_current_site(request)
    subject = 'Activate your account.'
    content = {
        'user':user,
        'domain': current_site.domain,
        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        'token':account_activation_token.make_token(user),
    }
    text_content = render_to_string('pages/email_template_registration_confirmation.html', content)
    htmly = get_template('pages/email_template_registration_confirmation.html')
    

    html_content = htmly.render(content)
    msg = EmailMultiAlternatives(subject, text_content, 'kristian.petrov@pytek.bg', [email])
    msg.attach_alternative(html_content, "text/html")
    print(msg)
    msg.send()


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


@login_required
def logout(request):
    auth_logout(request)
    return redirect('login')

@login_required
def myprofile_normal(request):
    if request.user.is_legal == True:
        return redirect('my-profile-legal')
    user = Account.objects.get(user=request.user)

    user_form = EditUserForm(user=request.user, initial={'username':user.user.username})
    account_form = EditAccountForm(instance=user, initial={
        'name': user.name,
        'email': user.user.email,
        'phone': user.phone,
        'club_card': user.club_card,
        'adress': user.adress,
        'city': user.city,
        'region': user.region,
        'zip_code': user.zip_code
    })
    success = None
    if "change-user" in request.POST:
        user_form = EditUserForm(user=request.user,data=request.POST)
        if user_form.is_valid():
            user_form.save()
            update_session_auth_hash(request, user_form.user)
            success = 'user-change'

    elif 'change-personal' in request.POST:
        account_form = EditAccountForm(request.POST, instance=user, )
        if account_form.is_valid():
            account_form.save()
            success = 'personal-change'

    context = {
        'success':success,
        'user_form':user_form,
        'account_form':account_form,
    }
    return render(request, 'pages/my-profile.html', context)


@login_required
def myprofile_legal(request):
    if request.user.is_normal == True:
        return redirect('my-profile-normal')
    user_form = EditUserForm(user=request.user, initial={'username':user.user.username})
    legal_form = EditLegalAccountForm(instance=user, initial={
        'name': user.name,
        'email': user.user.email,
        'phone': user.phone,
        'club_card': user.club_card,
        'adress': user.adress,
        'city': user.city,
        'region': user.region,
        'zip_code': user.zip_code,
        'mol': user.mol,
        'eik': user.eik,
        'dds_number': user.dds_number,
        'tax_address': user.tax_address,
        'delivery_adress': user.delivery_adress,
    })
    if "change-user" in request.POST:
        user_form = EditUserForm(user=request.user,data=request.POST)
        if user_form.is_valid():
            user_form.save()
            update_session_auth_hash(request, user_form.user)
            success = 'user-change'
    elif 'change-personal' in request.POST:
        legal_form = EditLegalAccountForm(request.POST, instance=user, )
        if legal_form.is_valid():
            legal_form.save()
            success = 'personal-change'
    else:
        success = None
    context = {
        'success':success,
        'user_form':user_form,
        'legal_form':legal_form,
    }
    return render(request, 'pages/my-profile.html', context)


class ExtendPasswordResetView(PasswordResetView):
    success = None
    def get_context_data(self, **kwargs,):
        context = super(ExtendPasswordResetView, self).get_context_data(**kwargs)
        context['success'] = self.success
        return context

