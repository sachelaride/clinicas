
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from clinica.models import Agendamento, Prontuario

class Command(BaseCommand):
    help = 'Cria grupos de usuários e atribui permissões'

    def handle(self, *args, **options):
        # Criação dos grupos
        coordenador_group, created = Group.objects.get_or_create(name='Coordenador')
        atendente_group, created = Group.objects.get_or_create(name='Atendente')
        profissional_group, created = Group.objects.get_or_create(name='Profissional')

        # Obtém os content types para os modelos
        agendamento_content_type = ContentType.objects.get_for_model(Agendamento)
        prontuario_content_type = ContentType.objects.get_for_model(Prontuario)

        # Obtém as permissões
        change_agendamento = Permission.objects.get(content_type=agendamento_content_type, codename='change_agendamento')
        view_prontuario = Permission.objects.get(content_type=prontuario_content_type, codename='view_prontuario')
        change_prontuario = Permission.objects.get(content_type=prontuario_content_type, codename='change_prontuario')
        delete_prontuario = Permission.objects.get(content_type=prontuario_content_type, codename='delete_prontuario')
        add_prontuario = Permission.objects.get(content_type=prontuario_content_type, codename='add_prontuario')

        # Atribui permissões ao grupo Coordenador
        coordenador_group.permissions.add(change_agendamento, view_prontuario, change_prontuario, delete_prontuario, add_prontuario)

        # Atribui permissões ao grupo Atendente
        atendente_group.permissions.add(change_agendamento)

        # Atribui permissões ao grupo Profissional
        profissional_group.permissions.add(view_prontuario, change_prontuario, add_prontuario)

        self.stdout.write(self.style.SUCCESS('Grupos e permissões configurados com sucesso!'))
