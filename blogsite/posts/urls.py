from django.urls import path
from .views import PostCreateView, PostListView, PostUpdateView, PostDeleteView, PostDetailView  # PostDetailView add kiya

urlpatterns = [
    path("read/", PostListView.as_view(), name="post_list"),
    path("read/<int:pk>/", PostDetailView.as_view(), name="post_detail"),  # yeh add kiya
    path("create/", PostCreateView.as_view(), name="post_create"),
    path("update/<int:pk>/", PostUpdateView.as_view(), name="post_update"),
    path("delete/<int:pk>/", PostDeleteView.as_view(), name="post_delete"),
]