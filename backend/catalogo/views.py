from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from .models import Produto

# 1. PÁGINA INICIAL (INDEX)
# Lista todos os produtos do SQLite para o carrossel/grid
def index(request):
    produtos = Produto.objects.all()
    return render(request, 'catalogo/index.html', {'produtos': produtos})

# 2. DETALHE DO PRODUTO
# Exibe informações de um produto específico baseado no ID
def detalhe_produto(request, id):
    produto = get_object_or_404(Produto, id=id)
    return render(request, 'catalogo/detalhe.html', {'produto': produto})

# 3. REGISTO DE UTILIZADOR (SIGN UP)
# Cria o utilizador no banco de dados SQLite
def cadastro_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Guarda o utilizador no SQLite
            messages.success(request, "Conta criada com sucesso! Faça o login.")
            return redirect('catalogo:login')
        else:
            # Se houver erro (senha fraca, user já existe), mantém os dados e mostra erro
            messages.error(request, "Erro no formulário. Verifique os dados.")
    else:
        form = UserCreationForm()
    
    return render(request, 'catalogo/registro.html', {'form': form})

# 4. LOGIN DE UTILIZADOR
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('catalogo:index')
    else:
        form = AuthenticationForm()
    
    return render(request, 'catalogo/login.html', {'form': form})

# 5. LOGOUT (SAIR)
def logout_view(request):
    logout(request)
    return redirect('catalogo:index')

# 6. PAINEL DO ADMINISTRADOR (SÓ STAFF)
# A função de cadastro de produtos que só o Admin acessa
@staff_member_required
def dashboard_admin(request):
    # Aqui podes adicionar lógica para listar produtos para editar/apagar
    return render(request, 'catalogo/dashboard_admin.html')