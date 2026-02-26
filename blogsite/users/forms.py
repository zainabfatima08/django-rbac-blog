from django import forms
from .models import CustomUser

class AuthorRegistrationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields =['username', 'email', 'password']

    def save(self, commit = True):
        user = super().save(commit = False)
        user.set_password(self.cleaned_data['password'])
        user.is_author = True
        user.is_active = False
        if commit:
            user.save()
            return user
            