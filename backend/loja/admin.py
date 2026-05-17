from django.contrib import admin
from .models import Categoria, Produto

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'slug']
    prepopulated_fields = {'slug': ('nome',)} # Gera o slug automaticamente ao escrever o nome

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'preco', 'disponivel', 'criado_em']
    list_filter = ['disponivel', 'criado_em']
    list_editable = ['preco', 'disponivel'] # Permite editar direto na lista
    prepopulated_fields = {'slug': ('nome',)}