
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model

User = get_user_model()

class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):

        email = sociallogin.account.extra_data.get("email")
        if not email:
            return
        
        if not sociallogin.is_existing:
            try:
                existing_user = User.objects.get(email=email)
                sociallogin.connect(request, existing_user)
            except User.DoesNotExist:
                pass

    def save_user(self, request, sociallogin, form=None):
    
        user = super().save_user(request, sociallogin, form)
        email = user.email
        if email:
            email_address, created = EmailAddress.objects.get_or_create(
                user=user,
                email=email
            )
            if not email_address.verified:
                email_address.verified = True
                email_address.save()
        return user
