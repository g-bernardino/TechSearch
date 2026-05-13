from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('login/', views.login_view, name='login'),
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('logout/', views.logout_view, name='logout'),
    path('produto/<int:id>/', views.detalhe_produto, name='detalhe_produto'),
    path('painel-admin/', views.dashboard_admin, name='dashboard_admin'),
]