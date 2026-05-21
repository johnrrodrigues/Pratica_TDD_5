from django.urls import path
from core.views import login, logout, home, cadastrar_link


urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('index/', home, name='index'),
    path('cadastrar/', cadastrar_link, name='cadastrar_link'),
    path('', home,name='home')
]