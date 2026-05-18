from django.db import models
from django.utils.text import slugify

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
    imagem = models.ImageField(upload_to='produtos/%Y/%m/%d', blank=True)

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