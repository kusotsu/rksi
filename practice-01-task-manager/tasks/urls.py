from django.urls import path

from . import views

app_name = "tasks"

urlpatterns = [
    path("", views.task_list, name="index"),
    path("new/", views.task_create, name="new"),
    path("<int:task_id>/edit/", views.task_edit, name="edit"),
    path("<int:task_id>/delete/", views.task_delete, name="delete"),
    path("<int:task_id>/toggle/", views.task_toggle, name="toggle"),
]

