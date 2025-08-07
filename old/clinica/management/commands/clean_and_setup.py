from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
User = get_user_model()
from django.contrib.contenttypes.models import ContentType
from clinica.models import Prontuario, Paciente, Agendamento, Atendimento, PastaDocumento, DocumentoArquivo, TipoTratamento, Clinica
from django.db import transaction

class Command(BaseCommand):
    help = 'Cleans the database, keeps only superusers, creates "Administradores" group, and assigns clinic/treatment permissions.'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('Starting database cleanup and setup...'))

        with transaction.atomic():
            # 1. Delete all data except superusers
            self.stdout.write(self.style.WARNING('Deleting non-superuser data...'))
            # Delete related models first to avoid integrity errors
            TipoTratamento.objects.all().delete()
            TipoTratamento.objects.all().delete()
            Atendimento.objects.all().delete()
            Agendamento.objects.all().delete()
            Prontuario.objects.all().delete()
            DocumentoArquivo.objects.all().delete()
            PastaDocumento.objects.all().delete()
            Paciente.objects.all().delete()
            Clinica.objects.all().delete()

            # Delete non-superuser users
            non_superusers = User.objects.filter(is_superuser=False)
            num_deleted_users = non_superusers.count()
            non_superusers.delete()
            self.stdout.write(self.style.SUCCESS(f'Deleted {num_deleted_users} non-superuser users.'))

            # 2. Create "Administradores" group
            admin_group, created = Group.objects.get_or_create(name='Administradores')
            if created:
                self.stdout.write(self.style.SUCCESS('Successfully created "Administradores" group.'))
            else:
                self.stdout.write(self.style.WARNING('"Administradores" group already exists.'))

            # 3. Assign permissions to "Administradores" group
            self.stdout.write(self.style.WARNING('Assigning permissions to "Administradores" group...'))
            
            # Permissions for Clinica model
            clinica_content_type = ContentType.objects.get_for_model(Clinica)
            clinica_permissions = [
                'add_clinica', 'change_clinica', 'delete_clinica', 'view_clinica'
            ]
            for perm_name in clinica_permissions:
                permission = Permission.objects.get(content_type=clinica_content_type, codename=perm_name)
                admin_group.permissions.add(permission)
                self.stdout.write(self.style.SUCCESS(f'  - Added {perm_name} to "Administradores".'))

            # Permissions for TipoTratamento model
            tipotratamento_content_type = ContentType.objects.get_for_model(TipoTratamento)
            tipotratamento_permissions = [
                'add_tipotratamento', 'change_tipotratamento', 'delete_tipotratamento', 'view_tipotratamento'
            ]
            for perm_name in tipotratamento_permissions:
                permission = Permission.objects.get(content_type=tipotratamento_content_type, codename=perm_name)
                admin_group.permissions.add(permission)
                self.stdout.write(self.style.SUCCESS(f'  - Added {perm_name} to "Administradores".'))
            
            # 5. Add all superusers to the "Administradores" group
            superusers = User.objects.filter(is_superuser=True)
            for user in superusers:
                user.groups.add(admin_group)
                self.stdout.write(self.style.SUCCESS(f'Added superuser "{user.username}" to "Administradores" group.'))

        self.stdout.write(self.style.SUCCESS('Database cleanup and setup completed successfully!'))
