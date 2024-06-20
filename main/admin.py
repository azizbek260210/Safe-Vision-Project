from django.contrib import admin
from . import models
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django import forms
from .models import CustomUser
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .forms import UserCreationForm, UserChangeForm


class CustomUserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('phone','id', 'username','confirm', 'first_name', 'last_name', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('phone', 'username', 'first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'confirm', 'first_name', 'last_name')}
        ),
    )
    search_fields = ('phone', 'username', 'first_name', 'last_name')
    ordering = ('phone',)
    filter_horizontal = ()

    def save_model(self, request, obj, form, change):
        if 'code' in form.cleaned_data:
            # Process SMS code here
            pass  # Replace with actual SMS verification code
        obj.save()

admin.site.register(CustomUser, CustomUserAdmin)

admin.site.register(models.Banner)
admin.site.register(models.Product)
admin.site.register(models.Category)
admin.site.register(models.SubCategory)
admin.site.register(models.ProductImage)
# admin.site.register(models.ProductVideo)
admin.site.register(models.Cart)
admin.site.register(models.CartProduct)
admin.site.register(models.WishList)
# admin.site.register(models.EnterProduct)
