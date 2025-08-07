"""ASGI config for sistema_clinicas project."""

# Arquivo: sistema_clinicas/asgi.py
# Configuração ASGI para o projeto

import os

from django.core.asgi import get_asgi_application

# Define o módulo de configurações do Django para o ambiente ASGI
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_clinicas.settings')

# Obtém a aplicação ASGI (Asynchronous Server Gateway Interface) do Django.
# Esta é a interface principal para servidores web assíncronos.
application = get_asgi_application()
