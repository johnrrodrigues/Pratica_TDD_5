from django.urls import path
from core.views import login, logout, home, listar_links, cadastrar_link


urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('index/', home, name='index'),
    path('cadastrar/', cadastrar_link, name='cadastrar_link'),
    path('listar/', listar_links, name='listar_links'),
    path('', home,name='home')
]