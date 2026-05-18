from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('carrinho/', views.carrinho, name='carrinho'),
    path('favoritos/', views.favoritos, name='favoritos'),
    path('painel-admin/', views.dashboard_admin, name='dashboard_admin'),
    path('cadastro_produto/', views.cadastrar_produto, name='cadastro_produto'),
]