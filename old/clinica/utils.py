"""Módulo de utilidades para a aplicação de clínica."""

import os
from django.conf import settings
from django.utils import timezone

# Define o número máximo de arquivos permitidos por diretório antes de criar um novo
MAX_FILES_PER_DIRECTORY = 999

def get_upload_path(instance, filename, model_name):
    """Gera um caminho de upload dinâmico para arquivos, criando novas pastas se o limite for atingido.

    Args:
        instance: A instância do modelo ao qual o arquivo está sendo anexado.
        filename (str): O nome original do arquivo.
        model_name (str): O nome do modelo (ex: 'documentos', 'prontuarios').

    Returns:
        str: O caminho completo para o upload do arquivo.
    """
    today = timezone.now() # Obtém a data e hora atuais
    # Constrói o diretório base no formato: uploads/modelo/ano/mes/dia
    base_dir = os.path.join('uploads', model_name, str(today.year), str(today.month).zfill(2), str(today.day).zfill(2))
    # Constrói o caminho completo no sistema de arquivos
    full_base_dir_path = os.path.join(settings.MEDIA_ROOT, base_dir)

    # Garante que o diretório base exista, criando-o se necessário
    os.makedirs(full_base_dir_path, exist_ok=True)

    # Verifica o número de arquivos no diretório base
    # Lista apenas arquivos, ignorando subdiretórios
    file_count = len([name for name in os.listdir(full_base_dir_path) if os.path.isfile(os.path.join(full_base_dir_path, name))])

    # Se o limite de arquivos por diretório for atingido
    if file_count >= MAX_FILES_PER_DIRECTORY:
        new_dir_index = 1 # Começa a procurar por um novo subdiretório numerado
        while True:
            # Constrói o caminho para o subdiretório numerado
            numbered_dir = os.path.join(base_dir, str(new_dir_index))
            full_numbered_dir_path = os.path.join(settings.MEDIA_ROOT, numbered_dir)
            # Verifica se o subdiretório não existe ou se ainda tem espaço para arquivos
            if not os.path.exists(full_numbered_dir_path) or len([name for name in os.listdir(full_numbered_dir_path) if os.path.isfile(os.path.join(full_numbered_dir_path, name))]) < MAX_FILES_PER_DIRECTORY:
                os.makedirs(full_numbered_dir_path, exist_ok=True) # Cria o novo subdiretório
                return os.path.join(numbered_dir, filename) # Retorna o caminho com o novo subdiretório
            new_dir_index += 1 # Incrementa o índice para o próximo subdiretório
    
    # Se o limite não foi atingido, retorna o caminho no diretório base
    return os.path.join(base_dir, filename)

def documento_upload_path(instance, filename):
    """Função de upload_to para o modelo DocumentoArquivo."""
    return get_upload_path(instance, filename, 'documentos')

def prontuario_upload_path(instance, filename):
    """Função de upload_to para o modelo Prontuario."""
    return get_upload_path(instance, filename, 'prontuarios')
