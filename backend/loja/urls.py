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
    path('carrinho/adicionar/<int:product_id>/', views.adicionar_ao_carrinho, name='adicionar_ao_carrinho'),
    path('carrinho/aumentar/<int:item_id>/', views.aumentar_quantidade, name='aumentar_quantidade'),
    path('carrinho/diminuir/<int:item_id>/', views.diminuir_quantidade, name='diminuir_quantidade'),
]