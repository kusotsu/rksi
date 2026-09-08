from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import BlogPostForm
from .models import BlogPost


def index(request):
    posts = BlogPost.objects.select_related("owner").order_by("-date_added")
    return render(request, "blogs/index.html", {"posts": posts})


def post_detail(request, post_id):
    post = get_object_or_404(BlogPost.objects.select_related("owner"), id=post_id)
    return render(request, "blogs/post_detail.html", {"post": post})


@login_required
def new_post(request):
    if request.method == "POST":
        form = BlogPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.owner = request.user
            post.save()
            messages.success(request, "Публикация добавлена.")
            return redirect("blogs:index")
    else:
        form = BlogPostForm()
    return render(request, "blogs/post_form.html", {"form": form, "heading": "Новая публикация"})


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id, owner=request.user)
    if request.method == "POST":
        form = BlogPostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Публикация обновлена.")
            return redirect("blogs:post_detail", post_id=post.id)
    else:
        form = BlogPostForm(instance=post)
    return render(
        request,
        "blogs/post_form.html",
        {"form": form, "heading": "Редактирование публикации", "post": post},
    )

