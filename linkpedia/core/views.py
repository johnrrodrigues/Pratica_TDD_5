from django.shortcuts import render, redirect
from django.db.models import Q
from core.forms import LoginForm, LinkForm
from core.models import LinkModel
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required


def login(request):
    if request.user.id is not None:
        return redirect("home")
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            auth_login(request, form.user)
            return redirect("home")
        context = {"acesso_negado": True}
        return render(request, "login.html", {"form": form})
    return render(request, "login.html", {"form": LoginForm()})


def logout(request):
    if request.method == "POST":
        auth_logout(request)
        return render(request, "logout.html")
    return redirect("home")


@login_required
def home(request):
    context = {}
    return render(request, "index.html", context)


@login_required
def cadastrar_link(request):
    if request.method == "POST":
        form = LinkForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = LinkForm()
    return render(request, "cadastrar.html", {"form": form})


@login_required
def listar_links(request):
    termo_busca = request.GET.get("busca", "").strip()
    if termo_busca:
        links = LinkModel.objects.filter(
            Q(titulo__icontains=termo_busca) |
            Q(link__icontains=termo_busca) |
            Q(observacao__icontains=termo_busca))
    else:
        links = LinkModel.objects.all()
    return render(request, "listar.html", {"links": links, "busca": termo_busca})
