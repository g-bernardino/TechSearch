from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required  
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Produto, Categoria

# ==============================================================================
# 1. PÁGINA INICIAL (HOME)
# ==============================================================================
def home(request):
    """
    Renderiza a página inicial com todos os produtos disponíveis.
    Os templates são lidos diretamente da raiz da pasta 'frontend/'.
    """
    produtos = Produto.objects.filter(disponivel=True)
    return render(request, 'home.html', {'featured_products': produtos})

# ==============================================================================
# 2. REGISTO DE UTILIZADOR (SIGN UP)
# ==============================================================================
def cadastro_view(request):
    """
    Gere a criação de novas contas de utilizador de forma manual e segura.
    Contorna o UserCreationForm e processa os dados de forma explícita para o banco.
    """
    if request.method == 'POST':
        # Captura os dados exatamente como estão no 'name' do HTML de cadastro.html
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password1', '')
        confirm_password = request.POST.get('password2', '')

        # 1. Validação de preenchimento dos campos obrigatórios
        if not username or not email or not password or not confirm_password:
            messages.error(request, "Todos os campos do formulário são obrigatórios.")
            return render(request, 'cadastro.html')

        # 2. Validação de correspondência de palavras-passe
        if password != confirm_password:
            messages.error(request, "As senhas inseridas não coincidem.")
            return render(request, 'cadastro.html')

        # 3. Validação de tamanho da palavra-passe
        if len(password) < 3:
            messages.error(request, "A senha deve ter pelo menos 3 caracteres.")
            return render(request, 'cadastro.html')

        # 4. Validação se o nome de utilizador já existe
        if User.objects.filter(username=username).exists():
            messages.error(request, "Este nome de usuário já está registado.")
            return render(request, 'cadastro.html')

        # 5. Validação se o e-mail já existe no banco de dados
        if User.objects.filter(email=email).exists():
            messages.error(request, "Este e-mail já está em uso por outra conta.")
            return render(request, 'cadastro.html')

        try:
            # 6. Gravação manual do utilizador de forma robusta na base de dados
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            user.save()  # Salva definitivamente o registo na tabela auth_user
            
            # Autentica e inicia a sessão do utilizador criado de forma automática
            login(request, user)
            messages.success(request, f"Conta criada com sucesso! Bem-vindo(a), {user.username}!")
            return redirect('home')
        except Exception as e:
            messages.error(request, f"Erro inesperado ao gravar no banco de dados: {str(e)}")
            return render(request, 'cadastro.html')

    return render(request, 'cadastro.html')

# ==============================================================================
# 3. LOGIN DE UTILIZADOR (SIGN IN)
# ==============================================================================
def login_view(request):
    """
    Efetua a autenticação de utilizadores aceitando tanto username quanto e-mail.
    """
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        usuario_ou_email = request.POST.get('username')
        senha_enviada = request.POST.get('password')
        
        username_para_login = usuario_ou_email
        
        # Se for detetado um e-mail, localiza o username associado a ele para o login nativo
        if '@' in usuario_ou_email:
            try:
                usuario_encontrado = User.objects.get(email=usuario_ou_email)
                username_para_login = usuario_encontrado.username
            except User.DoesNotExist:
                pass

        user = authenticate(request, username=username_para_login, password=senha_enviada)
        
        if user is not None:
            login(request, user)
            messages.success(request, f"Bem-vindo de volta, {user.username}!")
            
            # Encaminha o utilizador para a página que tentou aceder previamente ou para a home
            proxima_pagina = request.GET.get('next', 'home')
            return redirect(proxima_pagina)
        else:
            messages.error(request, "Utilizador, E-mail ou Senha inválidos.")
            
    return render(request, 'login.html')

# ==============================================================================
# 4. LOGOUT (SAIR)
# ==============================================================================
def logout_view(request):
    """
    Termina a sessão ativa do utilizador e redireciona para a página inicial.
    """
    logout(request)
    return redirect('home')

# ==============================================================================
# 5. PAINEL ADMINISTRATIVO
# ==============================================================================
@staff_member_required
def dashboard_admin(request):
    """
    Ecrã de administração para gerir métricas e stock da loja.
    """
    produtos = Produto.objects.all()
    return render(request, 'dashboard_admin.html', {'produtos': produtos})

# ==============================================================================
# 6. REGISTAR NOVO PRODUTO (ADMIN POST)
# ==============================================================================
@staff_member_required
def cadastrar_produto(request):
    """
    Recebe os dados do formulário do painel administrativo e instancia o novo produto.
    Toda a lógica complexa (como a geração de slug único) é feita pelo save() do modelo.
    """
    if request.method == 'POST':
        nome = request.POST.get('name', '').strip()
        categoria_nome = request.POST.get('category', '').strip()
        preco = request.POST.get('price')
        descricao = request.POST.get('description', '').strip()
        
        if not nome or not preco or not categoria_nome:
            messages.error(request, "Campos obrigatórios em falta (Nome, Categoria ou Preço).")
            return redirect('dashboard_admin')

        try:
            # 1. Obtém ou cria a categoria (o slug de categoria é gerado no save() do models.py)
            categoria_obj, _ = Categoria.objects.get_or_create(nome=categoria_nome)
            
            # 2. Instancia o produto (o slug de produto é gerado no save() do models.py)
            novo_produto = Produto(
                categoria=categoria_obj,
                nome=nome,
                descricao=descricao,
                preco=preco,
                disponivel=True
            )
            
            # Se houver upload de imagem, ela é capturada aqui
            imagem_arquivo = request.FILES.get('image')
            if imagem_arquivo:
                novo_produto.imagem = imagem_arquivo

            novo_produto.save()
            messages.success(request, f"Produto '{nome}' registado com sucesso!")
        except Exception as e:
            messages.error(request, f"Erro ao registar o produto: {str(e)}")
            
    try:
        return redirect('loja:dashboard_admin')
    except Exception:
        return redirect('dashboard_admin')

# ==============================================================================
# 7. FAVORITOS (RESTRITO)
# ==============================================================================
@login_required(login_url='login')
def favoritos(request):
    """
    Visualização de produtos favoritados pelo utilizador. Requer login ativo.
    """
    return render(request, 'favoritos.html')

# ==============================================================================
# 8. CARRINHO DE COMPRAS (RESTRITO)
# ==============================================================================
@login_required(login_url='login')
def carrinho(request):
    """
    Visualização e gestão de compras do utilizador. Requer login ativo.
    """
    return render(request, 'carrinho.html')