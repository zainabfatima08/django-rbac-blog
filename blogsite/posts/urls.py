from django.urls import path
from .views import (
    PostCreateView, PostListView, 
    PostUpdateView, PostDeleteView,
    PostDetailView, PostPublishView, 
    PostUnpublishView,CommentCreateView,
    CommentDeleteView, LikeToggleView,
    AdminDashboardView, SearchSuggestionsView
)

urlpatterns = [
    path("read/", PostListView.as_view(), name="post_list"),
    path("read/<slug:slug>/", PostDetailView.as_view(), name="post_detail"),
    path("create/", PostCreateView.as_view(), name="post_create"),
    path("update/<slug:slug>/", PostUpdateView.as_view(), name="post_update"),
    path("delete/<slug:slug>/", PostDeleteView.as_view(), name="post_delete"),
    path("publish/<slug:slug>/", PostPublishView.as_view(), name = 'post_publish'),
    path("unpublish/<slug:slug>", PostUnpublishView.as_view(), name = "post_unpublish"),
    path("comment/<slug:slug>/add/", CommentCreateView.as_view(), name = 'comment_add'),
    path("comment/<slug:slug>/delete/", CommentDeleteView.as_view(), name = 'comment_delete'),
    path("like/<slug:slug>/", LikeToggleView.as_view(), name = "like_toggle"),
    path("dashboard/", AdminDashboardView.as_view(), name = "dashboard"),
    path("suggestions/", SearchSuggestionsView.as_view(), name="search_suggestions"),
]