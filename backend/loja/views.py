from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Produto, Categoria, CartItem

# ==============================================================================
# 1. PÁGINA INICIAL (HOME)
# ==============================================================================
def home(request):
    produtos = Produto.objects.filter(disponivel=True)
    
    # CONTADOR REAL PARA A NAVBAR:
    cart_count = 0
    if request.user.is_authenticated:
        # Puxa os itens do carrinho do usuário logado
        cart_items = CartItem.objects.filter(user=request.user)
        # Soma a quantidade real de todas as caixinhas do banco de dados
        cart_count = sum(item.quantity for item in cart_items)
        
    context = {
        'featured_products': produtos,
        'cart_count': cart_count, # Injeta o valor exato que o seu home.html precisa!
    }
    return render(request, 'home.html', context)
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
    # Puxa os itens salvos no banco SQLite para este usuário específico
    cart_items = CartItem.objects.filter(user=request.user)
    
    # Calcula os totais que o HTML do carrinho precisa exibir
    total_price = sum(item.subtotal() for item in cart_items)
    cart_count = sum(item.quantity for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'cart_count': cart_count,
    }
    return render(request, 'carrinho.html', context)

# ==============================================================================
# 8. SISTEMA DO CARRINHO (AÇÕES NO BANCO)
# ==============================================================================
@login_required(login_url='login')
def adicionar_ao_carrinho(request, product_id):
    # Procura o produto pelo ID. Se não achar, joga erro 404
    produto = get_object_or_404(Produto, id=product_id)
    
    # Busca o item no carrinho. Se não existir no SQLite, ele cria um novo.
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=produto,
        defaults={'quantity': 1}
    )
    
    # Se ele já existia, incrementa a quantidade +1
    if not created:
        cart_item.quantity += 1
        cart_item.save()
        
    messages.success(request, f"{produto.nome} adicionado ao carrinho!")
    return redirect('carrinho')

# ==============================================================================
# 9. PÁGINA DE PAGAMENTO (CHECKOUT)
# ==============================================================================
@login_required(login_url='login')
def pagamento_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.subtotal() for item in cart_items)
    cart_count = sum(item.quantity for item in cart_items)
    
    if cart_count == 0:
        messages.warning(request, "Seu carrinho está vazio.")
        return redirect('home')
        
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'cart_count': cart_count,
    }
    return render(request, 'pagamento.html', context)

# ==============================================================================
# 10. AUMENTAR E DIMINUIR QUANTIDADE (NO BANCO DE DADOS)
# ==============================================================================
@login_required(login_url='login')
def aumentar_quantidade(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    item.quantity += 1
    item.save()
    return redirect('carrinho')

@login_required(login_url='login')
def diminuir_quantidade(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete() # Se era 1 e clicou em menos, remove do carrinho
    return redirect('carrinho')

def home(request):
    # Busca todos os produtos cadastrados no banco de dados
    produtos_cadastrados = Produto.objects.all()
    
    # Passa os produtos para o template através do contexto
    context = {
        'produtos': produtos_cadastrados
    }
    return render(request, 'home.html', context)