from rest_framework import serializers
from clinica.models import Paciente, Agendamento, Atendimento, Prontuario, User, Clinica, LancamentoFinanceiro, DocumentoArquivo, Lead, Profissional, PastaDocumento, TipoTratamento

class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        fields = '__all__'

class AgendamentoSerializer(serializers.ModelSerializer):
    paciente_nome = serializers.ReadOnlyField(source='paciente.nome')
    profissional_username = serializers.ReadOnlyField(source='profissional.user.username')

    class Meta:
        model = Agendamento
        fields = '__all__'
        extra_fields = ['paciente_nome', 'profissional_username']

class AtendimentoSerializer(serializers.ModelSerializer):
    paciente_nome = serializers.ReadOnlyField(source='agendamento.paciente.nome')
    profissional_username = serializers.ReadOnlyField(source='agendamento.profissional.user.username')

    class Meta:
        model = Atendimento
        fields = '__all__'
        extra_fields = ['paciente_nome', 'profissional_username']

class ProntuarioSerializer(serializers.ModelSerializer):
    paciente_nome = serializers.ReadOnlyField(source='paciente.nome')

    class Meta:
        model = Prontuario
        fields = '__all__'
        extra_fields = ['paciente_nome']

class UserSerializer(serializers.ModelSerializer):
    perfil_display = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'perfil', 'clinica', 'perfil_display']

    def get_perfil_display(self, obj):
        return obj.get_perfil_display()

class ClinicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clinica
        fields = '__all__'

class LancamentoFinanceiroSerializer(serializers.ModelSerializer):
    class Meta:
        model = LancamentoFinanceiro
        fields = '__all__'

class DocumentoArquivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentoArquivo
        fields = '__all__'
        read_only_fields = ('hash_arquivo',)

class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = '__all__'

class ProfissionalSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True) # Inclui os dados do usuário relacionado

    class Meta:
        model = Profissional
        fields = '__all__'

class PastaDocumentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PastaDocumento
        fields = '__all__'

class TipoTratamentoSerializer(serializers.ModelSerializer):
    clinica_nome = serializers.ReadOnlyField(source='clinica.nome')

    class Meta:
        model = TipoTratamento
        fields = '__all__'
        extra_fields = ['clinica_nome']