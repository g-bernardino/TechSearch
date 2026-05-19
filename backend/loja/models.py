from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

# ==============================================================================
# MODELO PARA AS CATEGORIAS
# ==============================================================================
class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    # Permite blank=True para que possamos gerar o slug automaticamente no save
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    class Meta:
        verbose_name_plural = 'Categorias'

    def save(self, *args, **kwargs):
        # Gera o slug dinamicamente com base no nome antes de gravar
        if not self.slug:
            self.slug = slugify(self.nome)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome

# ==============================================================================
# MODELO PARA OS PRODUTOS
# ==============================================================================
class Produto(models.Model):
    categoria = models.ForeignKey(Categoria, related_name='produtos', on_delete=models.CASCADE)
    nome = models.CharField(max_length=200)
    # Permite blank=True para que seja autogerado pelo Django no save
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    descricao = models.TextField(blank=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    disponivel = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    imagem = models.URLField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # Evita colisões de slugs idênticos no banco de dados de forma proativa
        if not self.slug:
            slug_proposto = slugify(self.nome)
            slug_final = slug_proposto
            contador = 1
            while Produto.objects.filter(slug=slug_final).exists():
                slug_final = f"{slug_proposto}-{contador}"
                contador += 1
            self.slug = slug_final
            
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome
    
    @classmethod
    def criar_produto(cls, nome, categoria_nome, preco, descricao, imagem=None):
        from .models import Categoria
        categoria_obj, _ = Categoria.objects.get_or_create(nome=categoria_nome)
        
        novo_produto = cls.objects.create(
            nome=nome,
            categoria=categoria_obj,
            preco=preco,
            descricao=descricao,
            disponivel=True
        )
        if imagem:
            novo_produto.imagem = imagem
            novo_produto.save()
        return novo_produto
    
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)

    def subtotal(self):
        return self.product.preco * self.quantity