import os
import random
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
from django.core.files.base import ContentFile # Importar ContentFile
from django.conf import settings # Importar settings para MEDIA_ROOT

from clinica.models import (
    Agendamento,
    Atendimento,
    CampanhaMarketing,
    Clinica,
    Comissao,
    Convenio,
    CupomDesconto,
    DocumentoArquivo,
    Fatura,
    LancamentoFinanceiro,
    Lead,
    Paciente,
    PastaDocumento,
    PesquisaSatisfacao,
    Plano,
    Profissional,
    Prontuario,
    TabelaPrecos,
    TipoTratamento,
    User,
)


class Command(BaseCommand):
    help = "Populates the database with test data."

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing data before populating.",
        )

    def handle(self, *args, **options):
        self.fake = Faker("pt_BR")
        self.stdout.write(self.style.SUCCESS("Starting data population..."))

        if options["clear"]:
            self.clear_data()

        self.create_clinica()
        self.create_users()
        self.create_profissionais()
        self.create_pacientes()
        self.create_tipos_tratamento()
        self.create_convenios_e_planos()
        self.create_agendamentos_e_atendimentos()
        self.create_prontuarios()
        self.create_lancamentos_financeiros()
        self.create_faturas()
        self.create_comissoes()
        self.create_leads()
        self.create_campanhas_marketing()
        self.create_pesquisas_satisfacao()
        self.create_cupons_desconto()
        self.create_documentos()

        self.stdout.write(self.style.SUCCESS("Data population completed!"))

    def clear_data(self):
        self.stdout.write(self.style.WARNING("Clearing existing data..."))
        Agendamento.objects.all().delete()
        Atendimento.objects.all().delete()
        CampanhaMarketing.objects.all().delete()
        Clinica.objects.all().delete()
        Comissao.objects.all().delete()
        Convenio.objects.all().delete()
        CupomDesconto.objects.all().delete()
        DocumentoArquivo.objects.all().delete()
        Fatura.objects.all().delete()
        LancamentoFinanceiro.objects.all().delete()
        Lead.objects.all().delete()
        Paciente.objects.all().delete()
        PastaDocumento.objects.all().delete()
        PesquisaSatisfacao.objects.all().delete()
        Plano.objects.all().delete()
        Profissional.objects.all().delete()
        Prontuario.objects.all().delete()
        TabelaPrecos.objects.all().delete()
        TipoTratamento.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()  # Keep superuser
        self.stdout.write(self.style.WARNING("Data cleared."))

    def create_clinica(self):
        self.clinica = Clinica.objects.create(
            nome=self.fake.company(),
            endereco=self.fake.address(),
            telefone=self.fake.phone_number(),
            num_guiches=random.randint(3, 10),
            tempo_minimo_atendimento=random.choice([15, 30, 45, 60]),
        )
        self.stdout.write(self.style.SUCCESS(f"Created Clinica: {self.clinica.nome}"))

    def create_users(self):
        self.coordinator_user = User.objects.create_user(
            username="coordenador",
            email="coordenador@example.com",
            password="test1234",
            perfil="COORDENADOR",
            clinica=self.clinica,
            is_staff=True,
        )
        self.stdout.write(self.style.SUCCESS("Created Coordinator User."))

        self.professional_users = []
        for i in range(3):
            user = User.objects.create_user(
                username=f"profissional{i+1}",
                email=f"profissional{i+1}@example.com",
                password="test1234",
                perfil="PROFISSIONAL",
                clinica=self.clinica,
                is_staff=True,
            )
            self.professional_users.append(user)
        self.stdout.write(self.style.SUCCESS("Created Professional Users."))

        self.atendente_users = []
        for i in range(2):
            user = User.objects.create_user(
                username=f"atendente{i+1}",
                email=f"atendente{i+1}@example.com",
                password="test1234",
                perfil="ATENDENTE",
                clinica=self.clinica,
                is_staff=True,
            )
            self.atendente_users.append(user)
        self.stdout.write(self.style.SUCCESS("Created Atendente Users."))

    def create_profissionais(self):
        self.profissionais = []
        especialidades = ["Odontologia", "Clínica Geral", "Pediatria", "Dermatologia"]
        conselhos = ["CRO", "CRM", "COREN"]
        for user in self.professional_users:
            profissional = Profissional.objects.create(
                user=user,
                especialidade=random.choice(especialidades),
                conselho_profissional=random.choice(conselhos),
                numero_conselho=self.fake.unique.pystr(min_chars=5, max_chars=10),
                carga_horaria_semanal=random.randint(20, 40),
                comissao_percentual=random.uniform(5.0, 20.0),
            )
            self.profissionais.append(profissional)
        self.stdout.write(self.style.SUCCESS("Created Profissionais."))

    def create_pacientes(self):
        self.pacientes = []
        for _ in range(20):
            paciente = Paciente.objects.create(
                nome=self.fake.name(),
                cpf=self.fake.unique.cpf(),
                rg=self.fake.unique.rg(),
                data_nascimento=self.fake.date_of_birth(minimum_age=1, maximum_age=90),
                email=self.fake.unique.email(),
                telefone=self.fake.phone_number(),
                endereco=self.fake.address(),
                responsavel_legal=self.fake.name() if random.random() < 0.2 else "",
                clinica=self.clinica,
            )
            self.pacientes.append(paciente)
        self.stdout.write(self.style.SUCCESS("Created Pacientes."))

    def create_tipos_tratamento(self):
        self.tipos_tratamento = []
        tratamentos = ["Limpeza", "Restauração", "Extração", "Clareamento", "Consulta"]
        for tratamento_nome in tratamentos:
            tipo_tratamento = TipoTratamento.objects.create(
                clinica=self.clinica,
                nome=tratamento_nome,
                descricao=self.fake.sentence(),
                tempo_minimo_atendimento=random.choice([15, 30, 45, 60]),
            )
            self.tipos_tratamento.append(tipo_tratamento)
        self.stdout.write(self.style.SUCCESS("Created Tipos de Tratamento."))

    def create_convenios_e_planos(self):
        self.convenios = []
        self.planos = []
        for _ in range(3):
            convenio = Convenio.objects.create(
                nome=self.fake.company() + " Convênio",
                clinica=self.clinica,
            )
            self.convenios.append(convenio)
            for _ in range(random.randint(1, 3)):
                plano = Plano.objects.create(
                    convenio=convenio,
                    nome=self.fake.word() + " Plano",
                )
                self.planos.append(plano)
        self.stdout.write(self.style.SUCCESS("Created Convenios and Planos."))

    def create_agendamentos_e_atendimentos(self):
        self.agendamentos = []
        self.atendimentos = []
        for _ in range(30):
            paciente = random.choice(self.pacientes)
            profissional = random.choice(self.profissionais)
            data_agendamento = self.fake.date_time_between(
                start_date="-1y", end_date="+1y", tzinfo=timezone.get_current_timezone()
            )
            # Ensure minimum 15 minutes duration for appointments
            data_agendamento = data_agendamento.replace(
                minute=(data_agendamento.minute // 15) * 15
            )

            agendamento = Agendamento.objects.create(
                paciente=paciente,
                profissional=profissional,
                data=data_agendamento,
                status=random.choice(["AGENDADO", "CONCLUIDO", "CANCELADO"]),
                guiche_numero=random.randint(1, self.clinica.num_guiches),
            )
            self.agendamentos.append(agendamento)

            if agendamento.status == "CONCLUIDO":
                data_inicio = agendamento.data
                data_fim = data_inicio + timedelta(minutes=random.randint(15, 60))
                atendimento = Atendimento.objects.create(
                    agendamento=agendamento,
                    observacoes=self.fake.paragraph(),
                    data_inicio=data_inicio,
                    data_fim=data_fim,
                    status="FINALIZADO",
                    tipo_tratamento_realizado=random.choice(self.tipos_tratamento),
                )
                self.atendimentos.append(atendimento)
            elif agendamento.status == "AGENDADO" and random.random() < 0.5: # Some pending appointments might have an ongoing attendance
                data_inicio = agendamento.data
                atendimento = Atendimento.objects.create(
                    agendamento=agendamento,
                    observacoes=self.fake.paragraph(),
                    data_inicio=data_inicio,
                    status="INICIADO",
                    tipo_tratamento_realizado=random.choice(self.tipos_tratamento),
                )
                self.atendimentos.append(atendimento)
        self.stdout.write(self.style.SUCCESS("Created Agendamentos and Atendimentos."))

    def create_prontuarios(self):
        self.prontuarios = []
        for atendimento in self.atendimentos:
            prontuario = Prontuario.objects.create(
                paciente=atendimento.agendamento.paciente,
                tipo_tratamento_definido=atendimento.tipo_tratamento_realizado,
                queixa_principal=self.fake.sentence(),
                historia_doenca_atual=self.fake.paragraph(),
                is_finalized=random.choice([True, False]),
            )
            atendimento.prontuario = prontuario
            atendimento.save()
            self.prontuarios.append(prontuario)
        self.stdout.write(self.style.SUCCESS("Created Prontuarios."))

    def create_lancamentos_financeiros(self):
        self.lancamentos_financeiros = []
        for atendimento in self.atendimentos:
            if random.random() < 0.7: # 70% of attendances have a financial entry
                tipo = random.choice(["RECEITA", "DESPESA"])
                lancamento = LancamentoFinanceiro.objects.create(
                    tipo=tipo,
                    descricao=self.fake.sentence(),
                    valor=self.fake.pydecimal(left_digits=3, right_digits=2, positive=True),
                    data_vencimento=self.fake.date_this_year(),
                    data_pagamento=self.fake.date_this_year() if random.random() < 0.8 else None,
                    atendimento=atendimento,
                )
                self.lancamentos_financeiros.append(lancamento)
        self.stdout.write(self.style.SUCCESS("Created Lancamentos Financeiros."))

    def create_faturas(self):
        self.faturas = []
        for convenio in self.convenios:
            for _ in range(random.randint(1, 3)):
                mes_referencia = self.fake.date_this_year()
                fatura = Fatura.objects.create(
                    convenio=convenio,
                    mes_referencia=mes_referencia,
                    valor_total=self.fake.pydecimal(left_digits=4, right_digits=2, positive=True),
                    status=random.choice(["ABERTA", "FECHADA", "PAGA", "GLOSADA"]),
                )
                # Add some random attendances to the invoice
                atendimentos_fatura = random.sample(
                    self.atendimentos,
                    min(random.randint(1, 5), len(self.atendimentos)),
                )
                fatura.atendimentos.set(atendimentos_fatura)
                self.faturas.append(fatura)
        self.stdout.write(self.style.SUCCESS("Created Faturas."))

    def create_comissoes(self):
        self.comissoes = []
        for atendimento in self.atendimentos:
            if atendimento.agendamento.profissional and random.random() < 0.6: # 60% of attendances generate commission
                comissao = Comissao.objects.create(
                    profissional=atendimento.agendamento.profissional,
                    atendimento=atendimento,
                    valor=self.fake.pydecimal(left_digits=2, right_digits=2, positive=True),
                    paga=random.choice([True, False]),
                )
                self.comissoes.append(comissao)
        self.stdout.write(self.style.SUCCESS("Created Comissoes."))

    def create_leads(self):
        self.leads = []
        origens = ["Google", "Redes Sociais", "Indicação", "Site"]
        for _ in range(15):
            lead = Lead.objects.create(
                nome=self.fake.name(),
                email=self.fake.unique.email(),
                telefone=self.fake.phone_number(),
                origem=random.choice(origens),
                status=random.choice(["NOVO", "CONTATO", "QUALIFICADO", "CONVERTIDO", "PERDIDO"]),
                clinica=self.clinica,
            )
            self.leads.append(lead)
        self.stdout.write(self.style.SUCCESS("Created Leads."))

    def create_campanhas_marketing(self):
        self.campanhas_marketing = []
        tipos = ["SMS", "WHATSAPP", "EMAIL", "OUTRO"]
        for _ in range(5):
            campanha = CampanhaMarketing.objects.create(
                nome=self.fake.catch_phrase(),
                tipo=random.choice(tipos),
                data_inicio=self.fake.date_this_year(),
                data_fim=self.fake.date_this_year() if random.random() < 0.7 else None,
                descricao=self.fake.paragraph(),
                clinica=self.clinica,
            )
            self.campanhas_marketing.append(campanha)
        self.stdout.write(self.style.SUCCESS("Created Campanhas de Marketing."))

    def create_pesquisas_satisfacao(self):
        self.pesquisas_satisfacao = []
        for paciente in random.sample(self.pacientes, min(10, len(self.pacientes))):
            pesquisa = PesquisaSatisfacao.objects.create(
                paciente=paciente,
                nota_nps=random.randint(0, 10),
                comentarios=self.fake.paragraph() if random.random() < 0.7 else "",
                clinica=self.clinica,
            )
            self.pesquisas_satisfacao.append(pesquisa)
        self.stdout.write(self.style.SUCCESS("Created Pesquisas de Satisfacao."))

    def create_cupons_desconto(self):
        self.cupons_desconto = []
        for _ in range(5):
            cupom = CupomDesconto.objects.create(
                codigo=self.fake.unique.word().upper() + str(random.randint(100, 999)),
                valor_desconto=self.fake.pydecimal(left_digits=2, right_digits=2, positive=True),
                data_validade=self.fake.date_this_year(),
                ativo=random.choice([True, False]),
                campanha=random.choice(self.campanhas_marketing) if random.random() < 0.7 else None,
                clinica=self.clinica,
            )
            self.cupons_desconto.append(cupom)
        self.stdout.write(self.style.SUCCESS("Created Cupons de Desconto."))

    def create_documentos(self):
        self.documentos = []
        # Garante que o diretório de upload exista
        upload_dir = os.path.join(settings.MEDIA_ROOT, "uploads", "documentos")
        os.makedirs(upload_dir, exist_ok=True)

        for paciente in random.sample(self.pacientes, min(10, len(self.pacientes))):
            pasta = PastaDocumento.objects.create(
                nome=f"Documentos de {paciente.nome}",
                clinica=self.clinica,
            )
            for _ in range(random.randint(1, 3)):
                doc_file_name = f"{self.fake.word()}.pdf"
                # Crie um ContentFile com conteúdo dummy
                dummy_content = ContentFile(self.fake.text().encode('utf-8'))
                
                documento = DocumentoArquivo.objects.create(
                    pasta=pasta,
                    paciente=paciente,
                    arquivo=dummy_content, # Atribua o ContentFile aqui
                    hash_arquivo=self.fake.sha256(),
                )
                # O nome do arquivo precisa ser definido após a criação do ContentFile
                documento.arquivo.name = os.path.join("uploads", "documentos", doc_file_name)
                documento.save()
                self.documentos.append(documento)
        self.stdout.write(self.style.SUCCESS("Created Documentos."))