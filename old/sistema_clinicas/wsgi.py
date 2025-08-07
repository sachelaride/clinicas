"""WSGI config for sistema_clinicas project."""

# Arquivo: sistema_clinicas/wsgi.py
# Configuração WSGI para o projeto

import os

from django.core.wsgi import get_wsgi_application

# Define o módulo de configurações do Django para o ambiente WSGI
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_clinicas.settings')

# Obtém a aplicação WSGI (Web Server Gateway Interface) do Django.
# Esta é a interface principal para servidores web compatíveis com WSGI.
application = get_wsgi_application()
