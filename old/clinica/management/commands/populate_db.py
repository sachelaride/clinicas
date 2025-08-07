"""Módulo para comando de gerenciamento personalizado para popular o banco de dados."""

# Importa a classe BaseCommand para criar comandos de gerenciamento personalizados
from django.core.management.base import BaseCommand
# Importa a função para obter o modelo de usuário ativo do Django
from django.contrib.auth import get_user_model
# Importa o modelo Clinica do aplicativo clinica
from clinica.models import Clinica

# Obtém o modelo de usuário personalizado que está ativo no projeto
User = get_user_model()

class Command(BaseCommand):
    """Comando de gerenciamento para popular o banco de dados com dados iniciais.

    Este comando cria uma clínica padrão e um superusuário inicial se eles não existirem.
    É útil para configurar um ambiente de desenvolvimento rapidamente.
    """
    help = 'Populate the database with initial data' # Descrição do comando exibida na ajuda

    def handle(self, *args, **options):
        """Lógica principal do comando de gerenciamento.

        Executada quando o comando `python manage.py populate_db` é chamado.
        """
        # Tenta obter uma clínica com o nome 'Clínica Central'.
        # Se não existir, cria uma nova com os valores padrão fornecidos.
        clinica, created = Clinica.objects.get_or_create(
            nome='Clínica Central',
            defaults={'endereco': 'Rua Exemplo, 123'}
        )
        if created:
            # Exibe uma mensagem de sucesso se a clínica foi criada
            self.stdout.write(self.style.SUCCESS('Criada Clínica: Clínica Central'))
        else:
            # Exibe uma mensagem de aviso se a clínica já existia
            self.stdout.write(self.style.WARNING('Clínica Central já existe'))

        # Define o nome de usuário para o superusuário a ser criado
        username = 'admin'
        # Verifica se um superusuário com este nome de usuário já existe
        if not User.objects.filter(username=username).exists():
            # Cria um novo superusuário com as credenciais e perfil especificados
            User.objects.create_superuser(
                username=username,
                password='lizard1240king', # Senha padrão (MUDAR EM PRODUÇÃO!)
                email='admin@example.com',
                perfil='COORDENADOR', # Define o perfil do superusuário como COORDENADOR
                clinica=clinica # Associa o superusuário à clínica criada
            )
            # Exibe uma mensagem de sucesso se o superusuário foi criado
            self.stdout.write(self.style.SUCCESS(f'Criado superusuário: {username}'))
        else:
            # Exibe uma mensagem de aviso se o superusuário já existia
            self.stdout.write(self.style.WARNING(f'Superusuário {username} já existe'))

        # Exibe uma mensagem final de sucesso para a operação de população do banco de dados
        self.stdout.write(self.style.SUCCESS('Banco de dados populado com sucesso.'))
