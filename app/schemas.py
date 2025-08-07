from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import date, datetime
from decimal import Decimal
from enum import Enum

class PermissaoBase(BaseModel):
    nome: str
    descricao: Optional[str] = None

class PermissaoCreate(PermissaoBase):
    pass

class PermissaoUpdate(PermissaoBase):
    pass

class PermissaoInDBBase(PermissaoBase):
    id: int

    class Config:
        orm_mode = True

class PerfilBase(BaseModel):
    nome: str

class PerfilCreate(PerfilBase):
    pass

class PerfilUpdate(PerfilBase):
    permissoes: Optional[List[int]] = None

class PerfilInDBBase(PerfilBase):
    id: int
    permissoes: List[PermissaoInDBBase] = []

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    username: str
    email: Optional[EmailStr] = None
    perfil_id: Optional[int] = None
    clinica_id: Optional[int] = None
    first_name: Optional[str] = ""
    last_name: Optional[str] = ""
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_staff: Optional[bool] = False

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None

class UserInDBBase(UserBase):
    id: int
    date_joined: datetime
    last_login: Optional[datetime] = None
    perfil: PerfilInDBBase # Adicionado para carregar o objeto Perfil

    class Config:
        orm_mode = True

class ClinicaBase(BaseModel):
    nome: str
    endereco: str
    telefone: Optional[str] = None
    num_guiches: Optional[int] = 1
    tempo_minimo_atendimento: Optional[int] = 30

class ClinicaCreate(ClinicaBase):
    pass

class ClinicaUpdate(ClinicaBase):
    pass

class ClinicaInDBBase(ClinicaBase):
    id: int

    class Config:
        orm_mode = True

class PacienteBase(BaseModel):
    nome: str
    cpf: str
    rg: Optional[str] = None
    plano_id: Optional[int] = None
    data_nascimento: date
    email: Optional[EmailStr] = None
    telefone: Optional[str] = None
    endereco: Optional[str] = None
    responsavel_legal: Optional[str] = None
    clinica_id: Optional[int] = None

class PacienteCreate(PacienteBase):
    pass

class PacienteUpdate(PacienteBase):
    pass

class PacienteInDBBase(PacienteBase):
    id: int

    class Config:
        orm_mode = True

class ProfissionalBase(BaseModel):
    user_id: int
    especialidade: str
    conselho_profissional: str
    numero_conselho: str
    carga_horaria_semanal: Optional[int] = 40
    comissao_percentual: Optional[Decimal] = Field(default=0.0, decimal_places=2, max_digits=5)

class ProfissionalCreate(ProfissionalBase):
    pass

class ProfissionalUpdate(ProfissionalBase):
    pass

class ProfissionalInDBBase(ProfissionalBase):
    id: int

    class Config:
        orm_mode = True

class ConvenioBase(BaseModel):
    nome: str
    clinica_id: Optional[int] = None

class ConvenioCreate(ConvenioBase):
    pass

class ConvenioUpdate(ConvenioBase):
    pass

class ConvenioInDBBase(ConvenioBase):
    id: int

    class Config:
        orm_mode = True

class PlanoBase(BaseModel):
    convenio_id: int
    nome: str

class PlanoCreate(PlanoBase):
    pass

class PlanoUpdate(PlanoBase):
    pass

class PlanoInDBBase(PlanoBase):
    id: int

    class Config:
        orm_mode = True

class TipoTratamentoBase(BaseModel):
    clinica_id: int
    nome: str
    descricao: Optional[str] = None
    tempo_minimo_atendimento: Optional[int] = 30

class TipoTratamentoCreate(TipoTratamentoBase):
    pass

class TipoTratamentoUpdate(TipoTratamentoBase):
    pass

class TipoTratamentoInDBBase(TipoTratamentoBase):
    id: int

    class Config:
        orm_mode = True

class ProntuarioBase(BaseModel):
    paciente_id: int
    tipo_tratamento_definido_id: Optional[int] = None
    editavel: Optional[bool] = True
    is_finalized: Optional[bool] = False
    queixa_principal: Optional[str] = None
    historia_doenca_atual: Optional[str] = None
    antecedentes_pessoais_familiares: Optional[str] = None
    habitos_vida: Optional[str] = None
    uso_medicamentos: Optional[str] = None
    alergias_conhecidas: Optional[str] = None
    sinais_vitais: Optional[str] = None
    exame_fisico_geral_segmentar: Optional[str] = None
    avaliacoes_especificas: Optional[str] = None
    hipoteses_diagnosticas: Optional[str] = None
    exames_complementares: Optional[str] = None
    conclusao_diagnostica: Optional[str] = None
    prescricoes: Optional[str] = None
    encaminhamentos: Optional[str] = None
    procedimentos_realizados: Optional[str] = None
    orientacoes_paciente: Optional[str] = None
    plano_tratamento_acompanhamento: Optional[str] = None
    evolucao_clinica: Optional[str] = None
    termo_consentimento: Optional[str] = None
    fichas_avaliacao_especifica: Optional[str] = None
    exames_laboratoriais_imagem: Optional[str] = None
    relatorios_outros_profissionais: Optional[str] = None
    assinatura_profissional: Optional[str] = None
    registro_profissional: Optional[str] = None

class ProntuarioCreate(ProntuarioBase):
    pass

class ProntuarioUpdate(ProntuarioBase):
    pass

class ProntuarioInDBBase(ProntuarioBase):
    id: int
    data_criacao: datetime

    class Config:
        orm_mode = True

class AgendamentoStatusEnum(str, Enum):
    AGENDADO = "AGENDADO"
    CONCLUIDO = "CONCLUIDO"
    CANCELADO = "CANCELADO"

class AgendamentoBase(BaseModel):
    paciente_id: int
    profissional_id: Optional[int] = None
    data: datetime
    status: AgendamentoStatusEnum = AgendamentoStatusEnum.AGENDADO
    guiche_numero: Optional[int] = None

class AgendamentoCreate(AgendamentoBase):
    pass

class AgendamentoUpdate(AgendamentoBase):
    pass

class AgendamentoInDBBase(AgendamentoBase):
    id: int

    class Config:
        orm_mode = True

class AtendimentoStatusEnum(str, Enum):
    INICIADO = "INICIADO"
    FINALIZADO = "FINALIZADO"

class AtendimentoBase(BaseModel):
    agendamento_id: int
    observacoes: Optional[str] = None
    data_fim: Optional[datetime] = None
    status: AtendimentoStatusEnum = AtendimentoStatusEnum.INICIADO
    tipo_tratamento_realizado_id: Optional[int] = None
    prontuario_id: Optional[int] = None

class AtendimentoCreate(AtendimentoBase):
    pass

class AtendimentoUpdate(AtendimentoBase):
    pass

class AtendimentoInDBBase(AtendimentoBase):
    id: int
    data_inicio: datetime

    class Config:
        orm_mode = True

class PastaDocumentoBase(BaseModel):
    nome: str
    clinica_id: int

class PastaDocumentoCreate(PastaDocumentoBase):
    pass

class PastaDocumentoUpdate(PastaDocumentoBase):
    pass

class PastaDocumentoInDBBase(PastaDocumentoBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class DocumentoArquivoBase(BaseModel):
    pasta_id: int
    paciente_id: Optional[int] = None
    arquivo: str
    hash_arquivo: str

class DocumentoArquivoCreate(DocumentoArquivoBase):
    pass

class DocumentoArquivoUpdate(DocumentoArquivoBase):
    pass

class DocumentoArquivoInDBBase(DocumentoArquivoBase):
    id: int
    uploaded_at: datetime

    class Config:
        orm_mode = True

class TabelaPrecosBase(BaseModel):
    tratamento_id: int
    plano_id: Optional[int] = None
    preco: Decimal = Field(decimal_places=2, max_digits=10)

class TabelaPrecosCreate(TabelaPrecosBase):
    pass

class TabelaPrecosUpdate(TabelaPrecosBase):
    pass

class TabelaPrecosInDBBase(TabelaPrecosBase):
    id: int

    class Config:
        orm_mode = True

class LancamentoFinanceiroTipoEnum(str, Enum):
    RECEITA = "RECEITA"
    DESPESA = "DESPESA"

class LancamentoFinanceiroBase(BaseModel):
    tipo: LancamentoFinanceiroTipoEnum
    descricao: str
    valor: Decimal = Field(decimal_places=2, max_digits=10)
    data_vencimento: date
    data_pagamento: Optional[date] = None
    atendimento_id: Optional[int] = None

class LancamentoFinanceiroCreate(LancamentoFinanceiroBase):
    pass

class LancamentoFinanceiroUpdate(LancamentoFinanceiroBase):
    pass

class LancamentoFinanceiroInDBBase(LancamentoFinanceiroBase):
    id: int

    class Config:
        orm_mode = True

class FaturaStatusEnum(str, Enum):
    ABERTA = "ABERTA"
    FECHADA = "FECHADA"
    PAGA = "PAGA"
    GLOSADA = "GLOSADA"

class FaturaBase(BaseModel):
    convenio_id: int
    mes_referencia: date
    valor_total: Decimal = Field(decimal_places=2, max_digits=10)
    status: FaturaStatusEnum = FaturaStatusEnum.ABERTA

class FaturaCreate(FaturaBase):
    pass

class FaturaUpdate(FaturaBase):
    pass

class FaturaInDBBase(FaturaBase):
    id: int

    class Config:
        orm_mode = True

class ComissaoBase(BaseModel):
    profissional_id: int
    atendimento_id: int
    valor: Decimal = Field(decimal_places=2, max_digits=10)
    paga: Optional[bool] = False

class ComissaoCreate(ComissaoBase):
    pass

class ComissaoUpdate(ComissaoBase):
    pass

class ComissaoInDBBase(ComissaoBase):
    id: int

    class Config:
        orm_mode = True

class LeadStatusEnum(str, Enum):
    NOVO = "NOVO"
    CONTATO = "CONTATO"
    QUALIFICADO = "QUALIFICADO"
    CONVERTIDO = "CONVERTIDO"
    PERDIDO = "PERDIDO"

class LeadBase(BaseModel):
    nome: str
    email: Optional[EmailStr] = None
    telefone: Optional[str] = None
    origem: Optional[str] = None
    status: LeadStatusEnum = LeadStatusEnum.NOVO
    clinica_id: Optional[int] = None

class LeadCreate(LeadBase):
    pass

class LeadUpdate(LeadBase):
    pass

class LeadInDBBase(LeadBase):
    id: int
    data_criacao: datetime
    data_atualizacao: datetime

    class Config:
        orm_mode = True

class CampanhaMarketingTipoEnum(str, Enum):
    SMS = "SMS"
    WHATSAPP = "WHATSAPP"
    EMAIL = "EMAIL"
    OUTRO = "OUTRO"

class CampanhaMarketingBase(BaseModel):
    nome: str
    tipo: CampanhaMarketingTipoEnum
    data_inicio: date
    data_fim: Optional[date] = None
    descricao: Optional[str] = None
    clinica_id: Optional[int] = None

class CampanhaMarketingCreate(CampanhaMarketingBase):
    pass

class CampanhaMarketingUpdate(CampanhaMarketingBase):
    pass

class CampanhaMarketingInDBBase(CampanhaMarketingBase):
    id: int

    class Config:
        orm_mode = True

class PesquisaSatisfacaoBase(BaseModel):
    paciente_id: int
    nota_nps: int = Field(ge=0, le=10)
    comentarios: Optional[str] = None
    clinica_id: Optional[int] = None

class PesquisaSatisfacaoCreate(PesquisaSatisfacaoBase):
    pass

class PesquisaSatisfacaoUpdate(PesquisaSatisfacaoBase):
    pass

class PesquisaSatisfacaoInDBBase(PesquisaSatisfacaoBase):
    id: int
    data_pesquisa: date

    class Config:
        orm_mode = True

class CupomDescontoBase(BaseModel):
    codigo: str
    valor_desconto: Decimal = Field(decimal_places=2, max_digits=10)
    data_validade: date
    ativo: Optional[bool] = True
    campanha_id: Optional[int] = None
    clinica_id: Optional[int] = None

class CupomDescontoCreate(CupomDescontoBase):
    pass

class CupomDescontoUpdate(CupomDescontoBase):
    pass

class CupomDescontoInDBBase(CupomDescontoBase):
    id: int

    class Config:
        orm_mode = True

# Schemas for relationships (read-only, nested)
class Clinica(ClinicaInDBBase):
    users: List[UserInDBBase] = []
    tipos_tratamento: List[TipoTratamentoInDBBase] = []
    convenios: List[ConvenioInDBBase] = []
    leads: List[LeadInDBBase] = []
    campanhas_marketing: List[CampanhaMarketingInDBBase] = []
    pesquisas_satisfacao: List[PesquisaSatisfacaoInDBBase] = []
    cupons_desconto: List[CupomDescontoInDBBase] = []
    pastas_documento: List[PastaDocumentoInDBBase] = []

class User(UserInDBBase):
    clinica: Optional[ClinicaInDBBase] = None
    profissional_profile: Optional[ProfissionalInDBBase] = None
    perfil: PerfilInDBBase # Adicionado para carregar o objeto Perfil

class Profissional(ProfissionalInDBBase):
    user: UserInDBBase
    agendamentos: List[AgendamentoInDBBase] = []
    comissoes: List[ComissaoInDBBase] = []

class Paciente(PacienteInDBBase):
    plano: Optional[PlanoInDBBase] = None
    clinica: Optional[ClinicaInDBBase] = None
    prontuarios: List[ProntuarioInDBBase] = []
    agendamentos: List[AgendamentoInDBBase] = []
    documentos_arquivo: List[DocumentoArquivoInDBBase] = []
    pesquisas_satisfacao: List[PesquisaSatisfacaoInDBBase] = []

class Convenio(ConvenioInDBBase):
    clinica: Optional[ClinicaInDBBase] = None
    planos: List[PlanoInDBBase] = []

class Plano(PlanoInDBBase):
    convenio: ConvenioInDBBase
    tabelas_precos: List[TabelaPrecosInDBBase] = []

class TipoTratamento(TipoTratamentoInDBBase):
    clinica: ClinicaInDBBase
    prontuarios: List[ProntuarioInDBBase] = []
    atendimentos: List[AtendimentoInDBBase] = []
    tabelas_precos: List[TabelaPrecosInDBBase] = []

class Prontuario(ProntuarioInDBBase):
    paciente: PacienteInDBBase
    tipo_tratamento_definido: Optional[TipoTratamentoInDBBase] = None
    atendimentos_relacionados: List[AtendimentoInDBBase] = []

class Agendamento(AgendamentoInDBBase):
    paciente: PacienteInDBBase
    profissional: Optional[ProfissionalInDBBase] = None
    atendimento: Optional[AtendimentoInDBBase] = None

class Atendimento(AtendimentoInDBBase):
    agendamento: AgendamentoInDBBase
    tipo_tratamento_realizado: Optional[TipoTratamentoInDBBase] = None
    prontuario: Optional[ProntuarioInDBBase] = None
    lancamentos_financeiros: List[LancamentoFinanceiroInDBBase] = []
    comissoes: List[ComissaoInDBBase] = []
    faturas: List[FaturaInDBBase] = []

class PastaDocumento(PastaDocumentoInDBBase):
    clinica: ClinicaInDBBase
    documentos_arquivo: List[DocumentoArquivoInDBBase] = []

class DocumentoArquivo(DocumentoArquivoInDBBase):
    pasta: PastaDocumentoInDBBase
    paciente: Optional[PacienteInDBBase] = None

class TabelaPrecos(TabelaPrecosInDBBase):
    tratamento: TipoTratamentoInDBBase
    plano: Optional[PlanoInDBBase] = None

class LancamentoFinanceiro(LancamentoFinanceiroInDBBase):
    atendimento: Optional[AtendimentoInDBBase] = None

class Fatura(FaturaInDBBase):
    convenio: ConvenioInDBBase
    atendimentos: List[AtendimentoInDBBase] = []

class Comissao(ComissaoInDBBase):
    profissional: ProfissionalInDBBase
    atendimento: AtendimentoInDBBase

class Lead(LeadInDBBase):
    clinica: Optional[ClinicaInDBBase] = None

class CampanhaMarketing(CampanhaMarketingInDBBase):
    clinica: Optional[ClinicaInDBBase] = None
    cupons_desconto: List[CupomDescontoInDBBase] = []

class PesquisaSatisfacao(PesquisaSatisfacaoInDBBase):
    paciente: PacienteInDBBase
    clinica: Optional[ClinicaInDBBase] = None

class CupomDesconto(CupomDescontoInDBBase):
    campanha: Optional[CampanhaMarketingInDBBase] = None
    clinica: Optional[ClinicaInDBBase] = None

class Token(BaseModel):
    access_token: str
    token_type: str

class LoginRequest(BaseModel):
    username: str
    password: str
    clinic_id: Optional[int] = None