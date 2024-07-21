from django.urls import path
from .views import PostsByTag

urlpatterns = [
    path('', PostsByTag.as_view(), name='posts-by-tag-post'),
    path('<int:pk>/', PostsByTag.as_view(), name='posts-by-tag-get'),
]
