import requests
from django.core.management.base import BaseCommand
from loja.models import Produto

class Command(BaseCommand):
    help = 'Importa produtos de tecnologia da API externa'

    def handle(self, *args, **kwargs):
        # Lista de categorias de tecnologia do DummyJSON
        categorias_tech = ['laptops', 'smartphones', 'tablets', 'mobile-accessories', 'graphics-processing-unit', 'memory', 'ssd', 'hdd', 'keyboard', 'computer-mouse', 'monitor', 'motherboard', 'headphones', 'computer', 'tv', 'television', 'central-processing-unit', 'charger', 'power-bank', 'camera', 'bluetooth-speaker', 'dongle', 'flash-drive']
        total = 0

        for categoria in categorias_tech:
            url = f"https://dummyjson.com/products/category/{categoria}"
            self.stdout.write(f"Buscando produtos da categoria: {categoria}...")
            
            try:
                response = requests.get(url)
                # Levanta um erro se a requisição falhar (ex: erro 404 ou 500)
                response.raise_for_status() 
                data = response.json()

                for item in data.get('products', []):
                    try:
                        # Evita duplicação
                        if Produto.objects.filter(nome=item['title']).exists():
                            continue

                        Produto.criar_produto(
                            nome=item['title'],
                            categoria_nome=item['category'],
                            preco=float(item['price']),
                            descricao=item['description'], 
                            imagem=item['thumbnail']
                        )

                        total += 1

                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"Erro ao salvar o produto {item.get('title', 'Desconhecido')}: {e}"))
            
            except requests.exceptions.RequestException as e:
                 self.stdout.write(self.style.ERROR(f"Erro ao acessar a API para a categoria {categoria}: {e}"))

        self.stdout.write(self.style.SUCCESS(f"Sucesso! {total} produtos de tecnologia foram importados para o banco de dados!"))