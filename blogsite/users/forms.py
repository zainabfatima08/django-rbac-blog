from django import forms
from .models import CustomUser

class AuthorRegistrationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields =['username', 'email', 'password']

        def save(self, commit = True):
            user = super().save(commit = False)
            user.is_author = True
            user.is_active = False
            if commit:
                user.save()
                return user
            