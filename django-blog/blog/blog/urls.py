"""
URL configuration for blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from .view_single_post import SinglePostView
from .view_post import PostsView
from .view_posts_by_tag import PostsByTag
from .view_tags import TagsView, get_all_tags
from .view_comment import CommentView
from .view_like import LikeView
from .view_user_profile import UserProfileView
from .view_home import home_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path("posts/<int:pk>", PostsView.as_view(), name="post-details"),
    path("posts/", PostsView.as_view(), name="posts"),
    path("posts/new/", SinglePostView.as_view(), name="new-post"),
    path("like/", LikeView.as_view(), name="like"),    
    path("posts/<int:pk>/edit", SinglePostView.as_view(), name="edit-post"),
    path("comments/", CommentView.as_view(), name="all-comments"),
    path("comments/new/", CommentView.as_view(), name="new-comment"),
    path("tags/all-tags", get_all_tags, name='get-all-tags'),
    path("tags/", TagsView.as_view(), name="tags"),
    path("tags/new", TagsView.as_view(), name="new-tag"),
    path("posts/by-tag", PostsByTag.as_view(), name='posts-by-tag-post'),
    path('posts/by-tag/<int:pk>', PostsByTag.as_view(), name='posts-by-tag-get'),
    path("user-profile/", UserProfileView.as_view(), name="user-profile"),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path("", home_view, name="home"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
