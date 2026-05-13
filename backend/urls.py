from django.urls import path
from backend.views import index, login, cadastro

urlpatterns = [
    path('', index),
    path('login/', login, name= 'login'),
    path('cadastro/', cadastro, name= 'cadastro'),
]