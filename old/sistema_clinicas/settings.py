"""Configurações principais do projeto Django para o Sistema de Clínicas."""

import os
from pathlib import Path

# Define o diretório base do projeto, que é dois níveis acima deste arquivo (settings.py)
BASE_DIR = Path(__file__).resolve().parent.parent


# Chave de segurança (gerada aleatoriamente para este exemplo; substitua por uma chave única e secreta em produção)
SECRET_KEY = 'django-insecure-@k#9z2h5j7p!qwe4rty8uio0pasdfghjklzxcvbnm1234567890'


# Configurações de Debug e Hosts Permitidos
DEBUG = True  # Define o modo de depuração. Deve ser False em produção para segurança.
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0', '192.168.0.136', 'testserver'] # Lista de hosts permitidos para acessar a aplicação.
#ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.1.0.0', '192.168.0.136']  # Exemplo: Adicione o IP do servidor se necessário em produção

# Modelo de Usuário Personalizado
AUTH_USER_MODEL = 'clinica.User' # Define o modelo de usuário personalizado a ser usado pelo Django.
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend', # Backend de autenticação padrão do Django.
]

# Aplicativos Instalados
INSTALLED_APPS = [
    'django.contrib.admin', # Interface de administração do Django.
    'django.contrib.auth', # Sistema de autenticação e permissões.
    'django.contrib.contenttypes', # Framework para tipos de conteúdo.
    'django.contrib.sessions', # Framework de sessões.
    'django.contrib.messages', # Framework de mensagens.
    'django.contrib.staticfiles', # Gerenciamento de arquivos estáticos.
    'corsheaders', # Adicionado para CORS
    'rest_framework', # Adicionado para Django REST Framework
    'clinica.apps.ClinicaConfig', # Seu aplicativo 'clinica'.
#    'clinica', # Alternativa mais simples para registrar o app, se ClinicaConfig não for necessário.
]

# Middleware
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware', # Adicionado para CORS
    'django.middleware.security.SecurityMiddleware', # Proteções de segurança básicas.
    'django.contrib.sessions.middleware.SessionMiddleware', # Gerencia sessões de usuário.
    'django.middleware.common.CommonMiddleware', # Normaliza requisições e respostas.
    'django.middleware.csrf.CsrfViewMiddleware', # Proteção contra ataques CSRF.
    'django.contrib.auth.middleware.AuthenticationMiddleware', # Associa usuários a requisições.
    'django.contrib.messages.middleware.MessageMiddleware', # Gerencia mensagens temporárias.
    'django.middleware.clickjacking.XFrameOptionsMiddleware', # Proteção contra clickjacking.
]

# Configuração de URLs
ROOT_URLCONF = 'sistema_clinicas.urls' # Define o módulo de URL raiz do projeto.

# Configuração de Banco de Dados (Primeira ocorrência - pode ser um placeholder ou duplicata)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'clinicas_db',  # Nome do banco de dados criado
        'USER': 'german',      # Usuário do banco de dados criado
        'PASSWORD': 'lizard1240king',  # Senha do usuário do banco de dados
        'HOST': 'localhost',         # Geralmente 'localhost' se o PostgreSQL estiver na mesma máquina
        'PORT': '5432',                  # Porta padrão do PostgreSQL
    }
}


# Configuração de Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates', # Backend de templates do Django.
        'DIRS': [BASE_DIR / 'frontend' / 'build'], # Diretórios adicionais para templates (vazio por padrão, apps têm seus próprios).
        'APP_DIRS': True, # Permite que o Django procure templates dentro dos diretórios 'templates' dos apps.
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug', # Adiciona variáveis de depuração ao contexto.
                'django.template.context_processors.request', # Adiciona o objeto request ao contexto.
                'django.contrib.auth.context_processors.auth', # Adiciona variáveis de autenticação ao contexto.
                'django.contrib.messages.context_processors.messages', # Adiciona mensagens ao contexto.
            ],
        },
    },
]

# Arquivos Estáticos
STATIC_URL = '/static/' # URL para servir arquivos estáticos.
STATIC_ROOT = BASE_DIR / 'staticfiles' # Diretório onde os arquivos estáticos serão coletados para produção.
STATICFILES_DIRS = [ 
        BASE_DIR / 'static', # Diretórios adicionais onde o Django deve procurar arquivos estáticos.
        BASE_DIR / 'frontend' / 'build' / 'static',
]

# Configuração de Mídia (Uploads)
MEDIA_URL = '/media/' # URL para servir arquivos de mídia (uploads de usuários).
MEDIA_ROOT = BASE_DIR / 'media' # Diretório onde os arquivos de mídia serão armazenados.
FILE_UPLOAD_TEMP_DIR = BASE_DIR / 'tmp' # Diretório temporário para uploads de arquivos.

# Configuração de Cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache', # Backend de cache baseado em arquivo.
        'LOCATION': BASE_DIR / 'django_cache', # Diretório onde os arquivos de cache serão armazenados.
    }
}


# Configuração de Logging
LOGGING = {
    'version': 1, # Versão da configuração de logging.
    'disable_existing_loggers': False, # Não desabilita loggers existentes.
    'handlers': {
        'file': { # Handler para logar em arquivo.
            'level': 'INFO', # Nível mínimo de log a ser capturado.
            'class': 'logging.FileHandler', # Classe do handler (escreve em arquivo).
            'filename': BASE_DIR / 'logs' / 'audit.log', # Caminho do arquivo de log.
        },
    },
    'loggers': {
        'clinica': { # Logger específico para o aplicativo 'clinica'.
            'handlers': ['file'], # Usa o handler 'file'.
            'level': 'INFO', # Nível mínimo de log para este logger.
            'propagate': True, # Propaga logs para loggers pais.
        },
    },
}

CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]
CORS_ALLOW_CREDENTIALS = True
CSRF_TRUSTED_ORIGINS = ['http://localhost:3000']

LOGIN_URL = '/api/login/'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
}

# Configurações de Integração (Placeholders)

# Integração com Plataformas de Telemedicina (Ex: Zoom, Whereby)
TELEMEDICINA_API_KEY = os.environ.get('TELEMEDICINA_API_KEY', '')
TELEMEDICINA_API_SECRET = os.environ.get('TELEMEDICINA_API_SECRET', '')
TELEMEDICINA_WEBHOOK_SECRET = os.environ.get('TELEMEDICINA_WEBHOOK_SECRET', '')

# Integração com Plataformas de Pagamento (Ex: PagSeguro, Gerencianet)
PAYMENT_GATEWAY_API_KEY = os.environ.get('PAYMENT_GATEWAY_API_KEY', '')
PAYMENT_GATEWAY_API_SECRET = os.environ.get('PAYMENT_GATEWAY_API_SECRET', '')
PAYMENT_GATEWAY_WEBHOOK_SECRET = os.environ.get('PAYMENT_GATEWAY_WEBHOOK_SECRET', '')

# Integração com ERPs (Ex: Totvs, Omie)
ERP_API_KEY = os.environ.get('ERP_API_KEY', '')
ERP_API_SECRET = os.environ.get('ERP_API_SECRET', '')
ERP_TENANT_ID = os.environ.get('ERP_TENANT_ID', '')