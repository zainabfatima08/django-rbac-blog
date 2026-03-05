from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment, Like
from .forms import PostForm, CommentForm
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, View
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator

def is_admin(user):
    return user.is_staff

def is_author(user):
    return user.is_author and user.is_approved

def get_posts_for_users(user):
    if user.is_authenticated and user.is_staff:
        return Post.objects.all().order_by('-created_at')
    elif user.is_authenticated and user.is_author:
        return Post.objects.filter(
            Q(author=user) | Q(status='Published')
        ).distinct().order_by('-created_at')
    else:
        return Post.objects.filter(status='Published').order_by('-created_at')


# LIST VIEW
class PostListView(View):
    template_name = "posts/post_list.html"

    def get(self, request):
        posts = get_posts_for_users(request.user)
        search_query = request.GET.get('search', '')

        if search_query:
            posts = posts.filter(
                Q(topic__icontains=search_query) |
                Q(article__icontains=search_query)
            ).distinct()

        paginator = Paginator(posts, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, self.template_name, {
            'posts'        : page_obj,
            'page_obj'     : page_obj,
            'search_query' : search_query,
        })


# SEARCH SUGGESTIONS VIEW
class SearchSuggestionsView(View):

    def get(self, request):
        query = request.GET.get('search', '')
        suggestions = []

        if query:
            posts = get_posts_for_users(request.user).filter(
                topic__icontains=query
            )[:5]
            suggestions = [
                {'slug': post.slug, 'topic': post.topic}
                for post in posts
            ]

        return JsonResponse({'suggestions': suggestions})


# DETAIL VIEW
class PostDetailView(DetailView):
    model = Post
    template_name = "posts/post_detail.html"
    context_object_name = "post"
    slug_field = 'slug'          # ✅ model mein slug field
    slug_url_kwarg = 'slug'      # ✅ URL mein slug keyword

    def get_queryset(self):
        return get_posts_for_users(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context['comments'] = post.comments.all().order_by('-created_at')
        context['comment_form'] = CommentForm()
        context['like_count'] = post.likes.count()
        context['user_liked'] = post.likes.filter(user=self.request.user).exists() if self.request.user.is_authenticated else False
        return context


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
        form.instance.status = 'Draft'
        messages.success(self.request, "Post saved as Draft!")
        return super().form_valid(form)


# UPDATE VIEW
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "posts/post_form.html"
    success_url = reverse_lazy("post_list")
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author or self.request.user.is_staff


# DELETE VIEW
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "posts/post_delete.html"
    success_url = reverse_lazy("post_list")
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def test_func(self):
        return self.request.user.is_staff


# PUBLISH VIEW
class PostPublishView(LoginRequiredMixin, UserPassesTestMixin, View):

    def test_func(self):
        post = get_object_or_404(Post, slug=self.kwargs['slug'])
        return self.request.user.is_staff or self.request.user == post.author

    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        post.status = 'Published'
        post.save()
        messages.success(request, f'"{post.topic}" has been published!')
        return redirect('post_list')


# UNPUBLISH VIEW
class PostUnpublishView(LoginRequiredMixin, UserPassesTestMixin, View):

    def test_func(self):
        return self.request.user.is_staff

    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        post.status = 'Draft'
        post.save()
        messages.success(request, f'"{post.topic}" has been unpublished!')
        return redirect('post_list')


# COMMENT CREATE VIEW
class CommentCreateView(LoginRequiredMixin, View):

    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, "Comment successfully added!")
        return redirect('post_detail', slug=slug)


# COMMENT DELETE VIEW
class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, View):

    def test_func(self):
        comment = get_object_or_404(Comment, pk=self.kwargs['pk'])
        return self.request.user.is_staff or self.request.user == comment.post.author

    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        post_slug = comment.post.slug   # pk ki jagah slug save karo
        comment.delete()
        messages.success(request, "Comment deleted successfully!")
        return redirect('post_detail', slug=post_slug)


# LIKE TOGGLE VIEW
class LikeToggleView(LoginRequiredMixin, View):

    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        like = post.likes.filter(user=request.user)

        if like.exists():
            like.delete()
            liked = False
        else:
            Like.objects.create(user=request.user, post=post)
            liked = True

        return JsonResponse({
            'liked'     : liked,
            'like_count': post.likes.count()
        })


# AUTHOR DASHBOARD VIEW
class AdminDashboardView(LoginRequiredMixin, UserPassesTestMixin, View):

    def test_func(self):
        return is_author(self.request.user) or is_admin(self.request.user)

    def get(self, request):
        posts = Post.objects.filter(author=request.user)

        total_posts     = posts.count()
        draft_posts     = posts.filter(status='Draft').count()
        published_posts = posts.filter(status='Published').count()
        total_likes     = Like.objects.filter(post__author=request.user).count()
        total_comments  = Comment.objects.filter(post__author=request.user).count()
        recent_posts    = posts.order_by('-created_at')[:5]

        return render(request, 'posts/dashboard.html', {
            'total_posts'    : total_posts,
            'draft_posts'    : draft_posts,
            'published_posts': published_posts,
            'total_likes'    : total_likes,
            'total_comments' : total_comments,
            'recent_posts'   : recent_posts,
        })