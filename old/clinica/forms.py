from django import forms
from .models import User, Clinica, Paciente, Agendamento, Atendimento, PastaDocumento, DocumentoArquivo, Prontuario, TipoTratamento, Profissional, LancamentoFinanceiro, Fatura, Comissao, Lead, CampanhaMarketing, PesquisaSatisfacao, CupomDesconto


class ProntuarioForm(forms.ModelForm):
    class Meta:
        model = Prontuario
        fields = ['paciente', 'tipo_tratamento_definido', 'queixa_principal', 'historia_doenca_atual', 'antecedentes_pessoais_familiares', 'habitos_vida', 'uso_medicamentos', 'alergias_conhecidas', 'sinais_vitais', 'exame_fisico_geral_segmentar', 'avaliacoes_especificas', 'hipoteses_diagnosticas', 'exames_complementares', 'conclusao_diagnostica', 'prescricoes', 'encaminhamentos', 'procedimentos_realizados', 'orientacoes_paciente', 'plano_tratamento_acompanhamento', 'evolucao_clinica', 'termo_consentimento', 'fichas_avaliacao_especifica', 'exames_laboratoriais_imagem', 'relatorios_outros_profissionais', 'assinatura_profissional', 'registro_profissional', 'is_finalized']
        widgets = {
            'queixa_principal': forms.Textarea(attrs={'rows': 3}),
            'historia_doenca_atual': forms.Textarea(attrs={'rows': 3}),
            'antecedentes_pessoais_familiares': forms.Textarea(attrs={'rows': 3}),
            'habitos_vida': forms.Textarea(attrs={'rows': 3}),
            'uso_medicamentos': forms.Textarea(attrs={'rows': 3}),
            'alergias_conhecidas': forms.Textarea(attrs={'rows': 3}),
            'sinais_vitais': forms.Textarea(attrs={'rows': 3}),
            'exame_fisico_geral_segmentar': forms.Textarea(attrs={'rows': 3}),
            'avaliacoes_especificas': forms.Textarea(attrs={'rows': 3}),
            'hipoteses_diagnosticas': forms.Textarea(attrs={'rows': 3}),
            'exames_complementares': forms.Textarea(attrs={'rows': 3}),
            'conclusao_diagnostica': forms.Textarea(attrs={'rows': 3}),
            'prescricoes': forms.Textarea(attrs={'rows': 3}),
            'encaminhamentos': forms.Textarea(attrs={'rows': 3}),
            'procedimentos_realizados': forms.Textarea(attrs={'rows': 3}),
            'orientacoes_paciente': forms.Textarea(attrs={'rows': 3}),
            'plano_tratamento_acompanhamento': forms.Textarea(attrs={'rows': 3}),
            'evolucao_clinica': forms.Textarea(attrs={'rows': 3}),
        }


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'perfil', 'clinica', 'password']
        widgets = {'password': forms.PasswordInput()}


class ClinicaForm(forms.ModelForm):
    class Meta:
        model = Clinica
        fields = ['nome', 'endereco', 'telefone', 'num_guiches', 'tempo_minimo_atendimento']


class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['nome', 'cpf', 'rg', 'plano', 'data_nascimento', 'email', 'telefone', 'endereco', 'responsavel_legal']
        widgets = {'data_nascimento': forms.DateInput(attrs={'type': 'date'})}


class AgendamentoForm(forms.ModelForm):
    class Meta:
        model = Agendamento
        fields = ['paciente', 'profissional', 'data', 'guiche_numero', 'status']
        widgets = {'data': forms.DateTimeInput(attrs={'type': 'datetime-local'})}


class AtendimentoForm(forms.ModelForm):
    class Meta:
        model = Atendimento
        fields = ['agendamento', 'observacoes', 'status', 'tipo_tratamento_realizado', 'prontuario']


class PastaDocumentoForm(forms.ModelForm):
    class Meta:
        model = PastaDocumento
        fields = ['nome', 'clinica']


class DocumentoArquivoForm(forms.ModelForm):
    class Meta:
        model = DocumentoArquivo
        fields = ['pasta', 'paciente', 'arquivo']


class TipoTratamentoForm(forms.ModelForm):
    class Meta:
        model = TipoTratamento
        fields = ['clinica', 'nome', 'descricao']


class LancamentoFinanceiroForm(forms.ModelForm):
    class Meta:
        model = LancamentoFinanceiro
        fields = ['tipo', 'descricao', 'valor', 'data_vencimento', 'data_pagamento', 'atendimento']
        widgets = {
            'data_vencimento': forms.DateInput(attrs={'type': 'date'}),
            'data_pagamento': forms.DateInput(attrs={'type': 'date'}),
        }


class FaturaForm(forms.ModelForm):
    class Meta:
        model = Fatura
        fields = ['convenio', 'mes_referencia', 'atendimentos', 'valor_total', 'status']
        widgets = {
            'mes_referencia': forms.DateInput(attrs={'type': 'month'}),
        }


class ComissaoForm(forms.ModelForm):
    class Meta:
        model = Comissao
        fields = ['profissional', 'atendimento', 'valor', 'paga']


class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ['nome', 'email', 'telefone', 'origem', 'status']


class CampanhaMarketingForm(forms.ModelForm):
    class Meta:
        model = CampanhaMarketing
        fields = ['nome', 'tipo', 'data_inicio', 'data_fim', 'descricao']
        widgets = {
            'data_inicio': forms.DateInput(attrs={'type': 'date'}),
            'data_fim': forms.DateInput(attrs={'type': 'date'}),
        }


class PesquisaSatisfacaoForm(forms.ModelForm):
    class Meta:
        model = PesquisaSatisfacao
        fields = ['paciente', 'nota_nps', 'comentarios']


class CupomDescontoForm(forms.ModelForm):
    class Meta:
        model = CupomDesconto
        fields = ['codigo', 'valor_desconto', 'data_validade', 'ativo', 'campanha']
        widgets = {
            'data_validade': forms.DateInput(attrs={'type': 'date'}),
        }