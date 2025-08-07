from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from clinica.models import Clinica, User

class ClinicaAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser('admin_clinica_api', 'admin_clinica_api@example.com', 'password', perfil='ADMIN')
        self.client.login(username='admin_clinica_api', password='password')

    def test_clinica_list(self):
        """Testa a listagem de clínicas."""
        response = self.client.get(reverse('clinica_api:clinica_list_create_api'))
        self.assertEqual(response.status_code, 200)

    def test_clinica_create(self):
        """Testa a criação de uma clínica."""
        data = {
            'nome': 'Nova Clinica',
            'endereco': 'Rua Nova, 123',
            'telefone': '11987654321'
        }
        response = self.client.post(reverse('clinica_api:clinica_list_create_api'), data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_clinica_detail(self):
        """Testa o detalhe de uma clínica."""
        clinica = Clinica.objects.create(nome='Clinica Detalhe', endereco='Rua Detalhe, 456', telefone='11123456789')
        response = self.client.get(reverse('clinica_api:clinica_detail_update_delete_api', kwargs={'pk': clinica.pk}))
        self.assertEqual(response.status_code, 200)

    def test_clinica_update(self):
        """Testa a atualização de uma clínica."""
        clinica = Clinica.objects.create(nome='Clinica Original', endereco='Rua Original, 789', telefone='11987654321')
        updated_data = {
            'nome': 'Clinica Atualizada',
            'endereco': 'Rua Atualizada, 987',
            'telefone': '11123456789'
        }
        response = self.client.put(reverse('clinica_api:clinica_detail_update_delete_api', kwargs={'pk': clinica.pk}), updated_data, format='json')
        self.assertEqual(response.status_code, 200)
        clinica.refresh_from_db()
        self.assertEqual(clinica.nome, 'Clinica Atualizada')

    def test_clinica_delete(self):
        """Testa a exclusão de uma clínica."""
        clinica = Clinica.objects.create(nome='Clinica a Deletar', endereco='Rua a Deletar, 123', telefone='11123456789')
        response = self.client.delete(reverse('clinica_api:clinica_detail_update_delete_api', kwargs={'pk': clinica.pk}))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Clinica.objects.count(), 0)