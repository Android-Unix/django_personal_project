from django.contrib import admin
from account.models import Account
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.admin import UserAdmin
from account.forms import UserCreationForm, CustomUserChangeForm
from django.contrib.auth.forms import ReadOnlyPasswordHashField
  
class CustomUserAdmin(UserAdmin):
  
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password', 'is_active', 'is_staff')}),
        ('Permissions', {'fields': ('user_permissions',)}),
    )
    

    add_fieldsets = (
        (None, {
            'classes': ('wide'),
            'fields': ('first_name', 'last_name', 'username', 'email', 'dob', 'password1', 'password2')}
        ),
    )
    search_fields = ('email', 'username')
    ordering = ('email',)  

    form = CustomUserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

admin.site.register(Account, CustomUserAdmin)