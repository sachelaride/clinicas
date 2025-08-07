from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from clinica.models import Atendimento, Agendamento, Paciente, Profissional, Clinica, User
from datetime import datetime

class AtendimentoAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.clinica = Clinica.objects.create(nome='Clinica Teste')
        self.admin_user = User.objects.create_superuser('admin_atendimento_api', 'admin_atendimento_api@example.com', 'password', perfil='ADMIN', clinica=self.clinica)
        self.paciente_user = User.objects.create_user('paciente_user_atendimento_api', 'paciente_atendimento_api@teste.com', 'senha123', perfil='PACIENTE', clinica=self.clinica)
        self.paciente = Paciente.objects.create(
            nome='Paciente Atendimento API Teste',
            cpf='123.456.789-14',
            data_nascimento='1990-01-01',
            clinica=self.clinica
        )
        self.profissional_user = User.objects.create_user('profissional_user_atendimento_api', 'profissional_atendimento_api@teste.com', 'senha123', perfil='PROFISSIONAL', clinica=self.clinica)
        self.profissional = Profissional.objects.create(user=self.profissional_user, especialidade='Cardiologia')
        self.agendamento = Agendamento.objects.create(
            paciente=self.paciente,
            profissional=self.profissional,
            data=datetime.now(),
            status='AGENDADO'
        )
        self.client.login(username='admin_atendimento_api', password='password')

    def test_atendimento_list(self):
        """Testa a listagem de atendimentos."""
        response = self.client.get(reverse('clinica_api:atendimento_list_create_api'))
        self.assertEqual(response.status_code, 200)

    def test_atendimento_create(self):
        """Testa a criação de um atendimento."""
        data = {
            'agendamento': self.agendamento.id,
            'status': 'INICIADO'
        }
        response = self.client.post(reverse('clinica_api:atendimento_list_create_api'), data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_atendimento_detail(self):
        """Testa o detalhe de um atendimento."""
        atendimento = Atendimento.objects.create(agendamento=self.agendamento)
        response = self.client.get(reverse('clinica_api:atendimento_detail_update_delete_api', kwargs={'pk': atendimento.pk}))
        self.assertEqual(response.status_code, 200)

    def test_atendimento_update(self):
        """Testa a atualização de um atendimento."""
        atendimento = Atendimento.objects.create(agendamento=self.agendamento)
        updated_data = {
            'agendamento': self.agendamento.id,
            'status': 'FINALIZADO'
        }
        response = self.client.put(reverse('clinica_api:atendimento_detail_update_delete_api', kwargs={'pk': atendimento.pk}), updated_data, format='json')
        self.assertEqual(response.status_code, 200)
        atendimento.refresh_from_db()
        self.assertEqual(atendimento.status, 'FINALIZADO')

    def test_atendimento_delete(self):
        """Testa a exclusão de um atendimento."""
        atendimento = Atendimento.objects.create(agendamento=self.agendamento)
        response = self.client.delete(reverse('clinica_api:atendimento_detail_update_delete_api', kwargs={'pk': atendimento.pk}))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Atendimento.objects.count(), 0)