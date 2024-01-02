from django.urls import path
from blog import views

urlpatterns = [
    path(r"^$", views.PostListView.as_view(), name="post_list"),
    path(r"^about/$", views.AboutView.as_view(), name="about"),
    path(r"^post/(?P<pk>\d+)$", views.PostDetailView.as_view(), name="post_detail"),
    path(r"^post/new/$", views.PostCreateView.as_view(), name="post_new"),
    path(r"^post/(?P<pk>\d+)/edit/$", views.PostUpdateView.as_view(), name="post_edit"),
    path(r"^post/(?P<pk>\d+)/remove/$", views.PostDeleteView.as_view(), name="post_remove"),
    path(r"^drafts/$", views.DraftListView.as_view(), name="post_draft_list"),
]

