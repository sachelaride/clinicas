"""Módulo que define os modelos de dados para a aplicação de clínica."""

# Importa módulos do Django para modelos
from django.db import models
# Importa configurações do projeto Django
from django.conf import settings
# Importa o modelo de usuário abstrato do Django para estender
from django.contrib.auth.models import AbstractUser
# Importa validador de expressão regular para campos de modelo
from django.core.validators import RegexValidator
# Importa hashlib para cálculo de hash SHA-256 para verificação de integridade de arquivos
import hashlib
# Importa o módulo os para operações de sistema de arquivos
import os
# Importa datetime para manipulação de datas e horas
from datetime import datetime
# Importa funções de utilidade para o caminho de upload de arquivos dinâmico
from .utils import documento_upload_path, prontuario_upload_path
from django.contrib.auth import get_user_model # Importar o modelo de usuário


class Convenio(models.Model):
    """Modelo que representa um convênio médico."""
    nome = models.CharField(max_length=100, unique=True)
    clinica = models.ForeignKey('Clinica', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.nome

class Plano(models.Model):
    """Modelo que representa um plano de um convênio."""
    convenio = models.ForeignKey(Convenio, on_delete=models.CASCADE, related_name='planos')
    nome = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.convenio.nome} - {self.nome}"

    class Meta:
        unique_together = ('convenio', 'nome')


class Prontuario(models.Model):
    """Modelo que representa um prontuário médico de um paciente."""
    paciente = models.ForeignKey('Paciente', on_delete=models.CASCADE, related_name='prontuarios')
    tipo_tratamento_definido = models.ForeignKey('TipoTratamento', on_delete=models.SET_NULL, null=True, blank=True, help_text="O tipo de tratamento geral definido para este prontuário.")
    data_criacao = models.DateTimeField(auto_now_add=True)
    editavel = models.BooleanField(default=True)
    is_finalized = models.BooleanField(default=False, help_text="Indica se o prontuário foi finalizado.")

    # Histórico Clínico
    queixa_principal = models.TextField(blank=True)
    historia_doenca_atual = models.TextField(blank=True)
    antecedentes_pessoais_familiares = models.TextField(blank=True)
    habitos_vida = models.TextField(blank=True, help_text="Tabagismo, etilismo, sono, atividade física, alimentação")
    uso_medicamentos = models.TextField(blank=True)
    alergias_conhecidas = models.TextField(blank=True)

    # Exame Físico e Avaliações
    sinais_vitais = models.TextField(blank=True, help_text="Pressão arterial, temperatura, frequência cardíaca, etc.")
    exame_fisico_geral_segmentar = models.TextField(blank=True)
    avaliacoes_especificas = models.TextField(blank=True, help_text="Exames odontológicos, psicológicos, ortopédicos")

    # Diagnóstico
    hipoteses_diagnosticas = models.TextField(blank=True, help_text="CID-10, se possível")
    exames_complementares = models.TextField(blank=True, help_text="Solicitados ou realizados")
    conclusao_diagnostica = models.TextField(blank=True)

    # Conduta e Plano Terapêutico
    prescricoes = models.TextField(blank=True, help_text="Receituário")
    encaminhamentos = models.TextField(blank=True)
    procedimentos_realizados = models.TextField(blank=True)
    orientacoes_paciente = models.TextField(blank=True)
    plano_tratamento_acompanhamento = models.TextField(blank=True)

    # Evolução Clínica
    evolucao_clinica = models.TextField(blank=True, help_text="Registro das consultas subsequentes, alterações no quadro, etc.")

    # Termos e Documentos Anexos
    termo_consentimento = models.FileField(upload_to=prontuario_upload_path, null=True, blank=True)
    fichas_avaliacao_especifica = models.FileField(upload_to=prontuario_upload_path, null=True, blank=True)
    exames_laboratoriais_imagem = models.FileField(upload_to=prontuario_upload_path, null=True, blank=True)
    relatorios_outros_profissionais = models.FileField(upload_to=prontuario_upload_path, null=True, blank=True)

    # Assinaturas e Responsabilidade Técnica
    assinatura_profissional = models.CharField(max_length=100, blank=True)
    registro_profissional = models.CharField(max_length=50, blank=True)


    def save(self, *args, **kwargs):
        """Sobrescreve o método save para definir o prontuário como não editável após a primeira vez."""
        if self.is_finalized:
            self.editavel = False
        super().save(*args, **kwargs)

    class Meta:
        """Opções de metadados para o modelo Prontuario."""
        verbose_name = 'Prontuário'
        verbose_name_plural = 'Prontuários'

    def __str__(self):
        """Retorna uma representação em string do prontuário."""
        return f"Prontuário de {self.paciente} - {self.data_criacao}"


from django.contrib.auth.models import Group


class User(AbstractUser):
    """Modelo de usuário personalizado que estende o AbstractUser do Django."""
    PERFIL_CHOICES = (
        ('ADMIN', 'Administrador'),
        ('ATENDENTE', 'Atendente'),
        ('PROFISSIONAL', 'Profissional da Saúde'),
        ('COORDENADOR', 'Coordenador'),
        ('PACIENTE', 'Paciente'),
    )
    perfil = models.CharField(max_length=20, choices=PERFIL_CHOICES, blank=True)
    clinica = models.ForeignKey('Clinica', on_delete=models.SET_NULL, null=True, blank=True)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='clinica_user_groups',
        blank=True,
        help_text='The groups this user belongs to.',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='clinica_user_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.perfil:
            group_name = self.get_perfil_display()
            group, created = Group.objects.get_or_create(name=group_name)
            self.groups.add(group)

    def __str__(self):
        return f"{self.username} ({self.get_perfil_display()})"


class Profissional(models.Model):
    """Modelo que representa os dados de um profissional da saúde."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profissional_profile')
    especialidade = models.CharField(max_length=100)
    conselho_profissional = models.CharField(max_length=20, help_text="Ex: CRM, COREN, etc.")
    numero_conselho = models.CharField(max_length=20)
    carga_horaria_semanal = models.PositiveIntegerField(default=40)
    comissao_percentual = models.DecimalField(max_digits=5, decimal_places=2, default=0.0, help_text="Percentual de comissão por atendimento.")

    def __str__(self):
        return self.user.username


class Clinica(models.Model):
    """Modelo que representa uma clínica no sistema."""
    nome = models.CharField(max_length=100)
    endereco = models.TextField()
    telefone = models.CharField(max_length=25, blank=True)
    num_guiches = models.PositiveIntegerField(default=1, help_text="Número de guichês de atendimento disponíveis nesta clínica.")
    tempo_minimo_atendimento = models.PositiveIntegerField(default=30, help_text="Tempo mínimo de atendimento em minutos.")

    def __str__(self):
        return self.nome


class Paciente(models.Model):
    """Modelo que representa um paciente no sistema da clínica."""
    nome = models.CharField(max_length=100)
    cpf = models.CharField(
        max_length=14,
        unique=True,
        validators=[RegexValidator(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$', 'CPF deve estar no formato XXX.XXX.XXX-XX')]
    )
    rg = models.CharField(max_length=20, blank=True)
    plano = models.ForeignKey(Plano, on_delete=models.SET_NULL, null=True, blank=True)
    data_nascimento = models.DateField()
    email = models.EmailField(unique=True, blank=True, null=True)
    telefone = models.CharField(max_length=25, blank=True)
    endereco = models.TextField(blank=True)
    responsavel_legal = models.CharField(max_length=100, blank=True)
    clinica = models.ForeignKey('Clinica', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        User = get_user_model()
        cleaned_cpf = self.cpf.replace('.', '').replace('-', '')
        
        # Tenta encontrar um usuário existente com o CPF como username
        try:
            user = User.objects.get(username=cleaned_cpf)
            # Se o usuário existe, garante que o perfil é PACIENTE
            if user.perfil != 'PACIENTE':
                user.perfil = 'PACIENTE'
                user.save()
        except User.DoesNotExist:
            # Se o usuário não existe, cria um novo
            user = User.objects.create_user(
                username=cleaned_cpf,
                password=cleaned_cpf, # Senha padrão é o próprio CPF
                email=self.email, # Usa o email do paciente
                perfil='PACIENTE',
                clinica=self.clinica, # Vincula à clínica do paciente
            )
        super(Paciente, self).save(*args, **kwargs)


class Agendamento(models.Model):
    """Modelo que representa um agendamento de consulta ou procedimento."""
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    profissional = models.ForeignKey(Profissional, on_delete=models.CASCADE, null=True, blank=True)
    data = models.DateTimeField()
    status = models.CharField(
        max_length=20,
        choices=[('AGENDADO', 'Agendado'), ('CONCLUIDO', 'Concluído'), ('CANCELADO', 'Cancelado')],
        default='AGENDADO'
    )
    guiche_numero = models.PositiveIntegerField(null=True, blank=True, help_text="Número do guichê atribuído para este agendamento.")

    def __str__(self):
        return f"Agendamento de {self.paciente.nome} com {self.profissional.user.username} em {self.data}"


class Atendimento(models.Model):
    """Modelo que representa um atendimento realizado na clínica."""
    agendamento = models.ForeignKey(Agendamento, on_delete=models.CASCADE)
    observacoes = models.TextField(blank=True)
    data_inicio = models.DateTimeField(auto_now_add=True)
    data_fim = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[('INICIADO', 'Iniciado'), ('FINALIZADO', 'Finalizado')],
        default='INICIADO'
    )
    tipo_tratamento_realizado = models.ForeignKey('TipoTratamento', on_delete=models.SET_NULL, null=True, blank=True, help_text="O tipo de tratamento realizado neste atendimento.")
    prontuario = models.ForeignKey('Prontuario', on_delete=models.SET_NULL, null=True, blank=True, related_name='atendimentos_relacionados')

    def __str__(self):
        return f"Atendimento de {self.agendamento.paciente.nome} por {self.agendamento.profissional.user.username}"


class PastaDocumento(models.Model):
    """Modelo que representa uma pasta para organizar documentos."""
    nome = models.CharField(max_length=100)
    clinica = models.ForeignKey(Clinica, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome


class DocumentoArquivo(models.Model):
    """Modelo que representa um arquivo de documento anexado no sistema."""
    pasta = models.ForeignKey(PastaDocumento, on_delete=models.CASCADE)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, null=True)
    arquivo = models.FileField(upload_to=documento_upload_path)
    hash_arquivo = models.CharField(max_length=64)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.arquivo:
            self.hash_arquivo = self.calculate_hash()
        super().save(*args, **kwargs)

    def calculate_hash(self):
        sha256 = hashlib.sha256()
        for chunk in self.arquivo.chunks():
            sha256.update(chunk)
        return sha256.hexdigest()

    def __str__(self):
        return f"Arquivo em {self.pasta.nome}"


class TipoTratamento(models.Model):
    """Modelo para definir os tipos de tratamento oferecidos por uma clínica."""
    clinica = models.ForeignKey(Clinica, on_delete=models.CASCADE, related_name='tipos_tratamento')
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    tempo_minimo_atendimento = models.PositiveIntegerField(default=30, help_text="Tempo mínimo de atendimento em minutos.")

    def __str__(self):
        return f"{self.nome} ({self.clinica.nome})"

    class Meta:
        unique_together = ('clinica', 'nome')
        verbose_name = 'Tipo de Tratamento'
        verbose_name_plural = 'Tipos de Tratamento'


class TabelaPrecos(models.Model):
    """Tabela de preços para procedimentos, por convênio e particular."""
    tratamento = models.ForeignKey(TipoTratamento, on_delete=models.CASCADE, related_name='precos')
    plano = models.ForeignKey(Plano, on_delete=models.CASCADE, null=True, blank=True, help_text="Deixe em branco para preço particular.")
    preco = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('tratamento', 'plano')
        verbose_name = 'Tabela de Preço'
        verbose_name_plural = 'Tabelas de Preços'

    def __str__(self):
        if self.plano:
            return f"{self.tratamento.nome} ({self.plano}): R$ {self.preco}"
        return f"{self.tratamento.nome} (Particular): R$ {self.preco}"


class LancamentoFinanceiro(models.Model):
    """Modelo para registrar lançamentos financeiros (contas a pagar e a receber)."""
    TIPO_CHOICES = (
        ('RECEITA', 'Receita'),
        ('DESPESA', 'Despesa'),
    )
    tipo = models.CharField(max_length=7, choices=TIPO_CHOICES)
    descricao = models.CharField(max_length=255)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_vencimento = models.DateField()
    data_pagamento = models.DateField(null=True, blank=True)
    atendimento = models.ForeignKey(Atendimento, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.get_tipo_display()}: {self.descricao} - R$ {self.valor}"


class Fatura(models.Model):
    """Modelo para faturas de convênios."""
    convenio = models.ForeignKey(Convenio, on_delete=models.CASCADE)
    mes_referencia = models.DateField()
    atendimentos = models.ManyToManyField(Atendimento)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[
        ('ABERTA', 'Aberta'),
        ('FECHADA', 'Fechada'),
        ('PAGA', 'Paga'),
        ('GLOSADA', 'Glosada'),
    ], default='ABERTA')

    def __str__(self):
        return f"Fatura {self.convenio.nome} - {self.mes_referencia.strftime('%m/%Y')}"


class Comissao(models.Model):
    """Modelo para registrar comissões de profissionais."""
    profissional = models.ForeignKey(Profissional, on_delete=models.CASCADE)
    atendimento = models.ForeignKey(Atendimento, on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    paga = models.BooleanField(default=False)

    def __str__(self):
        return f"Comissão de {self.profissional.user.username} para o atendimento {self.atendimento.id}"


class Lead(models.Model):
    """Modelo para gerenciar leads e seu funil de conversão."""
    STATUS_CHOICES = (
        ('NOVO', 'Novo'),
        ('CONTATO', 'Em Contato'),
        ('QUALIFICADO', 'Qualificado'),
        ('CONVERTIDO', 'Convertido'),
        ('PERDIDO', 'Perdido'),
    )
    nome = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    telefone = models.CharField(max_length=25, blank=True, null=True)
    origem = models.CharField(max_length=100, blank=True, help_text="Ex: Google, Redes Sociais, Indicação")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NOVO')
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    clinica = models.ForeignKey('Clinica', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.nome


class CampanhaMarketing(models.Model):
    """Modelo para registrar campanhas de marketing."""
    TIPO_CHOICES = (
        ('SMS', 'SMS'),
        ('WHATSAPP', 'WhatsApp'),
        ('EMAIL', 'E-mail Marketing'),
        ('OUTRO', 'Outro'),
    )
    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    data_inicio = models.DateField()
    data_fim = models.DateField(null=True, blank=True)
    descricao = models.TextField(blank=True)
    clinica = models.ForeignKey('Clinica', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.nome


class PesquisaSatisfacao(models.Model):
    """Modelo para gerenciar pesquisas de satisfação (NPS)."""
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    data_pesquisa = models.DateField(auto_now_add=True)
    nota_nps = models.IntegerField(choices=[(i, str(i)) for i in range(0, 11)], help_text="Nota de 0 a 10 para o NPS.")
    comentarios = models.TextField(blank=True)
    clinica = models.ForeignKey('Clinica', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Pesquisa de {self.paciente.nome} - NPS: {self.nota_nps}"


class CupomDesconto(models.Model):
    """Modelo para gerenciar cupons de desconto."""
    codigo = models.CharField(max_length=50, unique=True)
    valor_desconto = models.DecimalField(max_digits=10, decimal_places=2)
    data_validade = models.DateField()
    ativo = models.BooleanField(default=True)
    campanha = models.ForeignKey(CampanhaMarketing, on_delete=models.SET_NULL, null=True, blank=True)
    clinica = models.ForeignKey('Clinica', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.codigo