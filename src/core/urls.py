from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('posts', views.PostViewSet, basename='posts')

urlpatterns = [
    path('', include(router.urls), name="posts_vs"),
    path('tags/', views.TagView.as_view(), name="tags"),
    path('tags/<slug:tag_slug>/', views.TagDetailView.as_view(), name="posts_by_tag"),
    path('aside/', views.AsideView.as_view(), name="aside_posts"),
    path('feedback/', views.FeedBackView.as_view(), name="feedback"),
    path('register/', views.RegisterView.as_view(), name="register"),
    path('profile/', views.ProfileView.as_view(), name="profile"),
    path('comments/<slug:post_slug>/', views.CommentView.as_view(), name="post_comments"),
]
