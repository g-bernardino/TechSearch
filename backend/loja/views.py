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
    produtos = Produto.objects.filter(disponivel=True)
    return render(request, 'home.html', {'featured_products': produtos})

# ==============================================================================
# 2. REGISTO DE UTILIZADOR (SIGN UP)
# ==============================================================================
def cadastro_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password1', '')
        confirm_password = request.POST.get('password2', '')

        if not username or not email or not password or not confirm_password:
            messages.error(request, "Todos os campos do formulário são obrigatórios.")
            return render(request, 'cadastro.html')

        if password != confirm_password:
            messages.error(request, "As senhas inseridas não coincidem.")
            return render(request, 'cadastro.html')

        if len(password) < 3:
            messages.error(request, "A senha deve ter pelo menos 3 caracteres.")
            return render(request, 'cadastro.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Este nome de usuário já está registado.")
            return render(request, 'cadastro.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Este e-mail já está em uso por outra conta.")
            return render(request, 'cadastro.html')

        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            login(request, user)
            messages.success(request, f"Conta criada com sucesso! Bem-vindo(a), {user.username}!")
            return redirect('home')
        except Exception as e:
            messages.error(request, f"Erro inesperado: {str(e)}")
            return render(request, 'cadastro.html')

    return render(request, 'cadastro.html')

# ==============================================================================
# 3. LOGIN DE UTILIZADOR
# ==============================================================================
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        usuario_ou_email = request.POST.get('username')
        senha_enviada = request.POST.get('password')
        username_para_login = usuario_ou_email

        if '@' in usuario_ou_email:
            try:
                usuario_encontrado = User.objects.get(email=usuario_ou_email)
                username_para_login = usuario_encontrado.username
            except User.DoesNotExist:
                pass

        user = authenticate(request, username=username_para_login, password=senha_enviada)
        if user is not None:
            login(request, user)
            return redirect(request.GET.get('next', 'home'))
        else:
            messages.error(request, "Utilizador, E-mail ou Senha inválidos.")

    return render(request, 'login.html')

# ==============================================================================
# 4. LOGOUT
# ==============================================================================
def logout_view(request):
    logout(request)
    return redirect('home')

# ==============================================================================
# 5. PAINEL ADMINISTRATIVO
# ==============================================================================
@staff_member_required
def dashboard_admin(request):
    produtos = Produto.objects.all()
    return render(request, 'dashboard_admin.html', {'produtos': produtos})

# ==============================================================================
# 6. CADASTRAR NOVO PRODUTO
# ==============================================================================
@staff_member_required
def cadastrar_produto(request):
    if request.method == 'POST':
        try:
            Produto.criar_produto(
                nome=request.POST.get('nome'),
                categoria_nome=request.POST.get('categoria'),
                preco=request.POST.get('preco'),
                descricao=request.POST.get('descricao', ''),
                imagem=request.FILES.get('imagem')
            )
            messages.success(request, "Produto cadastrado com sucesso!")
            return redirect('home')
        except Exception as e:
            messages.error(request, f"Erro ao cadastrar produto: {str(e)}")

    return render(request, 'cadastro_produto.html')

# ==============================================================================
# 7. FAVORITOS E CARRINHO
# ==============================================================================
@login_required(login_url='login')
def favoritos(request):
    return render(request, 'favoritos.html')

@login_required(login_url='login')
def carrinho(request):
    return render(request, 'carrinho.html')