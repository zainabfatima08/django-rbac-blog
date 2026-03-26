from django.urls import path
from django.contrib.auth import views as auth_views
from .views import AuthorRegisterView, ApproveAuthorView, PendingAuthorsListView, AuthorProfileView,PrivacyView, TermsView, DeleteDataView, SocialLogoutView
from django.views.generic import ListView

urlpatterns = [
    path("register/", AuthorRegisterView.as_view(), name = "register"),
    path("approve/<int:user_id>/", ApproveAuthorView.as_view(), name = "approve_list"),
    path("authors/", PendingAuthorsListView.as_view(), name = "author_list"),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('author/<str:username>', AuthorProfileView.as_view(), name = "author_profile"),
]
