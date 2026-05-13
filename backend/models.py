from django.db import models
from djongo import models
from django.contrib.auth.models import User

class Categoria (models.Model):
    nome = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    descricao = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Categorias"

    def __str__(self):      # Mostra o nome correto do objeto
        return self.nome 
    
class Produto(models.Model):        # 'on_delete=models.PROTECT': Impede que ao apagar uma Categoria os produtos nãp sejam apagados junto com ela.
    categoria = models.ForeignKey(Categoria, related_name='produtosCategorias', on_delete=models.PROTECT)

    nome = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    descricao = models.TextField(blank=True, null=True)
    
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    estoque = models.IntegerField(default=0)
    disponivel = models.BooleanField(default=False)

    class Meta:
        ordering = ('nome',)
        
    def __str__(self):
        return self.nome


    def save(self, *args, **kwargs):        # Função para caso haja estoque com produto, apareça como disponível. 
        if self.estoque > 0:                # '*args, **kwargs' = aceite qualquer lista de argumentos e argumentos nomeados que o Django mandar
            self.disponivel = True          

        else: 
            self.disponivel = False

        super().save(*args, **kwargs)


class Cliente(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)

    CPF = models.CharField(max_length=14)
    telefone = models.CharField(max_length=15)
    

    class Meta:
        verbose_name_plural = "Clientes"

    def __str__(self):
        return self.usuario.username
    
class Endereco(models.Model):
    cliente = models.ForeignKey(Cliente, related_name='enderecosClientes', on_delete=models.CASCADE)

    cep = models.CharField(max_length=9) # tamanho exato para a configuração '00000-000'
    rua = models.CharField(max_length=200)
    numero = models.CharField(max_length=10)
    complemento = models.CharField(max_length=100, blank=True, null=True)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)  # uso de siglas (PE, PB, SP...)

    class Meta:
        verbose_name_plural = "Endereços"

    def __str__(self):
        return f"{self.rua}, {self.numero}"
    
class Pedido(models.Model):
    STATUS_CHOICE = (
        ('P', 'Pendente'),
        ('A', 'Aprovado'),
        ('E', 'Enviado'),
        ('C', 'Cancelado'),
        ('F', 'Finalizado'),
    )

    cliente = models.ForeignKey(Cliente, related_name='pedidosClientes', on_delete=models.CASCADE)

    data_pedido = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICE, default='P')

    class Meta:
        verbose_name_plural = "Pedidos"

    def __str__(self):
        return f"Pedido {self.id} - {self.cliente.usuario.username}" 
    

class ItemProduto(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='itemPedido', on_delete=models.CASCADE)

    produto = models.ForeignKey(Produto, related_name='itemProdutos', on_delete=models.CASCADE)

    quantidade = models.IntegerField(default=1)
    preco_unitario = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        verbose_name_plural = "Itens do Pedido"

    def __str__(self):
        return f"{self.quantidade}x {self.produto.nome}"
    
    # mesma lógica da classe Produto.
    def save(self, *args, **kwargs):
        if self.quantidade <= 0:
            if self.pk:     # verifica se já consta no banco de dados
                self.delete()   # se existe e a quantidade caiu para zero, deleta do banco
            return      # o 'return' vazio faz a função parar
        
        # se a quantidade for 1 ou mais, segue o fluxo normalmente
        super().save(*args, **kwargs)

