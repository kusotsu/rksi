from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import BlogPost


class BlogPostTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.author = user_model.objects.create_user(username="author", password="strong-pass-123")
        self.other = user_model.objects.create_user(username="reader", password="strong-pass-123")
        self.old_post = BlogPost.objects.create(owner=self.author, title="Старая запись", text="Первый текст")
        self.new_post = BlogPost.objects.create(owner=self.author, title="Новая запись", text="Второй текст")
        BlogPost.objects.filter(id=self.old_post.id).update(date_added=timezone.now() - timedelta(days=1))

    def test_home_is_public_and_newest_post_is_first(self):
        response = self.client.get(reverse("blogs:index"))
        self.assertEqual(response.status_code, 200)
        posts = list(response.context["posts"])
        self.assertEqual(posts, [self.new_post, self.old_post])
        self.assertContains(response, "Новая запись")

    def test_empty_state_is_visible(self):
        BlogPost.objects.all().delete()
        response = self.client.get(reverse("blogs:index"))
        self.assertContains(response, "Публикаций пока нет")

    def test_anonymous_user_cannot_open_create_form(self):
        response = self.client.get(reverse("blogs:new_post"))
        self.assertRedirects(response, f"{reverse('users:login')}?next={reverse('blogs:new_post')}")

    def test_create_assigns_current_user_and_ignores_owner_input(self):
        self.client.force_login(self.other)
        response = self.client.post(
            reverse("blogs:new_post"),
            {"title": "Моя публикация", "text": "Содержимое", "owner": self.author.id},
        )
        self.assertRedirects(response, reverse("blogs:index"))
        self.assertEqual(BlogPost.objects.get(title="Моя публикация").owner, self.other)

    def test_author_can_edit_own_post(self):
        self.client.force_login(self.author)
        response = self.client.post(
            reverse("blogs:edit_post", args=[self.old_post.id]),
            {"title": "Исправленный заголовок", "text": "Исправленный текст", "owner": self.other.id},
        )
        self.assertRedirects(response, reverse("blogs:post_detail", args=[self.old_post.id]))
        self.old_post.refresh_from_db()
        self.assertEqual(self.old_post.title, "Исправленный заголовок")
        self.assertEqual(self.old_post.owner, self.author)

    def test_other_user_cannot_edit_post_and_sees_no_edit_link(self):
        self.client.force_login(self.other)
        page = self.client.get(reverse("blogs:index"))
        self.assertNotContains(page, reverse("blogs:edit_post", args=[self.old_post.id]))
        response = self.client.post(
            reverse("blogs:edit_post", args=[self.old_post.id]),
            {"title": "Взлом", "text": "Чужое изменение"},
        )
        self.assertEqual(response.status_code, 404)
        self.old_post.refresh_from_db()
        self.assertEqual(self.old_post.title, "Старая запись")

    def test_missing_post_returns_404(self):
        self.client.force_login(self.author)
        self.assertEqual(self.client.get(reverse("blogs:edit_post", args=[999999])).status_code, 404)


class UserFlowTests(TestCase):
    def test_registration_creates_and_logs_in_user(self):
        response = self.client.post(
            reverse("users:register"),
            {"username": "new-author", "password1": "Strong-pass-987", "password2": "Strong-pass-987"},
        )
        self.assertRedirects(response, reverse("blogs:index"))
        self.assertTrue(get_user_model().objects.filter(username="new-author").exists())
        self.assertIn("_auth_user_id", self.client.session)

    def test_logout_allows_post_only(self):
        user = get_user_model().objects.create_user(username="logout-user", password="strong-pass-123")
        self.client.force_login(user)
        self.assertEqual(self.client.get(reverse("users:logout")).status_code, 405)
        response = self.client.post(reverse("users:logout"))
        self.assertRedirects(response, reverse("blogs:index"))
        self.assertNotIn("_auth_user_id", self.client.session)

