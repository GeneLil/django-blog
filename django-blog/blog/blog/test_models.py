"""Module for models testing"""
from django.test import TestCase
from accounts.models import CustomUser
from .models import Post, Tag


class ModelsTestCase(TestCase):
    """Class for testing models"""
    def setUp(self) -> None:
        """Setting up conf"""
        CustomUser.objects.create(pk=1, username='john')
        CustomUser.objects.create(pk=2, username='jane')
        Tag.objects.create(title='first')
        Tag.objects.create(title='second')
        Post.objects.create(title='post', body='blah blah blah', author_id=1)
        return super().setUp()

    def test_getting_tags_titles_for_post(self):
        """Testing function for getting tag titles for post"""
        post = Post.objects.get(title='post')
        tag1 = Tag.objects.get(title='first')
        tag2 = Tag.objects.get(title='second')
        post.tags.set([tag1, tag2])
        self.assertEqual(post.get_tags_names(), ['first', 'second'])

    def test_getting_usernames_who_liked_post(self):
        """Testing function for getting user names who liked the post"""
        post = Post.objects.get(title='post')
        john = CustomUser.objects.get(username='john')
        jane = CustomUser.objects.get(username='jane')
        post.liked_by.set([john, jane])
        self.assertEqual(post.serialized_liked_by(), ['john', 'jane'])
        