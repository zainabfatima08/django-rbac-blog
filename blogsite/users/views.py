from django.shortcuts import render, redirect, get_object_or_404
from .forms import AuthorRegistrationForm
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.views.generic import CreateView, View, ListView
from django.urls import reverse_lazy
from django.contrib import messages
from django.conf import settings

# Create your views here.
User = get_user_model()


class AuthorRegisterView(CreateView):
    model = User
    form_class = AuthorRegistrationForm
    template_name = "users/register.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object

        send_mail(
            "New Author Approval Request",
            f"Please approve author: {user.username}\n\nApprove link: http://127.0.0.1:8000/users/approve/{user.id}/",
            settings.EMAIL_HOST_USER,
            [settings.EMAIL_HOST_USER]
        )
        messages.success(self.request, "Registration successful! Wait for admin approval.")
        return response


class ApproveAuthorView(View):
    def get(self, request, user_id):
        if not request.user.is_staff:
            messages.error(request, "Only admin can approve authors!")
            return redirect("home")
        
        user = get_object_or_404(User, id=user_id)

        if user.is_approved:
            messages.warning(request, f"{user.username} is already approved.")
        else:
            user.is_active = True
            user.is_approved = True
            user.save()

            send_mail(
                "Account Approved",
                "Your Author Account is approved. Now You can login!",
                settings.EMAIL_HOST_USER, 
                [user.email]
            )
            messages.success(request, f"{user.username}'s account has been approved successfully!")

        return redirect("author_list")

    
class PendingAuthorsListView(ListView):
    model = User
    template_name = "users/author_list.html"
    context_object_name = "authors"

    def get_queryset(self): 
        return User.objects.filter(is_approved = False, is_author = True)





