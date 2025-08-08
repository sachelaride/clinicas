"""
Database models for the application.

This file defines the SQLAlchemy models for all tables in the database.
"""
from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, ForeignKey, Text, Numeric, UniqueConstraint, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

# Tabela de associação para o relacionamento muitos-para-muitos entre Perfil e Permissao
perfil_permissao = Table('perfil_permissao', Base.metadata,
    Column('perfil_id', Integer, ForeignKey('perfis.id'), primary_key=True),
    Column('permissao_id', Integer, ForeignKey('permissoes.id'), primary_key=True)
)

class Perfil(Base):
    __tablename__ = "perfis"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True, nullable=False)
    permissoes = relationship("Permissao", secondary=perfil_permissao, back_populates="perfis")

class Permissao(Base):
    __tablename__ = "permissoes"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True, nullable=False)
    descricao = Column(String)
    perfis = relationship("Perfil", secondary=perfil_permissao, back_populates="permissoes")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    perfil_id = Column(Integer, ForeignKey("perfis.id"))
    is_active = Column(Boolean, default=True)
    clinica_id = Column(Integer, ForeignKey("clinicas.id"), nullable=True)

    perfil = relationship("Perfil")
    clinica = relationship("Clinica", back_populates="users")
    profissional_profile = relationship("Profissional", back_populates="user", uselist=False)
    
    # Django's AbstractUser fields that might be relevant
    first_name = Column(String, default="")
    last_name = Column(String, default="")
    date_joined = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, default=datetime.utcnow)
    is_superuser = Column(Boolean, default=False)
    is_staff = Column(Boolean, default=False)
    
    # Django's AbstractUser fields that might be relevant
    first_name = Column(String, default="")
    last_name = Column(String, default="")
    date_joined = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, default=datetime.utcnow)
    is_superuser = Column(Boolean, default=False)
    is_staff = Column(Boolean, default=False)

class Clinica(Base):
    __tablename__ = "clinicas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True, index=True, nullable=False)
    endereco = Column(Text, nullable=False)
    telefone = Column(String, default="")
    num_guiches = Column(Integer, default=1)
    tempo_minimo_atendimento = Column(Integer, default=30)

    users = relationship("User", back_populates="clinica")
    tipos_tratamento = relationship("TipoTratamento", back_populates="clinica")
    convenios = relationship("Convenio", back_populates="clinica")
    leads = relationship("Lead", back_populates="clinica")
    campanhas_marketing = relationship("CampanhaMarketing", back_populates="clinica")
    pesquisas_satisfacao = relationship("PesquisaSatisfacao", back_populates="clinica")
    cupons_desconto = relationship("CupomDesconto", back_populates="clinica")
    pastas_documento = relationship("PastaDocumento", back_populates="clinica")


class Paciente(Base):
    __tablename__ = "pacientes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    cpf = Column(String, unique=True, index=True, nullable=False)
    rg = Column(String, default="")
    plano_id = Column(Integer, ForeignKey("planos.id"), nullable=True)
    data_nascimento = Column(Date, nullable=False)
    email = Column(String, unique=True, index=True)
    telefone = Column(String, default="")
    endereco = Column(Text, default="")
    responsavel_legal = Column(String, default="")
    clinica_id = Column(Integer, ForeignKey("clinicas.id"), nullable=True)

    plano = relationship("Plano")
    clinica = relationship("Clinica")
    prontuarios = relationship("Prontuario", back_populates="paciente")
    agendamentos = relationship("Agendamento", back_populates="paciente")
    documentos_arquivo = relationship("DocumentoArquivo", back_populates="paciente")
    pesquisas_satisfacao = relationship("PesquisaSatisfacao", back_populates="paciente")


class Profissional(Base):
    __tablename__ = "profissionais"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    especialidade = Column(String, nullable=False)
    conselho_profissional = Column(String, nullable=False)
    numero_conselho = Column(String, nullable=False)
    carga_horaria_semanal = Column(Integer, default=40)
    comissao_percentual = Column(Numeric(5, 2), default=0.0)

    user = relationship("User", back_populates="profissional_profile")
    agendamentos = relationship("Agendamento", back_populates="profissional")
    comissoes = relationship("Comissao", back_populates="profissional")

class Convenio(Base):
    __tablename__ = "convenios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True, nullable=False)
    clinica_id = Column(Integer, ForeignKey("clinicas.id"), nullable=True)

    clinica = relationship("Clinica", back_populates="convenios")
    planos = relationship("Plano", back_populates="convenio")

class Plano(Base):
    __tablename__ = "planos"

    id = Column(Integer, primary_key=True, index=True)
    convenio_id = Column(Integer, ForeignKey("convenios.id"), nullable=False)
    nome = Column(String, nullable=False)

    convenio = relationship("Convenio", back_populates="planos")
    tabelas_precos = relationship("TabelaPrecos", back_populates="plano")

    __table_args__ = (
        UniqueConstraint('convenio_id', 'nome', name='_convenio_nome_uc'),
    )

class TipoTratamento(Base):
    __tablename__ = "tipos_tratamento"

    id = Column(Integer, primary_key=True, index=True)
    clinica_id = Column(Integer, ForeignKey("clinicas.id"), nullable=False)
    nome = Column(String, nullable=False)
    descricao = Column(Text, default="")
    tempo_minimo_atendimento = Column(Integer, default=30)

    clinica = relationship("Clinica", back_populates="tipos_tratamento")
    prontuarios = relationship("Prontuario", back_populates="tipo_tratamento_definido")
    atendimentos = relationship("Atendimento", back_populates="tipo_tratamento_realizado")
    tabelas_precos = relationship("TabelaPrecos", back_populates="tratamento")

    __table_args__ = (
        UniqueConstraint('clinica_id', 'nome', name='_clinica_nome_uc'),
    )

class Prontuario(Base):
    __tablename__ = "prontuarios"

    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"), nullable=False)
    tipo_tratamento_definido_id = Column(Integer, ForeignKey("tipos_tratamento.id"), nullable=True)
    data_criacao = Column(DateTime, default=datetime.utcnow)
    editavel = Column(Boolean, default=True)
    is_finalized = Column(Boolean, default=False)

    queixa_principal = Column(Text, default="")
    historia_doenca_atual = Column(Text, default="")
    antecedentes_pessoais_familiares = Column(Text, default="")
    habitos_vida = Column(Text, default="")
    uso_medicamentos = Column(Text, default="")
    alergias_conhecidas = Column(Text, default="")

    sinais_vitais = Column(Text, default="")
    exame_fisico_geral_segmentar = Column(Text, default="")
    avaliacoes_especificas = Column(Text, default="")

    hipoteses_diagnosticas = Column(Text, default="")
    exames_complementares = Column(Text, default="")
    conclusao_diagnostica = Column(Text, default="")

    prescricoes = Column(Text, default="")
    encaminhamentos = Column(Text, default="")
    procedimentos_realizados = Column(Text, default="")
    orientacoes_paciente = Column(Text, default="")
    plano_tratamento_acompanhamento = Column(Text, default="")

    evolucao_clinica = Column(Text, default="")

    termo_consentimento = Column(String, default="") # Storing path to file
    fichas_avaliacao_especifica = Column(String, default="") # Storing path to file
    exames_laboratoriais_imagem = Column(String, default="") # Storing path to file
    relatorios_outros_profissionais = Column(String, default="") # Storing path to file

    assinatura_profissional = Column(String, default="")
    registro_profissional = Column(String, default="")

    paciente = relationship("Paciente", back_populates="prontuarios")
    tipo_tratamento_definido = relationship("TipoTratamento", back_populates="prontuarios")
    atendimentos_relacionados = relationship("Atendimento", back_populates="prontuario")

class Agendamento(Base):
    __tablename__ = "agendamentos"

    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"), nullable=False)
    profissional_id = Column(Integer, ForeignKey("profissionais.id"), nullable=True)
    data = Column(DateTime, nullable=False)
    status = Column(String, default="AGENDADO") # AGENDADO, CONCLUIDO, CANCELADO
    guiche_numero = Column(Integer, nullable=True)

    paciente = relationship("Paciente", back_populates="agendamentos")
    profissional = relationship("Profissional", back_populates="agendamentos")
    atendimento = relationship("Atendimento", back_populates="agendamento", uselist=False)

class Atendimento(Base):
    __tablename__ = "atendimentos"

    id = Column(Integer, primary_key=True, index=True)
    agendamento_id = Column(Integer, ForeignKey("agendamentos.id"), nullable=False)
    observacoes = Column(Text, default="")
    data_inicio = Column(DateTime, default=datetime.utcnow)
    data_fim = Column(DateTime, nullable=True)
    status = Column(String, default="INICIADO") # INICIADO, FINALIZADO
    tipo_tratamento_realizado_id = Column(Integer, ForeignKey("tipos_tratamento.id"), nullable=True)
    prontuario_id = Column(Integer, ForeignKey("prontuarios.id"), nullable=True)

    agendamento = relationship("Agendamento", back_populates="atendimento")
    tipo_tratamento_realizado = relationship("TipoTratamento", back_populates="atendimentos")
    prontuario = relationship("Prontuario", back_populates="atendimentos_relacionados")
    lancamentos_financeiros = relationship("LancamentoFinanceiro", back_populates="atendimento")
    comissoes = relationship("Comissao", back_populates="atendimento")
    faturas = relationship("Fatura", secondary="fatura_atendimentos", back_populates="atendimentos")

class PastaDocumento(Base):
    __tablename__ = "pastas_documento"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    clinica_id = Column(Integer, ForeignKey("clinicas.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    clinica = relationship("Clinica", back_populates="pastas_documento")
    documentos_arquivo = relationship("DocumentoArquivo", back_populates="pasta")

class DocumentoArquivo(Base):
    __tablename__ = "documentos_arquivo"

    id = Column(Integer, primary_key=True, index=True)
    pasta_id = Column(Integer, ForeignKey("pastas_documento.id"), nullable=False)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"), nullable=True)
    arquivo = Column(String, nullable=False) # Storing path to file
    hash_arquivo = Column(String, nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)

    pasta = relationship("PastaDocumento", back_populates="documentos_arquivo")
    paciente = relationship("Paciente", back_populates="documentos_arquivo")

class TabelaPrecos(Base):
    __tablename__ = "tabelas_precos"

    id = Column(Integer, primary_key=True, index=True)
    tratamento_id = Column(Integer, ForeignKey("tipos_tratamento.id"), nullable=False)
    plano_id = Column(Integer, ForeignKey("planos.id"), nullable=True)
    preco = Column(Numeric(10, 2), nullable=False)

    tratamento = relationship("TipoTratamento", back_populates="tabelas_precos")
    plano = relationship("Plano", back_populates="tabelas_precos")

    __table_args__ = (
        UniqueConstraint('tratamento_id', 'plano_id', name='_tratamento_plano_uc'),
    )

class LancamentoFinanceiro(Base):
    __tablename__ = "lancamentos_financeiros"

    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String, nullable=False) # RECEITA, DESPESA
    descricao = Column(String, nullable=False)
    valor = Column(Numeric(10, 2), nullable=False)
    data_vencimento = Column(Date, nullable=False)
    data_pagamento = Column(Date, nullable=True)
    atendimento_id = Column(Integer, ForeignKey("atendimentos.id"), nullable=True)

    atendimento = relationship("Atendimento", back_populates="lancamentos_financeiros")

class Fatura(Base):
    __tablename__ = "faturas"

    id = Column(Integer, primary_key=True, index=True)
    convenio_id = Column(Integer, ForeignKey("convenios.id"), nullable=False)
    mes_referencia = Column(Date, nullable=False)
    valor_total = Column(Numeric(10, 2), nullable=False)
    status = Column(String, default="ABERTA") # ABERTA, FECHADA, PAGA, GLOSADA

    convenio = relationship("Convenio")
    atendimentos = relationship("Atendimento", secondary="fatura_atendimentos", back_populates="faturas")

# Association table for Fatura-Atendimento Many-to-Many relationship
from sqlalchemy import Table, Column
from sqlalchemy.schema import ForeignKey

fatura_atendimentos = Table(
    "fatura_atendimentos",
    Base.metadata,
    Column("fatura_id", Integer, ForeignKey("faturas.id"), primary_key=True),
    Column("atendimento_id", Integer, ForeignKey("atendimentos.id"), primary_key=True),
)

class Comissao(Base):
    __tablename__ = "comissoes"

    id = Column(Integer, primary_key=True, index=True)
    profissional_id = Column(Integer, ForeignKey("profissionais.id"), nullable=False)
    atendimento_id = Column(Integer, ForeignKey("atendimentos.id"), nullable=False)
    valor = Column(Numeric(10, 2), nullable=False)
    paga = Column(Boolean, default=False)

    profissional = relationship("Profissional", back_populates="comissoes")
    atendimento = relationship("Atendimento", back_populates="comissoes")

class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, nullable=True)
    telefone = Column(String, nullable=True)
    origem = Column(String, default="")
    status = Column(String, default="NOVO") # NOVO, CONTATO, QUALIFICADO, CONVERTIDO, PERDIDO
    data_criacao = Column(DateTime, default=datetime.utcnow)
    data_atualizacao = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    clinica_id = Column(Integer, ForeignKey("clinicas.id"), nullable=True)

    clinica = relationship("Clinica", back_populates="leads")

class CampanhaMarketing(Base):
    __tablename__ = "campanhas_marketing"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    tipo = Column(String, nullable=False) # SMS, WHATSAPP, EMAIL, OUTRO
    data_inicio = Column(Date, nullable=False)
    data_fim = Column(Date, nullable=True)
    descricao = Column(Text, default="")
    clinica_id = Column(Integer, ForeignKey("clinicas.id"), nullable=True)

    clinica = relationship("Clinica", back_populates="campanhas_marketing")
    cupons_desconto = relationship("CupomDesconto", back_populates="campanha")

class PesquisaSatisfacao(Base):
    __tablename__ = "pesquisas_satisfacao"

    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"), nullable=False)
    data_pesquisa = Column(Date, default=datetime.utcnow)
    nota_nps = Column(Integer, nullable=False) # 0 to 10
    comentarios = Column(Text, default="")
    clinica_id = Column(Integer, ForeignKey("clinicas.id"), nullable=True)

    paciente = relationship("Paciente", back_populates="pesquisas_satisfacao")
    clinica = relationship("Clinica", back_populates="pesquisas_satisfacao")

class CupomDesconto(Base):
    __tablename__ = "cupons_desconto"

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String, unique=True, nullable=False)
    valor_desconto = Column(Numeric(10, 2), nullable=False)
    data_validade = Column(Date, nullable=False)
    ativo = Column(Boolean, default=True)
    campanha_id = Column(Integer, ForeignKey("campanhas_marketing.id"), nullable=True)
    clinica_id = Column(Integer, ForeignKey("clinicas.id"), nullable=True)

    campanha = relationship("CampanhaMarketing", back_populates="cupons_desconto")
    clinica = relationship("Clinica", back_populates="cupons_desconto")
