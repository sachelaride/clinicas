from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from clinica.models import User, Clinica

class UserAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.clinica = Clinica.objects.create(nome='Clinica Teste')
        self.admin_user = User.objects.create_superuser('admin_user_api', 'admin_user_api@example.com', 'password', perfil='ADMIN', clinica=self.clinica)
        self.client.login(username='admin_user_api', password='password')

    def test_user_list(self):
        """Testa a listagem de usuários."""
        response = self.client.get(reverse('clinica_api:user_list_create_api'))
        self.assertEqual(response.status_code, 200)

    def test_user_create(self):
        """Testa a criação de um usuário."""
        data = {
            'username': 'new_user',
            'email': 'new_user@example.com',
            'password': 'password123',
            'perfil': 'PACIENTE',
            'clinica': self.clinica.id
        }
        response = self.client.post(reverse('clinica_api:user_list_create_api'), data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_user_detail(self):
        """Testa o detalhe de um usuário."""
        user = User.objects.create_user('test_user', 'test_user@example.com', 'password', perfil='PACIENTE', clinica=self.clinica)
        response = self.client.get(reverse('clinica_api:user_detail_update_delete_api', kwargs={'pk': user.pk}))
        self.assertEqual(response.status_code, 200)

    def test_user_update(self):
        """Testa a atualização de um usuário."""
        user = User.objects.create_user('update_user', 'update_user@example.com', 'password', perfil='PACIENTE', clinica=self.clinica)
        updated_data = {
            'username': 'updated_user',
            'email': 'updated_user@example.com',
            'perfil': 'ATENDENTE',
            'clinica': self.clinica.id
        }
        response = self.client.put(reverse('clinica_api:user_detail_update_delete_api', kwargs={'pk': user.pk}), updated_data, format='json')
        self.assertEqual(response.status_code, 200)
        user.refresh_from_db()
        self.assertEqual(user.username, 'updated_user')

    def test_user_delete(self):
        """Testa a exclusão de um usuário."""
        user = User.objects.create_user('delete_user', 'delete_user@example.com', 'password', perfil='PACIENTE', clinica=self.clinica)
        response = self.client.delete(reverse('clinica_api:user_detail_update_delete_api', kwargs={'pk': user.pk}))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(User.objects.filter(username='delete_user').count(), 0)