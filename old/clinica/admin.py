"""Módulo de configuração da interface de administração do Django para a aplicação 'clinica'."""

# Importa o módulo de administração do Django
from django.contrib import admin
# Importa os modelos do aplicativo clinica para registro na interface de administração
from .models import User, Clinica, Paciente, Agendamento, Atendimento, PastaDocumento, DocumentoArquivo, Prontuario, TipoTratamento

# Registra os modelos no painel administrativo do Django.
# Isso permite que os administradores visualizem, criem, editem e excluam instâncias desses modelos
# diretamente através da interface web de administração.
admin.site.register(User)
@admin.register(Clinica)
class ClinicaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'endereco', 'telefone', 'num_guiches', 'tempo_minimo_atendimento')
    search_fields = ('nome', 'endereco', 'telefone')
admin.site.register(Paciente)
admin.site.register(Agendamento)
admin.site.register(Atendimento)
admin.site.register(PastaDocumento)
admin.site.register(DocumentoArquivo)
admin.site.register(Prontuario)
admin.site.register(TipoTratamento)
