from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from clinica.models import Agendamento, Paciente, Profissional, Clinica, User
from datetime import datetime

class AgendamentoAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.clinica = Clinica.objects.create(nome='Clinica Teste')
        self.admin_user = User.objects.create_superuser('admin_agendamento', 'admin_agendamento@example.com', 'password', perfil='ADMIN', clinica=self.clinica)
        self.paciente_user = User.objects.create_user('paciente_user_agendamento', 'paciente_agendamento@teste.com', 'senha123', perfil='PACIENTE', clinica=self.clinica)
        self.paciente = Paciente.objects.create(
            nome='Paciente Agendamento Teste',
            cpf='123.456.789-13',
            data_nascimento='1990-01-01',
            clinica=self.clinica
        )
        self.profissional_user = User.objects.create_user('profissional_user_agendamento', 'profissional_agendamento@teste.com', 'senha123', perfil='PROFISSIONAL', clinica=self.clinica)
        self.profissional = Profissional.objects.create(user=self.profissional_user, especialidade='Cardiologia')
        self.client.login(username='admin_agendamento', password='password')

    def test_agendamento_list(self):
        """Testa a listagem de agendamentos."""
        response = self.client.get(reverse('clinica_api:agendamento_list_create_api'))
        self.assertEqual(response.status_code, 200)

    def test_agendamento_create(self):
        """Testa a criação de um agendamento."""
        data = {
            'paciente': self.paciente.id,
            'profissional': self.profissional.id,
            'data': datetime.now().isoformat(),
            'status': 'AGENDADO'
        }
        response = self.client.post(reverse('clinica_api:agendamento_list_create_api'), data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_agendamento_detail(self):
        """Testa o detalhe de um agendamento."""
        agendamento = Agendamento.objects.create(
            paciente=self.paciente,
            profissional=self.profissional,
            data=datetime.now(),
            status='AGENDADO'
        )
        response = self.client.get(reverse('clinica_api:agendamento_detail_update_delete_api', kwargs={'pk': agendamento.pk}))
        self.assertEqual(response.status_code, 200)

    def test_agendamento_update(self):
        """Testa a atualização de um agendamento."""
        agendamento = Agendamento.objects.create(
            paciente=self.paciente,
            profissional=self.profissional,
            data=datetime.now(),
            status='AGENDADO'
        )
        updated_data = {
            'paciente': self.paciente.id,
            'profissional': self.profissional.id,
            'data': datetime.now().isoformat(),
            'status': 'CONCLUIDO'
        }
        response = self.client.put(reverse('clinica_api:agendamento_detail_update_delete_api', kwargs={'pk': agendamento.pk}), updated_data, format='json')
        self.assertEqual(response.status_code, 200)
        agendamento.refresh_from_db()
        self.assertEqual(agendamento.status, 'CONCLUIDO')

    def test_agendamento_delete(self):
        """Testa a exclusão de um agendamento."""
        agendamento = Agendamento.objects.create(
            paciente=self.paciente,
            profissional=self.profissional,
            data=datetime.now(),
            status='AGENDADO'
        )
        response = self.client.delete(reverse('clinica_api:agendamento_detail_update_delete_api', kwargs={'pk': agendamento.pk}))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Agendamento.objects.count(), 0)