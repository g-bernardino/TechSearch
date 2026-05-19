from django.urls import path
from . import views

urlpatterns = [
    # Páginas Principais e Autenticação
    path('', views.home, name='home'),
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('favoritos/', views.favoritos, name='favoritos'),
    path('pagamento/', views.pagamento, name='pagamento'),
    path('pagamento/processar/', views.processar_pagamento, name='processar_pagamento'),
    
    # Painel Administrativo
    path('painel-admin/', views.dashboard_admin, name='dashboard_admin'),
    path('cadastro_produto/', views.cadastrar_produto, name='cadastro_produto'),
    
    # Visualização do Carrinho
    path('carrinho/', views.carrinho, name='carrinho'),
    
    # Sistema do Carrinho (Adicionar)
    path('carrinho/adicionar/<int:produto_id>/', views.adicionar_carrinho, name='adicionar_carrinho'),
    path('carrinho/adicionar-ao-carrinho/<int:product_id>/', views.adicionar_ao_carrinho, name='adicionar_ao_carrinho'), # Atalho de segurança
    
    # Alteração de Quantidades (Corrigido para receber produto_id e sincronizar com views.py)
    path('carrinho/aumentar/<int:produto_id>/', views.aumentar_quantidade, name='aumentar_quantidade'),
    path('carrinho/diminuir/<int:produto_id>/', views.diminuir_quantidade, name='diminuir_quantidade'),
    
    # Remoção Completa do Item do Carrinho
    path('carrinho/remover/<int:produto_id>/', views.remover_carrinho, name='remover_carrinho'),
    
    # Sistema de Favoritos
    path('favoritos/', views.favoritos, name='favoritos'),
    path('favoritos/adicionar/<int:produto_id>/', views.adicionar_favorito, name='adicionar_favorito'),
    path('favoritos/remover/<int:produto_id>/', views.remover_favorito, name='remover_favorito'), # Nova rota
    path('endereco/', views.endereco_view, name='endereco_view'),
    path('endereco/salvar/', views.salvar_endereco, name='salvar_endereco'),
]