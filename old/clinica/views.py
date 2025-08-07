# clinica/views.py - RECONSTRUÇÃO

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny, DjangoModelPermissions
from clinica.models import (
    User, Paciente, Profissional, Agendamento, Atendimento, DocumentoArquivo, Clinica,
    LancamentoFinanceiro, Lead, TipoTratamento, CampanhaMarketing, Comissao,
    Fatura, PesquisaSatisfacao, CupomDesconto, Prontuario, PastaDocumento
)
import json
from django.utils import timezone
from rest_framework import generics
from .serializers import (
    PacienteSerializer, AgendamentoSerializer, AtendimentoSerializer, ProntuarioSerializer,
    UserSerializer, ClinicaSerializer, LancamentoFinanceiroSerializer, DocumentoArquivoSerializer,
    LeadSerializer, ProfissionalSerializer, PastaDocumentoSerializer, TipoTratamentoSerializer
)

def get_selected_clinic_id(request):
    return request.session.get('selected_clinic_id')

# Helper function for API responses
def api_response(data, status=200):
    return JsonResponse(data, status=status, safe=False)

# Placeholder for common CRUD operations
def not_implemented_api(request, *args, **kwargs):
    return api_response({'message': 'API endpoint not implemented yet.'}, status=501)



# --- Pacientes ---
class PacienteListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = PacienteSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

    def get_queryset(self):
        clinic_id = get_selected_clinic_id(self.request)
        if clinic_id:
            return Paciente.objects.filter(clinica_id=clinic_id)
        return Paciente.objects.all()

    def perform_create(self, serializer):
        clinic_id = get_selected_clinic_id(self.request)
        if clinic_id:
            clinica = get_object_or_404(Clinica, pk=clinic_id)
            serializer.save(clinica=clinica)
        else:
            serializer.save()

class PacienteRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PacienteSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

    def get_queryset(self):
        clinic_id = get_selected_clinic_id(self.request)
        if clinic_id:
            return Paciente.objects.filter(clinica_id=clinic_id)
        return Paciente.objects.all()

# --- Agendamentos ---
# clinica/views.py - RECONSTRUÇÃO

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny, DjangoModelPermissions
from clinica.models import (
    User, Paciente, Profissional, Agendamento, Atendimento, DocumentoArquivo, Clinica,
    LancamentoFinanceiro, Lead, TipoTratamento, CampanhaMarketing, Comissao,
    Fatura, PesquisaSatisfacao, CupomDesconto, Prontuario, PastaDocumento
)
import json
from django.utils import timezone
from rest_framework import generics
from .serializers import (
    PacienteSerializer, AgendamentoSerializer, AtendimentoSerializer, ProntuarioSerializer,
    UserSerializer, ClinicaSerializer, LancamentoFinanceiroSerializer, DocumentoArquivoSerializer,
    LeadSerializer, ProfissionalSerializer, PastaDocumentoSerializer, TipoTratamentoSerializer
)

def get_selected_clinic_id(request):
    return request.session.get('selected_clinic_id')

# Helper function for API responses
def api_response(data, status=200):
    return JsonResponse(data, status=status, safe=False)

# Placeholder for common CRUD operations
def not_implemented_api(request, *args, **kwargs):
    return api_response({'message': 'API endpoint not implemented yet.'}, status=501)



# --- Pacientes ---
class PacienteListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = PacienteSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

    def get_queryset(self):
        clinic_id = get_selected_clinic_id(self.request)
        if clinic_id:
            return Paciente.objects.filter(clinica_id=clinic_id)
        return Paciente.objects.all()

    def perform_create(self, serializer):
        clinic_id = get_selected_clinic_id(self.request)
        if clinic_id:
            clinica = get_object_or_404(Clinica, pk=clinic_id)
            serializer.save(clinica=clinica)
        else:
            serializer.save()

class PacienteRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PacienteSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

    def get_queryset(self):
        clinic_id = get_selected_clinic_id(self.request)
        if clinic_id:
            return Paciente.objects.filter(clinica_id=clinic_id)
        return Paciente.objects.all()

# --- Agendamentos ---
class AgendamentoListCreateAPIView(generics.ListCreateAPIView):
    queryset = Agendamento.objects.all()
    serializer_class = AgendamentoSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

class AgendamentoRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AgendamentoSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

    def get_queryset(self):
        clinic_id = get_selected_clinic_id(self.request)
        if clinic_id:
            return Agendamento.objects.filter(paciente__clinica_id=clinic_id)
        return Agendamento.objects.all()

# --- Usuários ---
class UserListCreateAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

class UserRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

    def get_queryset(self):
        clinic_id = get_selected_clinic_id(self.request)
        if clinic_id:
            return User.objects.filter(clinica_id=clinic_id)
        return User.objects.all()

# --- Clínicas ---
class ClinicaListCreateAPIView(generics.ListCreateAPIView):
    queryset = Clinica.objects.all()
    serializer_class = ClinicaSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

class ClinicaRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Clinica.objects.all()
    serializer_class = ClinicaSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

# --- Lançamentos Financeiros ---
class LancamentoFinanceiroListCreateAPIView(generics.ListCreateAPIView):
    queryset = LancamentoFinanceiro.objects.all()
    serializer_class = LancamentoFinanceiroSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

class LancamentoFinanceiroRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LancamentoFinanceiroSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

    def get_queryset(self):
        clinic_id = get_selected_clinic_id(self.request)
        if clinic_id:
            return LancamentoFinanceiro.objects.filter(clinica_id=clinic_id)
        return LancamentoFinanceiro.objects.all()

# --- Leads ---
class LeadListCreateAPIView(generics.ListCreateAPIView):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

class LeadRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LeadSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

    def get_queryset(self):
        clinic_id = get_selected_clinic_id(self.request)
        if clinic_id:
            return Lead.objects.filter(clinica_id=clinic_id)
        return Lead.objects.all()

# --- Tipos de Tratamento ---
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def tipo_tratamento_list_api(request):
    tipos_tratamento = TipoTratamento.objects.all().values()
    return api_response(list(tipos_tratamento))

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def tipo_tratamento_create_api(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        # Basic validation
        if not all(key in data for key in ['nome', 'descricao', 'preco']):
            return api_response({'message': 'Missing data for treatment type creation.'}, status=400)
        
        try:
            tipo_tratamento = TipoTratamento.objects.create(
                nome=data['nome'],
                descricao=data['descricao'],
                preco=data['preco'],
            )
            return api_response({'message': 'Treatment type created successfully', 'id': tipo_tratamento.id}, status=201)
        except Exception as e:
            return api_response({'message': str(e)}, status=400)
    return api_response({'message': 'Method not allowed'}, status=405)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def tipo_tratamento_detail_api(request, pk):
    tipo_tratamento = get_object_or_404(TipoTratamento, pk=pk)
    return api_response({
        'id': tipo_tratamento.id,
        'nome': tipo_tratamento.nome,
        'descricao': tipo_tratamento.descricao,
        'preco': str(tipo_tratamento.preco),
    })

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def tipo_tratamento_update_api(request, pk):
    if request.method == 'PUT':
        tipo_tratamento = get_object_or_404(TipoTratamento, pk=pk)
        data = json.loads(request.body)
        tipo_tratamento.nome = data.get('nome', tipo_tratamento.nome)
        tipo_tratamento.descricao = data.get('descricao', tipo_tratamento.descricao)
        tipo_tratamento.preco = data.get('preco', tipo_tratamento.preco)
        tipo_tratamento.save()
        return api_response({'message': 'Treatment type updated successfully'})
    return api_response({'message': 'Method not allowed'}, status=405)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def tipo_tratamento_delete_api(request, pk):
    if request.method == 'DELETE':
        clinic_id = get_selected_clinic_id(request)
        if not clinic_id:
            return api_response({'message': 'Clínica não selecionada.'}, status=400)
        tipo_tratamento = get_object_or_404(TipoTratamento, pk=pk, clinica_id=clinic_id)
        tipo_tratamento.delete()
        return api_response({'message': 'Treatment type deleted successfully'}, status=204)
    return api_response({'message': 'Method not allowed'}, status=405)

# --- Profissionais ---
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profissional_agenda_api(request):
    clinic_id = get_selected_clinic_id(request)
    if not clinic_id and request.user.username != 'admin':
        return api_response({'message': 'Clínica não selecionada.'}, status=400)
    profissional = get_object_or_404(Profissional, user=request.user)
    if request.user.username == 'admin':
        agendamentos = Agendamento.objects.filter(profissional=profissional).values()
    else:
       agendamentos = Agendamento.objects.filter
      (profissional=profissional, paciente__clinica_id=clinic_id).values()
    return api_response(list(agendamentos))

class ProfissionalListAPIView(generics.ListAPIView):
    serializer_class = ProfissionalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        clinic_id = get_selected_clinic_id(self.request)
        if self.request.user.username == 'admin':
            return Profissional.objects.all()
        if clinic_id:
            return Profissional.objects.filter(user__clinica_id=clinic_id)
        return Profissional.objects.none()

class ClinicaPublicListAPIView(generics.ListAPIView):
    queryset = Clinica.objects.all()
    serializer_class = ClinicaSerializer
    permission_classes = [AllowAny]