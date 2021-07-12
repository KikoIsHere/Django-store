from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views
from django.http import HttpResponse


urlpatterns = [
    path('login',views.login, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout, name='logout'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),

    path('my-profile', views.myprofile_normal, name='my-profile-normal'),
    path('my-profile-legal', views.myprofile_legal, name='my-profile-legal'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='pages/change-password.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    path('password_reset/', views.ExtendPasswordResetView.as_view(
        template_name='pages/forgotten-password.html',
        html_email_template_name='pages/email_template_pass_reset.html',
        from_email='kristian.petrov@pytek.bg',
        success_url=reverse_lazy('password_reset_done'),
        ),name='password_reset'),

    path('password_reset/done/', views.ExtendPasswordResetView.as_view(
        template_name='pages/forgotten-password.html',
        success=True
        ),name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='pages/change-password.html',
        success_url=reverse_lazy('login'),
        ),name='password_reset_confirm'),  
]
