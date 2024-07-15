from django.urls import path
from .views import TagsView, get_all_tags


urlpatterns = [
    path('', TagsView.as_view(), name="tags"),
    path('all', get_all_tags, name='get-all-tags'),
    path('new', TagsView.as_view(), name="new-tag"),
]