from django.urls import path
from .views import CommentView


urlpatterns = [
    path("", CommentView.as_view(), name="all-comments"),
    path("new", CommentView.as_view(), name="new-comment"),
]