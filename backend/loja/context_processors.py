from .models import CartItem

def contador_carrinho(request):
    cart_count = 0
    if request.user.is_authenticated:
        # Busca todos os itens do carrinho do usuário logado
        cart_items = CartItem.objects.filter(user=request.user)
        # Soma a quantidade de todas as caixinhas
        cart_count = sum(item.quantity for item in cart_items)
    
    # Retorna um dicionário com a variável que estará disponível em QUALQUER HTML
    return {'cart_count': cart_count}