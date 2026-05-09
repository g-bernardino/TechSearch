from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # 1. Rota para o painel de administração
    path('admin/', admin.site.urls),

    # 2. Rota principal que liga à tua aplicação 'catalogo'
    # Quando o utilizador aceder ao site vazio '', ele vai para o catalogo
    path('', include('catalogo.urls')),
]

# 3. CONFIGURAÇÃO PARA IMAGENS E CSS EM DESENVOLVIMENTO
# Este bloco diz ao Django: "Se estivermos a testar (DEBUG=True), 
# permite que as pastas de mídia e estáticos sejam acessíveis pelo navegador".
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)