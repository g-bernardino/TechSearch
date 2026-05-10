from django.db import models

# Modelo para as Categorias (ex: Calçado, Eletrónicos, Roupa)
class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True) # URL amigável (ex: /calcado-desportivo)

    class Meta:
        verbose_name_plural = 'Categorias'

    def __str__(self):
        return self.nome

# Modelo para os Produtos
class Produto(models.Model):
    categoria = models.ForeignKey(Categoria, related_name='produtos', on_delete=models.CASCADE)
    nome = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    descricao = models.TextField(blank=True) # Descrição opcional
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    disponivel = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    # Para imagens, precisaremos instalar uma biblioteca chamada 'Pillow' depois
    imagem = models.ImageField(upload_to='produtos/%Y/%m/%d', blank=True)

    def __str__(self):
        return self.nome
    
# Modelo do Carrinho
class Carrinho(models.Model):
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Carrinho {self.id}"


# Produtos dentro do carrinho
class ItemCarrinho(models.Model):
    carrinho = models.ForeignKey(
        Carrinho,
        related_name='itens',
        on_delete=models.CASCADE
    )

    produto = models.ForeignKey(
        Produto,
        on_delete=models.CASCADE
    )

    quantidade = models.PositiveIntegerField(default=1)

    adicionado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantidade}x {self.produto.nome}"