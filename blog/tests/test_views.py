from django.test import TestCase
from django.urls import reverse
from blog.models import Post


class PostListTestCause(TestCase):
    def setUp(self):
        Post.objects.create(text='this is test')

    def test_view_url_by_name(self):
        resp = self.client.get(reverse('post-list'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('post-list'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'blog/post_list.html')