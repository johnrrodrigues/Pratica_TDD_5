from django.urls import path
from core.views import (
    login,
    logout,
    home,
    listar_links,
    cadastrar_link,
    editar_link,
    gerenciar_edicao,
    excluir_link,
    gerenciar_exclusao,
)

urlpatterns = [
    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),
    path("index/", home, name="index"),
    path("cadastrar/", cadastrar_link, name="cadastrar_link"),
    path("listar/", listar_links, name="listar_links"),
    path("editar/<int:pk>/", editar_link, name="editar_link"),
    path("gerenciar_edicao/", gerenciar_edicao, name="gerenciar_edicao"),
    path("gerenciar_exclusao/", gerenciar_exclusao, name="gerenciar_exclusao"),
    path("excluir/<int:pk>/", excluir_link, name="excluir_link"),
    path("", home, name="home"),
]
