from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from clinica.models import Prontuario, Paciente, Clinica, User

class ProntuarioAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.clinica = Clinica.objects.create(nome='Clinica Teste')
        self.admin_user = User.objects.create_superuser('admin_prontuario_api', 'admin_prontuario_api@example.com', 'password', perfil='ADMIN', clinica=self.clinica)
        self.paciente_user = User.objects.create_user('paciente_user_prontuario_api', 'paciente_prontuario_api@teste.com', 'senha123', perfil='PACIENTE', clinica=self.clinica)
        self.paciente = Paciente.objects.create(
            nome='Paciente Prontuario API Teste',
            cpf='123.456.789-15',
            data_nascimento='1990-01-01',
            clinica=self.clinica
        )
        self.client.login(username='admin_prontuario_api', password='password')

    def test_prontuario_list(self):
        """Testa a listagem de prontuários."""
        response = self.client.get(reverse('clinica_api:prontuario_list_create_api'))
        self.assertEqual(response.status_code, 200)

    def test_prontuario_create(self):
        """Testa a criação de um prontuário."""
        data = {
            'paciente': self.paciente.id,
            'queixa_principal': 'Dor de cabeça'
        }
        response = self.client.post(reverse('clinica_api:prontuario_list_create_api'), data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_prontuario_detail(self):
        """Testa o detalhe de um prontuário."""
        prontuario = Prontuario.objects.create(paciente=self.paciente)
        response = self.client.get(reverse('clinica_api:prontuario_detail_update_delete_api', kwargs={'pk': prontuario.pk}))
        self.assertEqual(response.status_code, 200)

    def test_prontuario_update(self):
        """Testa a atualização de um prontuário."""
        prontuario = Prontuario.objects.create(paciente=self.paciente)
        updated_data = {
            'paciente': self.paciente.id,
            'queixa_principal': 'Enxaqueca'
        }
        response = self.client.put(reverse('clinica_api:prontuario_detail_update_delete_api', kwargs={'pk': prontuario.pk}), updated_data, format='json')
        self.assertEqual(response.status_code, 200)
        prontuario.refresh_from_db()
        self.assertEqual(prontuario.queixa_principal, 'Enxaqueca')

    def test_prontuario_delete(self):
        """Testa a exclusão de um prontuário."""
        prontuario = Prontuario.objects.create(paciente=self.paciente)
        response = self.client.delete(reverse('clinica_api:prontuario_detail_update_delete_api', kwargs={'pk': prontuario.pk}))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Prontuario.objects.count(), 0)