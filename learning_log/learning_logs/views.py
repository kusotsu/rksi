from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import EntryForm, TopicForm
from .models import Entry, Topic


def index(request):
    return render(request, "learning_logs/index.html")


@login_required
def topics(request):
    user_topics = Topic.objects.filter(owner=request.user).order_by("date_added")
    return render(request, "learning_logs/topics.html", {"topics": user_topics})


@login_required
def topic(request, topic_id):
    selected_topic = get_object_or_404(Topic, id=topic_id, owner=request.user)
    entries = selected_topic.entry_set.order_by("-date_added")
    return render(
        request,
        "learning_logs/topic.html",
        {"topic": selected_topic, "entries": entries},
    )


@login_required
def new_topic(request):
    if request.method == "POST":
        form = TopicForm(request.POST)
        if form.is_valid():
            created_topic = form.save(commit=False)
            created_topic.owner = request.user
            created_topic.save()
            messages.success(request, "Тема добавлена.")
            return redirect("learning_logs:topics")
    else:
        form = TopicForm()
    return render(request, "learning_logs/topic_form.html", {"form": form})


@login_required
def new_entry(request, topic_id):
    selected_topic = get_object_or_404(Topic, id=topic_id, owner=request.user)
    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.topic = selected_topic
            entry.save()
            messages.success(request, "Запись добавлена.")
            return redirect("learning_logs:topic", topic_id=selected_topic.id)
    else:
        form = EntryForm()
    return render(
        request,
        "learning_logs/entry_form.html",
        {"form": form, "topic": selected_topic, "heading": "Новая запись"},
    )


@login_required
def edit_entry(request, entry_id):
    entry = get_object_or_404(
        Entry.objects.select_related("topic"), id=entry_id, topic__owner=request.user
    )
    if request.method == "POST":
        form = EntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            messages.success(request, "Запись обновлена.")
            return redirect("learning_logs:topic", topic_id=entry.topic.id)
    else:
        form = EntryForm(instance=entry)
    return render(
        request,
        "learning_logs/entry_form.html",
        {"form": form, "topic": entry.topic, "entry": entry, "heading": "Редактирование записи"},
    )
