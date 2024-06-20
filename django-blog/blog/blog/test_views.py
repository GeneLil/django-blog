"""Module for views testing"""
import json
from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from accounts.models import CustomUser
from .models import Post, Like, Comment, Tag


class HomePageViewTest(TestCase):
    """Class for home page view testing"""

    def setUp(self) -> None:
        """Set up"""
        self.client = Client()
        user = CustomUser.objects.create(username='john')
        user.set_password('12345')
        user.save()
        return super().setUp()

    def test_redirects_not_logged_user_to_login(self):
        """Test redirection of non-logged user"""
        response = self.client.get("")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url='/accounts/login/')

    def test_redirects_logged_user_to_posts(self):
        """Test redirection of logged user"""
        self.client.login(username='john', password='12345')
        response = self.client.get('')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url='/posts/')


class LikeViewTest(TestCase):
    """Class for like view testing"""

    def setUp(self) -> None:
        """Set up"""
        self.client = Client()
        user = CustomUser.objects.create(pk=1, username='john')
        user.set_password('12345')
        user.save()
        Post.objects.create(pk=1, title='post', body='blah blah blah', author_id=1)
        return super().setUp()

    def test_like_is_created(self):
        """Test creation of Like instance"""
        self.client.login(username='john', password='12345')
        path = reverse('like-post', kwargs={'post_id': 1})
        response = self.client.post(path)
        self.assertEqual(response.status_code, 302)
        like = Like.objects.get(post_id=1, user_id=1)
        self.assertEqual(like.user.pk, 1)
        self.assertEqual(like.post.pk, 1)


class CommentViewTest(TestCase):
    """Class for comment view testing"""

    def setUp(self) -> None:
        """Set up"""
        self.client = Client()
        user = CustomUser.objects.create(pk=1, username='john')
        user.set_password('12345')
        user.save()
        Post.objects.create(pk=1, title='post', body='blah blah blah', author_id=1)
        return super().setUp()

    def test_comment_is_created(self):
        """Test creation of Comment instance"""
        self.client.login(username='john', password='12345')
        path = reverse('new-comment')
        response = self.client.post(path, data={'post_id': 1, 'body': 'Some comment'})
        self.assertEqual(response.status_code, 200)
        comment = Comment.objects.get(post_id=1, author_id=1)
        self.assertEqual(comment.author.pk, 1)
        self.assertEqual(comment.post.pk, 1)


class PostViewTest(TestCase):
    """Class for single post view testing"""

    def setUp(self) -> None:
        """Set up"""
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        post_image = SimpleUploadedFile('small.gif', small_gif, content_type='image/gif')

        self.client = Client()
        user = CustomUser.objects.create(pk=1, username='john')
        CustomUser.objects.create(pk=2, username='jane')
        user.set_password('12345')
        user.save()
        post1 = Post.objects.create(pk=1, title='post1',
                                    body='blah blah blah',
                                    author_id=1,
                                    image=post_image)
        post2 = Post.objects.create(pk=2, title='post2',
                                    body='blah blah blah',
                                    author_id=2,
                                    image=post_image)
        post3 = Post.objects.create(pk=3, title='post3',
                                    body='blah blah blah',
                                    author_id=1, image=post_image)
        tag1 = Tag.objects.create(pk=1, title="family")
        tag2 = Tag.objects.create(pk=2, title="adventure")
        tag3 = Tag.objects.create(pk=3, title="cats")
        post1.tags.set([tag1, tag2])
        post2.tags.set([tag2])
        post3.tags.set([tag1, tag3])
        post1.save()
        post2.save()
        post3.save()
        return super().setUp()

    def test_user_can_edit_post(self):
        """Test if user who created the post can edit it"""
        self.client.login(username='john', password='12345')
        path = reverse('post-details', kwargs={'pk': 1})
        response = self.client.get(path)
        self.assertEqual(response.context['can_edit_post'], True)

        path = reverse('post-details', kwargs={'pk': 2})
        response = self.client.get(path)
        self.assertEqual(response.context['can_edit_post'], False)

    def test_post_is_liked_by_user(self):
        """Test if post is correctly liked by user"""
        self.client.login(username='john', password='12345')
        path = reverse('like-post', kwargs={'post_id': 1})
        self.client.post(path)

        path = reverse('post-details', kwargs={'pk': 1})
        response = self.client.get(path)
        self.assertEqual(response.context['is_liked'], True)

    def test_show_posts_liked_by_user(self):
        """Test that url shows posts liked by user"""
        self.client.login(username='john', password='12345')
        like_1 = reverse('like-post', kwargs={'post_id': 1})
        self.client.post(like_1)
        like_2 = reverse('like-post', kwargs={'post_id': 2})
        self.client.post(like_2)

        posts_path = reverse('posts')
        response = self.client.get(posts_path)

        self.assertEqual(len(response.context['posts_liked_by_user']), 2)

    def test_search_post_by_tag_name(self):
        """Test search posts by tag name result"""
        self.client.login(username='john', password='12345')
        path = reverse('posts-by-tag-post')
        response = self.client.post(path,
                                    data=json.dumps({'tagTitle': 'family'}),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)
        response_content = response.content
        self.assertJSONEqual(str(response_content, encoding='utf8'), { 'posts': [
            {'id': 1, 'tags': ['family', 'adventure'], 'title': 'post1'},
            {'id': 3, 'tags': ['family', 'cats'], 'title': 'post3'}
        ] })
        
    def test_get_all_tags(self):
        """Test getting all tags"""
        self.client.login(username='john', password='12345')
        path = reverse('get-all-tags')
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)
        response_content = response.content
        self.assertJSONEqual(str(response_content, encoding='utf8'), { 'tags': [
            { 'id': 1, 'title': 'family' },
            { 'id': 2, 'title': 'adventure' },
            { 'id': 3, 'title': 'cats' }
        ] })
