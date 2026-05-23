from django.urls import path
from core.views import login, logout, home, listar_links, cadastrar_link, editar_link, gerenciar_edicao


urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('index/', home, name='index'),
    path('cadastrar/', cadastrar_link, name='cadastrar_link'),
    path('listar/', listar_links, name='listar_links'),
    path('editar/<int:pk>/', editar_link, name='editar_link'),
    path('gerenciar-edicao/', gerenciar_edicao, name='gerenciar_edicao'),

    path('', home,name='home')
]