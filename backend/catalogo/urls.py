from django.urls import path
from . import views

app_name = 'catalogo'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('registro/', views.cadastro_view, name='cadastro'), # Esta é a rota para a tela acima
    path('produto/<int:id>/', views.detalhe_produto, name='detalhe_produto'),
    path('painel-admin/', views.dashboard_admin, name='dashboard_admin'),
    path('logout/', views.logout_view, name='logout'),
]