"""Módulo que define as configurações de URL raiz para o projeto Sistema de Clínicas."""

# Importa o módulo admin do Django para incluir as URLs da interface de administração
from django.contrib import admin
# Importa path para definir rotas de URL e include para incluir URLs de outros aplicativos
from django.urls import path, include, re_path
from django.views.generic import TemplateView
# Importa serve para servir arquivos estáticos e de mídia em ambiente de desenvolvimento
from django.views.static import serve
# Importa as configurações do projeto
from django.conf import settings
# Importa a função static para configurar o serviço de arquivos estáticos e de mídia
from django.conf.urls.static import static

# Lista de padrões de URL para o projeto
urlpatterns = [
    path('admin/', admin.site.urls), # Inclui as URLs da interface de administração do Django
    path('api/', include('clinica.api_urls')),
    path('', include('clinica.urls')), # Inclui as URLs do aplicativo 'clinica' na raiz do projeto
    re_path(r'.*' , TemplateView.as_view(template_name='index.html'), name='react_app'),
]

# Configuração para servir arquivos estáticos e de mídia em ambiente de desenvolvimento (DEBUG=True)
# Esta configuração NÃO deve ser usada em produção; um servidor web (Nginx, Apache) deve servir esses arquivos.
if settings.DEBUG:
    # Adiciona URLs para servir arquivos estáticos
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    # Adiciona URLs para servir arquivos de mídia (uploads de usuários)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)