from django import forms
from .models import CustomUser


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, except password."""

    class Meta:
        model = CustomUser
        fields = ('phone', 'confirm', 'first_name', 'last_name')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_unusable_password()  # Set an unusable password
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field."""
    password = None

    class Meta:
        model = CustomUser
        fields = ('phone', 'username', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser')
