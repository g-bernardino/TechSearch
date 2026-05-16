from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required  
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from .models import Produto

# 1. PÁGINA INICIAL (HOME)
def home(request):
    produtos = Produto.objects.all()
    return render(request, 'home.html', {'produtos': produtos})

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

# 4. LOGIN DE UTILIZADOR
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            # Aqui está a mágica: pega o '?next=/favoritos/' da URL.
            # Se não existir (login direto), ele vai para a página de favoritos por padrão.
            proxima_pagina = request.GET.get('next', 'favoritos')
            return redirect(proxima_pagina)
        else:
            messages.error(request, "Usuário ou senha inválidos.")
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})

# 5. LOGOUT (SAIR)
def logout_view(request):
    logout(request)
    return redirect('home')

# 6. PAINEL DO ADMINISTRADOR (SÓ STAFF)
@staff_member_required
def dashboard_admin(request):
    return render(request, 'dashboard_admin')

# 7. FAVORITOS (Duplicação removida e corrigida)
@login_required(login_url='login')
def favoritos(request):
    # Certifique-se de que está 'favoritos.html' e não apenas 'favoritos'
    return render(request, 'favoritos.html')