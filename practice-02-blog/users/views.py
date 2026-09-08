from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render


def register(request):
    if request.user.is_authenticated:
        return redirect("blogs:index")
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Регистрация завершена. Теперь можно публиковать записи.")
            return redirect("blogs:index")
    else:
        form = UserCreationForm()
    return render(request, "users/register.html", {"form": form})

