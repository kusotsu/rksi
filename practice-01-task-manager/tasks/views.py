from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Case, IntegerField, Value, When
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import TaskForm
from .models import Task


def home(request):
    return render(request, "index.html")


@login_required
def task_list(request):
    tasks = (
        Task.objects.filter(owner=request.user)
        .annotate(
            priority_order=Case(
                When(priority=Task.Priority.HIGH, then=Value(0)),
                When(priority=Task.Priority.NORMAL, then=Value(1)),
                default=Value(2),
                output_field=IntegerField(),
            ),
            no_due_date=Case(
                When(due_date__isnull=True, then=Value(1)),
                default=Value(0),
                output_field=IntegerField(),
            ),
        )
        .order_by("completed", "priority_order", "no_due_date", "due_date", "-date_added")
    )
    return render(request, "tasks/task_list.html", {"tasks": tasks})


@login_required
def task_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.owner = request.user
            task.save()
            messages.success(request, "Задача создана.")
            return redirect("tasks:index")
    else:
        form = TaskForm()
    return render(request, "tasks/task_form.html", {"form": form, "heading": "Новая задача"})


@login_required
def task_edit(request, task_id):
    task = get_object_or_404(Task, id=task_id, owner=request.user)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, "Изменения сохранены.")
            return redirect("tasks:index")
    else:
        form = TaskForm(instance=task)
    return render(
        request,
        "tasks/task_form.html",
        {"form": form, "heading": "Редактирование задачи", "task": task},
    )


@login_required
def task_delete(request, task_id):
    task = get_object_or_404(Task, id=task_id, owner=request.user)
    if request.method == "POST":
        task.delete()
        messages.success(request, "Задача удалена.")
        return redirect("tasks:index")
    return render(request, "tasks/task_confirm_delete.html", {"task": task})


@login_required
@require_POST
def task_toggle(request, task_id):
    task = get_object_or_404(Task, id=task_id, owner=request.user)
    task.completed = not task.completed
    task.save(update_fields=["completed"])
    messages.success(
        request,
        "Задача завершена." if task.completed else "Задача возвращена в работу.",
    )
    return redirect("tasks:index")

