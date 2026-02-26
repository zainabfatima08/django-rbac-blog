from django.urls import path
from django.contrib.auth import views as auth_views
from .views import AuthorRegisterView, ApproveAuthorView, PendingAuthorsListView
from django.views.generic import ListView

urlpatterns = [
    path("register/", AuthorRegisterView.as_view(), name = "register"),
    path("approve/<int:user_id>/", ApproveAuthorView.as_view(), name = "approve_list"),
    path("authors/", PendingAuthorsListView.as_view(), name = "author_list"),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

]
