from django.urls import path
from backend.views import index, login, cadastro, ver_carrinho

urlpatterns = [
    path('', index),
    path('login/', login, name= 'login'),
    path('cadastro/', cadastro, name= 'cadastro'),
    path('carrinho/', ver_carrinho, name= 'ver_carrinho'),
]