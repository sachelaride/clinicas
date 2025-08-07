from django.urls import path
from . import vtemp_views

app_name = 'clinica_api'

urlpatterns = [
    # Rotas para Pacientes
    path('pacientes/', vtemp_views.PacienteListCreateAPIView.as_view(), name='paciente_list_create_api'),
    path('pacientes/<int:pk>/', vtemp_views.PacienteRetrieveUpdateDestroyAPIView.as_view(), name='paciente_detail_update_delete_api'),

    # Rotas para Usuários
    path('users/', vtemp_views.UserListCreateAPIView.as_view(), name='user_list_create_api'),
    path('users/<int:pk>/', vtemp_views.UserRetrieveUpdateDestroyAPIView.as_view(), name='user_detail_update_delete_api'),

    # Rotas para Clínicas
    path('clinicas/', vtemp_views.ClinicaListCreateAPIView.as_view(), name='clinica_list_create_api'),
    path('clinicas/<int:pk>/', vtemp_views.ClinicaRetrieveUpdateDestroyAPIView.as_view(), name='clinica_detail_update_delete_api'),

    # Rotas para Lançamentos Financeiros
    path('lancamentos-financeiros/', vtemp_views.LancamentoFinanceiroListCreateAPIView.as_view(), name='lancamento_financeiro_list_create_api'),
    path('lancamentos-financeiros/<int:pk>/', vtemp_views.LancamentoFinanceiroRetrieveUpdateDestroyAPIView.as_view(), name='lancamento_financeiro_detail_update_delete_api'),

    # Rotas para Leads
    path('leads/', vtemp_views.LeadListCreateAPIView.as_view(), name='lead_list_create_api'),
    path('leads/<int:pk>/', vtemp_views.LeadRetrieveUpdateDestroyAPIView.as_view(), name='lead_detail_update_delete_api'),

    # Rotas para Profissionais
    path('profissionais/', vtemp_views.ProfissionalListAPIView.as_view(), name='profissional_list_api'),

    # Rotas para Tipos de Tratamento
    path('tipos-tratamento/', vtemp_views.tipo_tratamento_list_api, name='tipo_tratamento_list_api'),
    path('tipos-tratamento/new/', vtemp_views.tipo_tratamento_create_api, name='tipo_tratamento_create_api'),
    path('tipos-tratamento/<int:pk>/', vtemp_views.tipo_tratamento_detail_api, name='tipo_tratamento_detail_api'),
    path('tipos-tratamento/<int:pk>/update/', vtemp_views.tipo_tratamento_update_api, name='tipo_tratamento_update_api'),
    path('tipos-tratamento/<int:pk>/delete/', vtemp_views.tipo_tratamento_delete_api, name='tipo_tratamento_delete_api'),

    # Rotas para o Portal do Profissional
    path('profissional/agenda/', vtemp_views.profissional_agenda_api, name='profissional_agenda_api'),

    # Rotas para o Portal do Paciente
    path('paciente/dashboard/', vtemp_views.paciente_dashboard_api, name='paciente_dashboard_api'),
    path('paciente/agendamentos/', vtemp_views.paciente_agendamentos_api, name='paciente_agendamentos_api'),
    path('paciente/prontuarios/', vtemp_views.paciente_prontuarios_api, name='paciente_prontuarios_api'),
    path('paciente/documentos/', vtemp_views.paciente_documentos_api, name='paciente_documentos_api'),
    path('paciente/lancamentos-financeiros/', vtemp_views.paciente_lancamentos_financeiros_api, name='paciente_lancamentos_financeiros_api'),
    path('paciente/agendar-consulta/', vtemp_views.paciente_agendar_consulta_api, name='paciente_agendar_consulta_api'),

    # Rotas para Campanhas de Marketing
    path('campanhas-marketing/', vtemp_views.campanha_marketing_list_api, name='campanha_marketing_list_api'),
    path('campanhas-marketing/new/', vtemp_views.campanha_marketing_create_api, name='campanha_marketing_create_api'),
    path('campanhas-marketing/<int:pk>/', vtemp_views.campanha_marketing_detail_api, name='campanha_marketing_detail_api'),
    path('campanhas-marketing/<int:pk>/update/', vtemp_views.campanha_marketing_update_api, name='campanha_marketing_update_api'),
    path('campanhas-marketing/<int:pk>/delete/', vtemp_views.campanha_marketing_delete_api, name='campanha_marketing_delete_api'),

    # Rotas para Comissões
    path('comissoes/', vtemp_views.comissao_list_api, name='comissao_list_api'),
    path('comissoes/new/', vtemp_views.comissao_create_api, name='comissao_create_api'),
    path('comissoes/<int:pk>/', vtemp_views.comissao_detail_api, name='comissao_detail_api'),
    path('comissoes/<int:pk>/update/', vtemp_views.comissao_update_api, name='comissao_update_api'),
    path('comissoes/<int:pk>/delete/', vtemp_views.comissao_delete_api, name='comissao_delete_api'),

    # Rotas para Faturas
    path('faturas/', vtemp_views.fatura_list_api, name='fatura_list_api'),
    path('faturas/new/', vtemp_views.fatura_create_api, name='fatura_create_api'),
    path('faturas/<int:pk>/', vtemp_views.fatura_detail_api, name='fatura_detail_api'),
    path('faturas/<int:pk>/update/', vtemp_views.fatura_update_api, name='fatura_update_api'),
    path('faturas/<int:pk>/delete/', vtemp_views.fatura_delete_api, name='fatura_delete_api'),

    # Rotas para Pesquisas de Satisfação
    path('pesquisas-satisfacao/', vtemp_views.pesquisa_satisfacao_list_api, name='pesquisa_satisfacao_list_api'),
    path('pesquisas-satisfacao/new/', vtemp_views.pesquisa_satisfacao_create_api, name='pesquisa_satisfacao_create_api'),
    path('pesquisas-satisfacao/<int:pk>/', vtemp_views.pesquisa_satisfacao_detail_api, name='pesquisa_satisfacao_detail_api'),
    path('pesquisas-satisfacao/<int:pk>/update/', vtemp_views.pesquisa_satisfacao_update_api, name='pesquisa_satisfacao_update_api'),
    path('pesquisas-satisfacao/<int:pk>/delete/', vtemp_views.pesquisa_satisfacao_delete_api, name='pesquisa_satisfacao_delete_api'),

    # Rotas para Cupons de Desconto
    path('cupons-desconto/', vtemp_views.cupom_desconto_list_api, name='cupom_desconto_list_api'),
    path('cupons-desconto/new/', vtemp_views.cupom_desconto_create_api, name='cupom_desconto_create_api'),
    path('cupons-desconto/<int:pk>/', vtemp_views.cupom_desconto_detail_api, name='cupom_desconto_detail_api'),
    path('cupons-desconto/<int:pk>/update/', vtemp_views.cupom_desconto_update_api, name='cupom_desconto_update_api'),
    path('cupons-desconto/<int:pk>/delete/', vtemp_views.cupom_desconto_delete_api, name='cupom_desconto_delete_api'),

    # Rotas para o Portal do Profissional
    path('profissional/agenda/', vtemp_views.profissional_agenda_api, name='profissional_agenda_api'),
    path('profissional/prontuarios/', vtemp_views.profissional_prontuarios_api, name='profissional_prontuarios_api'),

    # Outras Rotas da API
    path('agendamentos/', vtemp_views.AgendamentoListCreateAPIView.as_view(), name='agendamento_list_create_api'),
    path('agendamentos/<int:pk>/', vtemp_views.AgendamentoRetrieveUpdateDestroyAPIView.as_view(), name='agendamento_detail_update_delete_api'),
    path('atendimentos/', vtemp_views.AtendimentoListCreateAPIView.as_view(), name='atendimento_list_create_api'),
    path('atendimentos/<int:pk>/', vtemp_views.AtendimentoRetrieveUpdateDestroyAPIView.as_view(), name='atendimento_detail_update_delete_api'),

    # Rotas para Prontuarios
    path('prontuarios/', vtemp_views.ProntuarioListCreateAPIView.as_view(), name='prontuario_list_create_api'),
    path('prontuarios/<int:pk>/', vtemp_views.ProntuarioRetrieveUpdateDestroyAPIView.as_view(), name='prontuario_detail_update_delete_api'),
    path('documentos/', vtemp_views.DocumentoArquivoListCreateAPIView.as_view(), name='documento_list_create_api'),
    path('documentos/<int:pk>/', vtemp_views.DocumentoArquivoRetrieveUpdateDestroyAPIView.as_view(), name='documento_detail_update_delete_api'),

    # Rotas para Pastas de Documento
    path('pastas-documento/', vtemp_views.PastaDocumentoListCreateAPIView.as_view(), name='pasta_documento_list_create_api'),
    path('pastas-documento/<int:pk>/', vtemp_views.PastaDocumentoRetrieveUpdateDestroyAPIView.as_view(), name='pasta_documento_detail_update_delete_api'),

    path('user/', vtemp_views.current_user_api, name='current_user_api'),
    path('login/', vtemp_views.login_api, name='login_api'),
    path('clinicas-public/', vtemp_views.ClinicaPublicListAPIView.as_view(), name='clinicas_public_list_api'),
    path('logout/', vtemp_views.logout_api, name='logout_api'),
    path('csrf_token/', vtemp_views.get_csrf_token, name='csrf_token'),
]