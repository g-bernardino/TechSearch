from django.shortcuts import render

def index(request):
    return render(request, 'home.html')

def login(request):
    return render(request, 'login.html')

def cadastro(request):
    return render(request, 'cadastro.html')

def ver_carrinho(request):
    return render(request, 'carrinho.html', {
        'itens': [],
        'total': 0
    })
