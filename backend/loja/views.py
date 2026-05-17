from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required  
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Produto

# 1. PÁGINA INICIAL (HOME)
def home(request):
    produtos = Produto.objects.all()
    return render(request, 'home.html', {'featured_products': produtos})

# 3. REGISTO DE UTILIZADOR (SIGN UP)
def cadastro_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  
            messages.success(request, "Conta criada com sucesso! Faça o login.")
            return redirect('login')
        else:
            messages.error(request, "Erro no formulário. Verifique os dados.")
    else:
        form = UserCreationForm()
    
    return render(request, 'cadastro.html', {'form': form})

# 4. LOGIN INTELIGENTE (USUÁRIO OU EMAIL)
def login_view(request):
    if request.method == 'POST':
        # Buscamos manualmente os dados enviados pelo seu HTML personalizado
        usuario_ou_email = request.POST.get('username')
        senha_enviada = request.POST.get('password')
        
        # 1. Tentamos achar se o que foi digitado é um e-mail cadastrado
        username_para_login = usuario_ou_email
        if '@' in usuario_ou_email:
            try:
                usuario_encontrado = User.objects.get(email=usuario_ou_email)
                username_para_login = usuario_encontrado.username
            except User.DoesNotExist:
                pass # Se não achar por e-mail, tenta autenticar diretamente com o texto digitado

        # 2. Autentica o usuário usando o Django Backend
        user = authenticate(request, username=username_para_login, password=senha_enviada)
        
        if user is not None:
            login(request, user)
            messages.success(request, f"Bem-vindo de volta, {user.username}!")
            
            # Se tentou entrar por uma página bloqueada (ex: favoritos), redireciona pra ela
            proxima_pagina = request.GET.get('next', 'home')
            return redirect(proxima_pagina)
        else:
            messages.error(request, "Usuário, E-mail ou Senha inválidos.")
    
    return render(request, 'login.html')

# 5. LOGOUT (SAIR)
def logout_view(request):
    logout(request)
    return redirect('home')

# 6. PAINEL DO ADMINISTRADOR (SÓ STAFF)
@staff_member_required
def dashboard_admin(request):
    return render(request, 'dashboard_admin.html')

# 7. FAVORITOS
@login_required(login_url='login')
def favoritos(request):
    return render(request, 'favoritos.html')

# 8. CARRINHO
@login_required(login_url='login')
def carrinho(request):
    return render(request, 'carrinho.html')