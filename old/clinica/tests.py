from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework.test import APIClient
from clinica.models import User, Paciente, Clinica

@override_settings(LOGIN_URL='/test-login/')
class PacienteAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.clinica = Clinica.objects.create(nome='Clinica Teste', endereco='Rua Teste, 123', telefone='11999999999')
        self.admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'password', perfil='ADMIN', clinica=self.clinica)
        self.atendente_user = User.objects.create_user('atendente', 'atendente@example.com', 'password', perfil='ATENDENTE', clinica=self.clinica)
        self.paciente_user = User.objects.create_user('paciente', 'paciente@example.com', 'password', perfil='PACIENTE', clinica=self.clinica)

        # Login users for authenticated tests
        self.client.login(username='admin', password='password')
        self.client_atendente = APIClient()
        self.client_atendente.login(username='atendente', password='password')
        self.client_paciente = APIClient()
        self.client_paciente.login(username='paciente', password='password')

    def tearDown(self):
        pass

    def test_paciente_list_authenticated(self):
        """Testa se a listagem de pacientes funciona para usuários autenticados."""
        
        response = self.client.get(reverse('clinica_api:paciente_list_create_api'), follow=False)
        self.assertEqual(response.status_code, 200)

    def test_paciente_list_unauthenticated(self):
        """Testa se a listagem de pacientes retorna 403 para usuários não autenticados."""
        client = APIClient()
        response = client.get(reverse('clinica_api:paciente_list_create_api'), follow=False)
        self.assertEqual(response.status_code, 403)

    def test_paciente_create_authenticated(self):
        """Testa se a criação de paciente funciona para usuários autenticados com permissão."""
        data = {
            'nome': 'Novo Paciente',
            'cpf': '123.456.789-00',
            'email': 'novo@example.com',
            'telefone': '11987654321',
            'data_nascimento': '2000-01-01',
            'endereco': 'Rua Nova, 456',
            'clinica': self.clinica.id
        }
        response = self.client.post(reverse('clinica_api:paciente_list_create_api'), data, format='json', follow=False)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Paciente.objects.count(), 1)

    def test_paciente_create_unauthorized(self):
        """Testa se a criação de paciente retorna 403 para usuários sem permissão."""
        data = {
            'nome': 'Paciente Sem Permissao',
            'cpf': '987.654.321-00',
            'email': 'sempermissao@example.com',
            'telefone': '11912345678',
            'data_nascimento': '2000-01-01',
            'endereco': 'Rua Proibida, 789',
            'clinica': self.clinica.id
        }
        response = self.client_paciente.post(reverse('clinica_api:paciente_list_create_api'), data, format='json', follow=False)
        self.assertEqual(response.status_code, 403)

    def test_paciente_detail_authenticated(self):
        """Testa se o detalhe do paciente funciona para usuários autenticados."""
        paciente = Paciente.objects.create(nome='Paciente Detalhe', cpf='111.222.333-44', email='detalhe@example.com', telefone='11111111111', data_nascimento='1990-05-10', clinica=self.clinica)
        response = self.client.get(reverse('clinica_api:paciente_detail_update_delete_api', kwargs={'pk': paciente.pk}), follow=False)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['nome'], 'Paciente Detalhe')

    def test_paciente_update_authenticated(self):
        """Testa se a atualização de paciente funciona para usuários autenticados com permissão."""
        paciente = Paciente.objects.create(nome='Paciente Original', cpf='222.333.444-55', email='original@example.com', telefone='22222222222', data_nascimento='1985-03-15', clinica=self.clinica)
        updated_data = {
            'nome': 'Paciente Atualizado',
            'cpf': '222.333.444-55',
            'email': 'atualizado@example.com',
            'telefone': '22222222222',
            'data_nascimento': '1985-03-15',
            'endereco': 'Rua Atualizada, 789',
            'clinica': self.clinica.id
        }
        response = self.client.put(reverse('clinica_api:paciente_detail_update_delete_api', kwargs={'pk': paciente.pk}), updated_data, format='json', follow=False)
        self.assertEqual(response.status_code, 200)
        paciente.refresh_from_db()
        self.assertEqual(paciente.nome, 'Paciente Atualizado')

    def test_paciente_delete_authenticated(self):
        """Testa se a exclusão de paciente funciona para usuários autenticados com permissão."""
        paciente = Paciente.objects.create(nome='Paciente a Deletar', cpf='333.444.555-66', email='deletar@example.com', telefone='33333333333', data_nascimento='1970-01-01', clinica=self.clinica)
        response = self.client.delete(reverse('clinica_api:paciente_detail_update_delete_api', kwargs={'pk': paciente.pk}), follow=False)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Paciente.objects.count(), 0)