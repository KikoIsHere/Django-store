from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import Account, LegalAccount, User

admin.site.register(User, UserAdmin)
@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    exclude = ['user']
    display_field = ['username','email','name']

@admin.register(LegalAccount)
class LegalAccountAdmin(admin.ModelAdmin):
    exclude = ['user']
    display_field = ['username','email','name']
