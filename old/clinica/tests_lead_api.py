from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from clinica.models import Lead, Clinica, User

class LeadAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.clinica = Clinica.objects.create(nome='Clinica Teste')
        self.admin_user = User.objects.create_superuser('admin_lead_api', 'admin_lead_api@example.com', 'password', perfil='ADMIN', clinica=self.clinica)
        self.client.login(username='admin_lead_api', password='password')

    def test_lead_list(self):
        """Testa a listagem de leads."""
        response = self.client.get(reverse('clinica_api:lead_list_create_api'))
        self.assertEqual(response.status_code, 200)

    def test_lead_create(self):
        """Testa a criação de um lead."""
        data = {
            'nome': 'Novo Lead',
            'email': 'novo_lead@example.com',
            'telefone': '11999999999',
            'clinica': self.clinica.id
        }
        response = self.client.post(reverse('clinica_api:lead_list_create_api'), data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_lead_detail(self):
        """Testa o detalhe de um lead."""
        lead = Lead.objects.create(nome='Lead Detalhe', email='detalhe@example.com', telefone='11111111111', clinica=self.clinica)
        response = self.client.get(reverse('clinica_api:lead_detail_update_delete_api', kwargs={'pk': lead.pk}))
        self.assertEqual(response.status_code, 200)

    def test_lead_update(self):
        """Testa a atualização de um lead."""
        lead = Lead.objects.create(nome='Lead Original', email='original@example.com', telefone='11222222222', clinica=self.clinica)
        updated_data = {
            'nome': 'Lead Atualizado',
            'email': 'atualizado@example.com',
            'telefone': '11333333333',
            'status': 'CONVERTIDO',
            'clinica': self.clinica.id
        }
        response = self.client.put(reverse('clinica_api:lead_detail_update_delete_api', kwargs={'pk': lead.pk}), updated_data, format='json')
        self.assertEqual(response.status_code, 200)
        lead.refresh_from_db()
        self.assertEqual(lead.nome, 'Lead Atualizado')

    def test_lead_delete(self):
        """Testa a exclusão de um lead."""
        lead = Lead.objects.create(nome='Lead a Deletar', email='deletar@example.com', telefone='11444444444', clinica=self.clinica)
        response = self.client.delete(reverse('clinica_api:lead_detail_update_delete_api', kwargs={'pk': lead.pk}))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Lead.objects.count(), 0)