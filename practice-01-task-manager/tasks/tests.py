from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Task


class TaskAccessTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.owner = user_model.objects.create_user(username="owner", password="strong-pass-123")
        self.other = user_model.objects.create_user(username="other", password="strong-pass-123")
        self.task = Task.objects.create(
            owner=self.owner,
            title="Задача владельца",
            due_date=timezone.now() + timedelta(days=1),
            priority=Task.Priority.HIGH,
        )

    def test_task_list_requires_authentication(self):
        response = self.client.get(reverse("tasks:index"))
        self.assertRedirects(response, f"{reverse('users:login')}?next={reverse('tasks:index')}")

    def test_list_contains_only_current_users_tasks(self):
        Task.objects.create(owner=self.other, title="Чужая задача")
        self.client.force_login(self.owner)
        response = self.client.get(reverse("tasks:index"))
        self.assertContains(response, "Задача владельца")
        self.assertNotContains(response, "Чужая задача")

    def test_create_assigns_authenticated_owner(self):
        self.client.force_login(self.other)
        response = self.client.post(
            reverse("tasks:new"),
            {
                "title": "Новая задача",
                "description": "Проверка владельца",
                "due_date": "2030-05-10T14:30",
                "priority": Task.Priority.NORMAL,
                "completed": "",
                "owner": self.owner.id,
            },
        )
        self.assertRedirects(response, reverse("tasks:index"))
        self.assertEqual(Task.objects.get(title="Новая задача").owner, self.other)

    def test_invalid_due_date_returns_form_error(self):
        self.client.force_login(self.owner)
        response = self.client.post(
            reverse("tasks:new"),
            {"title": "Ошибка даты", "due_date": "не дата", "priority": Task.Priority.NORMAL},
        )
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context["form"], "due_date", "Введите корректные дату и время.")
        self.assertFalse(Task.objects.filter(title="Ошибка даты").exists())

    def test_other_user_cannot_edit_task(self):
        self.client.force_login(self.other)
        response = self.client.post(
            reverse("tasks:edit", args=[self.task.id]),
            {"title": "Взлом", "priority": Task.Priority.LOW},
        )
        self.assertEqual(response.status_code, 404)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, "Задача владельца")

    def test_other_user_cannot_delete_task(self):
        self.client.force_login(self.other)
        response = self.client.post(reverse("tasks:delete", args=[self.task.id]))
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Task.objects.filter(id=self.task.id).exists())

    def test_missing_task_returns_404(self):
        self.client.force_login(self.owner)
        response = self.client.get(reverse("tasks:edit", args=[999999]))
        self.assertEqual(response.status_code, 404)

    def test_toggle_changes_task_state_and_can_restore_it(self):
        self.client.force_login(self.owner)
        url = reverse("tasks:toggle", args=[self.task.id])
        self.client.post(url)
        self.task.refresh_from_db()
        self.assertTrue(self.task.completed)
        self.client.post(url)
        self.task.refresh_from_db()
        self.assertFalse(self.task.completed)

    def test_toggle_rejects_get(self):
        self.client.force_login(self.owner)
        response = self.client.get(reverse("tasks:toggle", args=[self.task.id]))
        self.assertEqual(response.status_code, 405)

    def test_get_delete_only_displays_confirmation(self):
        self.client.force_login(self.owner)
        response = self.client.get(reverse("tasks:delete", args=[self.task.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Task.objects.filter(id=self.task.id).exists())

    def test_post_delete_removes_task(self):
        self.client.force_login(self.owner)
        response = self.client.post(reverse("tasks:delete", args=[self.task.id]))
        self.assertRedirects(response, reverse("tasks:index"))
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())


class UserFlowTests(TestCase):
    def test_registration_creates_user_and_logs_in(self):
        response = self.client.post(
            reverse("users:register"),
            {"username": "student", "password1": "Strong-pass-987", "password2": "Strong-pass-987"},
        )
        self.assertRedirects(response, reverse("tasks:index"))
        self.assertTrue(get_user_model().objects.filter(username="student").exists())
        self.assertIn("_auth_user_id", self.client.session)

    def test_logout_rejects_get_and_accepts_post(self):
        user = get_user_model().objects.create_user(username="logout-user", password="strong-pass-123")
        self.client.force_login(user)
        self.assertEqual(self.client.get(reverse("users:logout")).status_code, 405)
        response = self.client.post(reverse("users:logout"))
        self.assertRedirects(response, reverse("index"))
        self.assertNotIn("_auth_user_id", self.client.session)
