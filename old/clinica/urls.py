from django.urls import path
from . import vtemp_views
# from .views import (
#     ClinicaListView, ClinicaCreateView, ClinicaUpdateView, ClinicaDeleteView,
#     TipoTratamentoListView, TipoTratamentoCreateView, TipoTratamentoUpdateView, TipoTratamentoDeleteView,
#     PacienteListView, PacienteCreateView, PacienteUpdateView, PacienteDeleteView,
#     AgendamentoListView, AgendamentoCreateView, AgendamentoUpdateView, AgendamentoDeleteView,
#     AtendimentoListView, AtendimentoCreateView, AtendimentoUpdateView, AtendimentoDeleteView,
#     DocumentoArquivoListView, DocumentoArquivoCreateView, DocumentoArquivoUpdateView, DocumentoArquivoDeleteView,
#     ProntuarioListView, ProntuarioCreateView, ProntuarioUpdateView, ProntuarioDeleteView,
#     LancamentoFinanceiroListView, LancamentoFinanceiroCreateView, LancamentoFinanceiroUpdateView, LancamentoFinanceiroDeleteView,
#     FaturaListView, FaturaCreateView, FaturaUpdateView, FaturaDeleteView,
#     ComissaoListView, ComissaoCreateView, ComissaoUpdateView, ComissaoDeleteView,
#     LeadListView, LeadCreateView, LeadUpdateView, LeadDeleteView,
#     CampanhaMarketingListView, CampanhaMarketingCreateView, CampanhaMarketingUpdateView, CampanhaMarketingDeleteView,
#     PesquisaSatisfacaoListView, PesquisaSatisfacaoCreateView, PesquisaSatisfacaoUpdateView, PesquisaSatisfacaoDeleteView,
#     CupomDescontoListView, CupomDescontoCreateView, CupomDescontoUpdateView, CupomDescontoDeleteView
# )

app_name = 'clinica'

urlpatterns = [
    # path('', views.index, name='index'),
    # path('dashboard/', views.dashboard, name='dashboard'),

    # path('login/', views.login_view, name='login'),
    # path('logout/', views.logout_view, name='logout'),

    # path('users/', views.user_list, name='user_list'),
    # path('users/new/', views.user_create, name='user_create'),
    # path('users/<int:pk>/update/', views.user_update, name='user_update'),
    # path('users/<int:pk>/delete/', views.user_delete, name='user_delete'),

    # Rotas para Clínicas (Class-Based Views) - COMENTADAS
    # path('clinicas/', ClinicaListView.as_view(), name='clinica_list'),
    # path('clinicas/new/', ClinicaCreateView.as_view(), name='clinica_create'),
    # path('clinicas/<int:pk>/update/', ClinicaUpdateView.as_view(), name='clinica_update'),
    # path('clinicas/<int:pk>/delete/', ClinicaDeleteView.as_view(), name='clinica_delete'),

    # Rotas para Tipos de Tratamento (Class-Based Views) - COMENTADAS
    # path('tipos-tratamento/', TipoTratamentoListView.as_view(), name='tipotratamento_list'),
    # path('tipos-tratamento/new/', TipoTratamentoCreateView.as_view(), name='tipotratamento_create'),
    # path('tipos-tratamento/<int:pk>/update/', TipoTratamentoUpdateView.as_view(), name='tipotratamento_update'),
    # path('tipos-tratamento/<int:pk>/delete/', TipoTratamentoDeleteView.as_view(), name='tipotratamento_delete'),

    # Rotas para Pacientes (Class-Based Views) - COMENTADAS
    # path('pacientes/', PacienteListView.as_view(), name='paciente_list'),
    # path('pacientes/new/', PacienteCreateView.as_view(), name='paciente_create'),
    # path('pacientes/<int:pk>/update/', PacienteUpdateView.as_view(), name='paciente_update'),
    # path('pacientes/<int:pk>/delete/', PacienteDeleteView.as_view(), name='paciente_delete'),

    # Rotas para Agendamentos (Class-Based Views) - COMENTADAS
    # path('agendamentos/', AgendamentoListView.as_view(), name='agendamento_list'),
    # path('agendamentos/new/', AgendamentoCreateView.as_view(), name='agendamento_create'),
    # path('agendamentos/<int:pk>/update/', AgendamentoUpdateView.as_view(), name='agendamento_update'),
    # path('agendamentos/<int:pk>/delete/', AgendamentoDeleteView.as_view(), name='agendamento_delete'),

    # Rotas para Atendimentos (Class-Based Views) - COMENTADAS
    # path('atendimentos/', AtendimentoListView.as_view(), name='atendimento_list'),
    # path('atendimentos/new/', AtendimentoCreateView.as_view(), name='atendimento_create'),
    # path('atendimentos/<int:pk>/update/', AtendimentoUpdateView.as_view(), name='atendimento_update'),
    # path('atendimentos/<int:pk>/delete/', AtendimentoDeleteView.as_view(), name='atendimento_delete'),

    # Rotas para Documentos (Class-Based Views) - COMENTADAS
    # path('documentos/', DocumentoArquivoListView.as_view(), name='documento_list'),
    # path('documentos/new/', DocumentoArquivoCreateView.as_view(), name='documento_create'),
    # path('documentos/<int:pk>/update/', DocumentoArquivoUpdateView.as_view(), name='documento_update'),
    # path('documentos/<int:pk>/delete/', DocumentoArquivoDeleteView.as_view(), name='documento_delete'),

    # Rotas para Prontuários (Class-Based Views) - COMENTADAS
    # path('prontuarios/', ProntuarioListView.as_view(), name='prontuario_list'),
    # path('prontuarios/new/', ProntuarioCreateView.as_view(), name='prontuario_create'),
    # path('prontuarios/<int:pk>/update/', ProntuarioUpdateView.as_view(), name='prontuario_update'),
    # path('prontuarios/<int:pk>/delete/', ProntuarioDeleteView.as_view(), name='prontuario_delete'),

    # path('agendamentos/calendario/', views.agendamento_calendario, name='agendamento_calendario'),
    # path('agendamentos/api/', views.agendamento_api, name='agendamento_api'),
    # path('agendamentos/check-availability/', views.agendamento_check_availability, name='agendamento_check_availability'),
    # path('atendimentos/api/', views.atendimento_api, name='atendimento_api'),
    # path('api/users/', views.api_users, name='api_users'),

    # Rotas para Lançamentos Financeiros (Class-Based Views) - COMENTADAS
    # path('lancamentos-financeiros/', LancamentoFinanceiroListView.as_view(), name='lancamentofinanceiro_list'),
    # path('lancamentos-financeiros/new/', LancamentoFinanceiroCreateView.as_view(), name='lancamentofinanceiro_create'),
    # path('lancamentos-financeiros/<int:pk>/update/', LancamentoFinanceiroUpdateView.as_view(), name='lancamentofinanceiro_update'),
    # path('lancamentos-financeiros/<int:pk>/delete/', LancamentoFinanceiroDeleteView.as_view(), name='lancamentofinanceiro_delete'),

    # Rotas para Faturas (Class-Based Views) - COMENTADAS
    # path('faturas/', FaturaListView.as_view(), name='fatura_list'),
    # path('faturas/new/', FaturaCreateView.as_view(), name='fatura_create'),
    # path('faturas/<int:pk>/update/', FaturaUpdateView.as_view(), name='fatura_update'),
    # path('faturas/<int:pk>/delete/', FaturaDeleteView.as_view(), name='fatura_delete'),

    # Rotas para Comissões (Class-Based Views) - COMENTADAS
    # path('comissoes/', ComissaoListView.as_view(), name='comissao_list'),
    # path('comissoes/new/', ComissaoCreateView.as_view(), name='comissao_create'),
    # path('comissoes/<int:pk>/update/', ComissaoUpdateView.as_view(), name='comissao_update'),
    # path('comissoes/<int:pk>/delete/', ComissaoDeleteView.as_view(), name='comissao_delete'),

    # Rotas para Leads (Class-Based Views) - COMENTADAS
    # path('leads/', LeadListView.as_view(), name='lead_list'),
    # path('leads/new/', LeadCreateView.as_view(), name='lead_create'),
    # path('leads/<int:pk>/update/', LeadUpdateView.as_view(), name='lead_update'),
    # path('leads/<int:pk>/delete/', LeadDeleteView.as_view(), name='lead_delete'),

    # Rotas para Campanhas de Marketing (Class-Based Views) - COMENTADAS
    # path('campanhas-marketing/', CampanhaMarketingListView.as_view(), name='campanhamarketing_list'),
    # path('campanhas-marketing/new/', CampanhaMarketingCreateView.as_view(), name='campanhamarketing_create'),
    # path('campanhas-marketing/<int:pk>/update/', CampanhaMarketingUpdateView.as_view(), name='campanhamarketing_update'),
    # path('campanhas-marketing/<int:pk>/delete/', CampanhaMarketingDeleteView.as_view(), name='campanhamarketing_delete'),

    # Rotas para Pesquisas de Satisfação (Class-Based Views) - COMENTADAS
    # path('pesquisas-satisfacao/', PesquisaSatisfacaoListView.as_view(), name='pesquisasatisfacao_list'),
    # path('pesquisas-satisfacao/new/', PesquisaSatisfacaoCreateView.as_view(), name='pesquisasatisfacao_create'),
    # path('pesquisas-satisfacao/<int:pk>/update/', PesquisaSatisfacaoUpdateView.as_view(), name='pesquisasatisfacao_update'),
    # path('pesquisas-satisfacao/<int:pk>/delete/', PesquisaSatisfacaoDeleteView.as_view(), name='pesquisasatisfacao_delete'),

    # Rotas para Cupons de Desconto (Class-Based Views) - COMENTADAS
    # path('cupons-desconto/', CupomDescontoListView.as_view(), name='cupomdesconto_list'),
    # path('cupons-desconto/new/', CupomDescontoCreateView.as_view(), name='cupomdesconto_create'),
    # path('cupons-desconto/<int:pk>/update/', CupomDescontoUpdateView.as_view(), name='cupomdesconto_update'),
    # path('cupons-desconto/<int:pk>/delete/', CupomDescontoDeleteView.as_view(), name='cupomdesconto_delete'),

    # Rotas para o Portal do Paciente - COMENTADAS
    # path('paciente/dashboard/', views.paciente_dashboard, name='paciente_dashboard'),
    # path('paciente/agendamentos/', views.paciente_agendamentos, name='paciente_agendamentos'),
    # path('paciente/prontuarios/', views.paciente_prontuarios, name='paciente_prontuarios'),
    # path('paciente/documentos/', views.paciente_documentos, name='paciente_documentos'),
    # path('paciente/lancamentos-financeiros/', views.paciente_lancamentos_financeiros, name='paciente_lancamentos_financeiros'),
    # path('paciente/agendar-consulta/', views.paciente_agendar_consulta, name='paciente_agendar_consulta'),

    # Rotas para o Portal do Profissional - COMENTADAS
    # path('profissional/dashboard/', views.profissional_dashboard, name='profissional_dashboard'),
    # path('profissional/agenda/', views.profissional_agenda, name='profissional_agenda'),
    # path('profissional/prontuarios/', views.profissional_prontuarios, name='profissional_prontuarios'),
]