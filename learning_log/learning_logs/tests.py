from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Entry, Topic


class LearningLogTests(TestCase):
    def setUp(self):
        users = get_user_model()
        self.owner = users.objects.create_user(username="owner", password="strong-pass-123")
        self.other = users.objects.create_user(username="other", password="strong-pass-123")
        self.topic = Topic.objects.create(text="Python", owner=self.owner)
        self.other_topic = Topic.objects.create(text="Чужая тема", owner=self.other)
        self.entry = Entry.objects.create(topic=self.topic, text="Первоначальная запись")

    def test_index_is_public_and_private_pages_require_login(self):
        self.assertEqual(self.client.get(reverse("learning_logs:index")).status_code, 200)
        protected = [
            reverse("learning_logs:topics"),
            reverse("learning_logs:topic", args=[self.topic.id]),
            reverse("learning_logs:new_topic"),
            reverse("learning_logs:new_entry", args=[self.topic.id]),
            reverse("learning_logs:edit_entry", args=[self.entry.id]),
        ]
        for url in protected:
            with self.subTest(url=url):
                self.assertRedirects(self.client.get(url), f"{reverse('users:login')}?next={url}")

    def test_topics_list_contains_only_current_users_topics(self):
        self.client.force_login(self.owner)
        response = self.client.get(reverse("learning_logs:topics"))
        self.assertContains(response, "Python")
        self.assertNotContains(response, "Чужая тема")

    def test_new_topic_assigns_current_user_and_ignores_owner_input(self):
        self.client.force_login(self.owner)
        response = self.client.post(
            reverse("learning_logs:new_topic"),
            {"text": "Django", "owner": self.other.id},
        )
        self.assertRedirects(response, reverse("learning_logs:topics"))
        self.assertEqual(Topic.objects.get(text="Django").owner, self.owner)

    def test_topic_page_rejects_other_owner_and_missing_id(self):
        self.client.force_login(self.owner)
        self.assertEqual(
            self.client.get(reverse("learning_logs:topic", args=[self.other_topic.id])).status_code,
            404,
        )
        self.assertEqual(
            self.client.get(reverse("learning_logs:topic", args=[999999])).status_code,
            404,
        )

    def test_new_entry_is_saved_to_own_topic(self):
        self.client.force_login(self.owner)
        response = self.client.post(
            reverse("learning_logs:new_entry", args=[self.topic.id]), {"text": "Новая запись"}
        )
        self.assertRedirects(response, reverse("learning_logs:topic", args=[self.topic.id]))
        self.assertTrue(Entry.objects.filter(topic=self.topic, text="Новая запись").exists())

    def test_new_entry_rejects_other_users_topic(self):
        self.client.force_login(self.owner)
        response = self.client.post(
            reverse("learning_logs:new_entry", args=[self.other_topic.id]), {"text": "Взлом"}
        )
        self.assertEqual(response.status_code, 404)
        self.assertFalse(Entry.objects.filter(text="Взлом").exists())

    def test_owner_can_edit_entry_but_cannot_change_topic(self):
        self.client.force_login(self.owner)
        response = self.client.post(
            reverse("learning_logs:edit_entry", args=[self.entry.id]),
            {"text": "Исправленная запись", "topic": self.other_topic.id},
        )
        self.assertRedirects(response, reverse("learning_logs:topic", args=[self.topic.id]))
        self.entry.refresh_from_db()
        self.assertEqual(self.entry.text, "Исправленная запись")
        self.assertEqual(self.entry.topic, self.topic)

    def test_other_user_cannot_edit_entry(self):
        self.client.force_login(self.other)
        response = self.client.post(
            reverse("learning_logs:edit_entry", args=[self.entry.id]), {"text": "Чужая правка"}
        )
        self.assertEqual(response.status_code, 404)
        self.entry.refresh_from_db()
        self.assertEqual(self.entry.text, "Первоначальная запись")

    def test_entries_are_newest_first(self):
        second = Entry.objects.create(topic=self.topic, text="Вторая запись")
        self.client.force_login(self.owner)
        response = self.client.get(reverse("learning_logs:topic", args=[self.topic.id]))
        self.assertEqual(list(response.context["entries"]), [second, self.entry])


class UserFlowTests(TestCase):
    def test_registration_creates_user_and_logs_in(self):
        response = self.client.post(
            reverse("users:register"),
            {"username": "student", "password1": "Strong-pass-987", "password2": "Strong-pass-987"},
        )
        self.assertRedirects(response, reverse("learning_logs:topics"))
        self.assertTrue(get_user_model().objects.filter(username="student").exists())
        self.assertIn("_auth_user_id", self.client.session)

    def test_logout_accepts_post_only(self):
        user = get_user_model().objects.create_user(username="student", password="strong-pass-123")
        self.client.force_login(user)
        self.assertEqual(self.client.get(reverse("users:logout")).status_code, 405)
        self.assertRedirects(self.client.post(reverse("users:logout")), reverse("learning_logs:index"))
        self.assertNotIn("_auth_user_id", self.client.session)
