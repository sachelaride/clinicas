"""Módulo de configuração do aplicativo Django para a aplicação 'clinica'."""

# Importa a classe base para configuração de aplicativos Django
from django.apps import AppConfig

class ClinicaConfig(AppConfig):
    """Configuração do aplicativo 'clinica'."""
    # Define o tipo de chave primária padrão para os modelos do aplicativo.
    # 'BigAutoField' é uma chave primária de 64 bits, adequada para a maioria dos casos.
    default_auto_field = 'django.db.models.BigAutoField'
    
    # Define o nome do aplicativo. Este nome deve corresponder ao nome do diretório
    # do aplicativo e é usado pelo Django para identificar o app.
    name = 'clinica'
