import random
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from faker import Faker

from clinica.models import (
    Clinica, Paciente, Agendamento, Atendimento, Prontuario,
    TipoTratamento, PastaDocumento, DocumentoArquivo
)

User = get_user_model()

class Command(BaseCommand):
    help = 'Populates the database with sample data.'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Populating database with sample data...'))
        fake = Faker('pt_BR')

        # Clear existing data (optional, but good for fresh runs)
        self.stdout.write(self.style.WARNING('Clearing existing data...'))
        # Delete related models first to avoid integrity errors
        # Tratamento.objects.all().delete() # Removido
        Atendimento.objects.all().delete()
        Agendamento.objects.all().delete()
        Prontuario.objects.all().delete()
        DocumentoArquivo.objects.all().delete()
        PastaDocumento.objects.all().delete()
        TipoTratamento.objects.all().delete()
        Paciente.objects.all().delete()
        Clinica.objects.all().delete()
        # Keep superusers, delete others
        User.objects.filter(is_superuser=False).delete()
        self.stdout.write(self.style.SUCCESS('Existing data cleared.'))

        # 1. Create Clinicas
        self.stdout.write(self.style.SUCCESS('Creating Clinicas...'))
        clinicas = []
        for i in range(3):
            clinica = Clinica.objects.create(
                nome=f'Clínica {fake.city()} {i+1}',
                endereco=fake.address(),
                telefone=fake.phone_number(),
                num_guiches=random.randint(2, 5),
                tempo_minimo_atendimento=random.choice([15, 30, 45, 60])
            )
            clinicas.append(clinica)
            self.stdout.write(f'  Created Clinica: {clinica.nome}')

        # 2. Create Users (Coordenadores, Atendentes, Alunos, Professores)
        self.stdout.write(self.style.SUCCESS('Creating Users...'))
        coordenadores = []
        atendentes = []
        alunos = []
        professores = []

        # Coordenadores
        for i in range(3):
            username = f'coordenador{i+1}'
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': f'{username}@example.com',
                    'password': 'password123',
                    'perfil': 'COORDENADOR',
                    'clinica': random.choice(clinicas)
                }
            )
            if created:
                user.set_password('password123')
                user.save()
                coordenadores.append(user)
                self.stdout.write(f'  Created Coordenador: {user.username}')
            else:
                coordenadores.append(user)
                self.stdout.write(f'  Coordenador {user.username} already exists, skipping creation.')

        # Atendentes
        for i in range(4):
            username = f'atendente{i+1}'
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': f'{username}@example.com',
                    'password': 'password123',
                    'perfil': 'ATENDENTE',
                    'clinica': random.choice(clinicas)
                }
            )
            if created:
                user.set_password('password123')
                user.save()
                atendentes.append(user)
                self.stdout.write(f'  Created Atendente: {user.username}')
            else:
                atendentes.append(user)
                self.stdout.write(f'  Atendente {user.username} already exists, skipping creation.')

        # Professores (para atuar como médicos)
        for i in range(5):
            username = f'professor{i+1}'
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': f'{username}@example.com',
                    'password': 'password123',
                    'perfil': 'PROFESSOR',
                    'clinica': random.choice(clinicas)
                }
            )
            if created:
                user.set_password('password123')
                user.save()
                professores.append(user)
                self.stdout.write(f'  Created Professor: {user.username}')
            else:
                professores.append(user)
                self.stdout.write(f'  Professor {user.username} already exists, skipping creation.')

        # Alunos
        for i in range(10):
            username = f'aluno{i+1}'
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': f'{username}@example.com',
                    'password': 'password123',
                    'perfil': 'ALUNO',
                    'clinica': random.choice(clinicas)
                }
            )
            if created:
                user.set_password('password123')
                user.save()
                alunos.append(user)
                self.stdout.write(f'  Created Aluno: {user.username}')
            else:
                alunos.append(user)
                self.stdout.write(f'  Aluno {user.username} already exists, skipping creation.')

        # 3. Create Pacientes
        self.stdout.write(self.style.SUCCESS('Creating Pacientes...'))
        pacientes = []
        for i in range(30):
            paciente = Paciente.objects.create(
                nome=fake.name(),
                cpf=fake.cpf(),
                data_nascimento=fake.date_of_birth(minimum_age=1, maximum_age=90),
                email=fake.email(),
                telefone=fake.phone_number(),
                endereco=fake.address(),
                responsavel_legal=fake.name() if random.random() < 0.1 else '' # 10% chance of having a legal guardian
            )
            pacientes.append(paciente)
            self.stdout.write(f'  Created Paciente: {paciente.nome}')

        # 4. Create TipoTratamento for each Clinica
        self.stdout.write(self.style.SUCCESS('Creating TipoTratamento...'))
        tipos_tratamento = []
        for clinica in clinicas:
            for i in range(random.randint(3, 7)): # 3 to 7 types per clinic
                tipo = TipoTratamento.objects.create(
                    clinica=clinica,
                    nome=f'Tratamento {fake.word().capitalize()} {i+1}',
                    descricao=fake.text(max_nb_chars=100)
                )
                tipos_tratamento.append(tipo)
                self.stdout.write(f'  Created TipoTratamento: {tipo.nome} for {clinica.nome}')

        # 5. Create Agendamentos, Atendimentos, Prontuarios
        self.stdout.write(self.style.SUCCESS('Creating Agendamentos, Atendimentos, Prontuarios...'))
        for _ in range(50): # Create 50 agendamentos
            paciente = random.choice(pacientes)
            medico = random.choice(professores)
            aluno = random.choice(alunos + [None]) # Some appointments might not have an intern
            clinica_agendamento = medico.clinica # Agendamento is tied to the doctor's clinic

            # Ensure there are available guiches for the chosen clinic
            guiches_disponiveis = list(range(1, clinica_agendamento.num_guiches + 1))
            random.shuffle(guiches_disponiveis)

            agendamento_data = fake.date_time_between(start_date='-30d', end_date='+30d', tzinfo=timezone.get_current_timezone())
            agendamento_data = agendamento_data.replace(hour=random.randint(8, 17), minute=random.choice([0, 30]), second=0, microsecond=0)

            # Find an available guiche for the selected date and clinic
            selected_guiche = None
            for guiche in guiches_disponiveis:
                if not Agendamento.objects.filter(
                    medico__clinica=clinica_agendamento,
                    data__date=agendamento_data.date(),
                    guiche_numero=guiche
                ).exists():
                    selected_guiche = guiche
                    break
            
            if selected_guiche is None:
                self.stdout.write(self.style.WARNING(f'  Skipping agendamento for {paciente.nome} due to no available guiches on {agendamento_data.date()} in {clinica_agendamento.nome}'))
                continue # Skip if no guiche is available

            agendamento = Agendamento.objects.create(
                paciente=paciente,
                medico=medico,
                aluno=aluno,
                data=agendamento_data,
                status=random.choice(['AGENDADO', 'CONCLUIDO', 'CANCELADO']),
                guiche_numero=selected_guiche
            )
            self.stdout.write(f'  Created Agendamento for {paciente.nome} at {agendamento.data} (Guichê: {agendamento.guiche_numero})')

            if agendamento.status == 'CONCLUIDO':
                # Create Prontuario first (or get existing one for patient)
                # For simplicity, let's create a new one for each concluded appointment for now
                # In a real scenario, you might link to an existing open prontuario
                
                # Select a TipoTratamento for the prontuario from the same clinic as the appointment
                available_tipos_tratamento_for_prontuario = TipoTratamento.objects.filter(clinica=clinica_agendamento)
                if not available_tipos_tratamento_for_prontuario.exists():
                    self.stdout.write(self.style.WARNING(f'  Skipping prontuario for {paciente.nome} due to no TipoTratamento in {clinica_agendamento.nome}'))
                    continue
                tipo_tratamento_definido = random.choice(list(available_tipos_tratamento_for_prontuario))

                prontuario = Prontuario.objects.create(
                    paciente=paciente,
                    tipo_tratamento_definido=tipo_tratamento_definido,
                    queixa_principal=fake.sentence(),
                    historia_doenca_atual=fake.paragraph(nb_sentences=3),
                    antecedentes_pessoais_familiares=fake.paragraph(nb_sentences=2),
                    habitos_vida=fake.sentence(),
                    uso_medicamentos=fake.sentence(),
                    alergias_conhecidas=fake.sentence(),
                    sinais_vitais=fake.sentence(),
                    exame_fisico_geral_segmentar=fake.paragraph(nb_sentences=2),
                    avaliacoes_especificas=fake.paragraph(nb_sentences=2),
                    hipoteses_diagnosticas=fake.sentence(),
                    exames_complementares=fake.paragraph(nb_sentences=2),
                    conclusao_diagnostica=fake.sentence(),
                    prescricoes=fake.paragraph(nb_sentences=2),
                    encaminhamentos=fake.sentence(),
                    procedimentos_realizados=fake.paragraph(nb_sentences=2),
                    orientacoes_paciente=fake.sentence(),
                    plano_tratamento_acompanhamento=fake.paragraph(nb_sentences=2),
                    evolucao_clinica=fake.paragraph(nb_sentences=3),
                    assinatura_profissional=fake.name(),
                    registro_profissional=fake.bothify(text='CRM-?? #####'),
                    is_finalized=False # Prontuário começa não finalizado
                )
                self.stdout.write(f'    Created Prontuario {prontuario.pk} for {paciente.nome}')

                # Create Atendimento and link to Prontuario
                atendimento = Atendimento.objects.create(
                    agendamento=agendamento,
                    professor_monitor=medico, # Professor is the monitor
                    observacoes=fake.paragraph(nb_sentences=2),
                    data_inicio=agendamento.data,
                    data_fim=agendamento.data + timedelta(minutes=random.randint(30, 90)),
                    tipo_tratamento_realizado=tipo_tratamento_definido, # Link to the same type as prontuario for simplicity
                    prontuario=prontuario
                )
                self.stdout.write(f'    Created Atendimento {atendimento.pk} linked to Prontuario {prontuario.pk}')

        self.stdout.write(self.style.SUCCESS('Database population completed!'))