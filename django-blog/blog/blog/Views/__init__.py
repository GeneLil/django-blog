"""Views module entrypoint"""
from .home import home_view
from .like import LikeView
from .new_comment import NewCommentView
from .posts import PostsView, get_posts_by_tag_search
from .single_post import SinglePostView
from .tags import TagsView, get_all_tags
from .user_profile import UserProfileView
