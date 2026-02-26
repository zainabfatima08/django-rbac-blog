from django.shortcuts import render, redirect, get_object_or_404
from .models import Post
from .forms import PostForm
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# Create your views here.

def is_admin(user):
    return user.is_staff

def is_author(user):
    return user.is_author and user.is_approved

# READ VIEW (list)

class PostListView(ListView):
    model = Post
    template_name = "posts/post_list.html"
    context_object_name = "posts"

# DETAIL VIEW
class PostDetailView(DetailView):
    model = Post
    template_name = "posts/post_detail.html"
    context_object_name = "post"

# CREATE VIEW
class PostCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "posts/post_form.html"
    success_url = reverse_lazy("post_list")

    def test_func(self):
        return is_admin(self.request.user) or is_author(self.request.user)
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

#UPDATE VIEW

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "posts/post_form.html"
    success_url = reverse_lazy("post_list")

    def test_func(self):  
        post = self.get_object()
        return self.request.user == post.author or self.request.user.is_staff

# DELETE VIEW

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):  # order fix kiya
    model = Post
    template_name = "posts/post_delete.html"
    success_url = reverse_lazy("post_list")

    def test_func(self):
        return self.request.user.is_staff