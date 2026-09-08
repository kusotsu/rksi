from django.contrib import admin
from django.urls import include, path

from tasks import views as task_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", task_views.home, name="index"),
    path("tasks/", include("tasks.urls")),
    path("users/", include("users.urls")),
]

