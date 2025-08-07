from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from clinica.models import LancamentoFinanceiro, Clinica, User
from datetime import date

class LancamentoFinanceiroAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.clinica = Clinica.objects.create(nome='Clinica Teste')
        self.admin_user = User.objects.create_superuser('admin_lancamento_api', 'admin_lancamento_api@example.com', 'password', perfil='ADMIN', clinica=self.clinica)
        self.client.login(username='admin_lancamento_api', password='password')

    def test_lancamento_financeiro_list(self):
        """Testa a listagem de lançamentos financeiros."""
        response = self.client.get(reverse('clinica_api:lancamento_financeiro_list_create_api'))
        self.assertEqual(response.status_code, 200)

    def test_lancamento_financeiro_create(self):
        """Testa a criação de um lançamento financeiro."""
        data = {
            'descricao': 'Aluguel',
            'valor': '1500.00',
            'tipo': 'DESPESA',
            'data_vencimento': date.today().isoformat()
        }
        response = self.client.post(reverse('clinica_api:lancamento_financeiro_list_create_api'), data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_lancamento_financeiro_detail(self):
        """Testa o detalhe de um lançamento financeiro."""
        lancamento = LancamentoFinanceiro.objects.create(
            descricao='Salário',
            valor='3000.00',
            tipo='RECEITA',
            data_vencimento=date.today()
        )
        response = self.client.get(reverse('clinica_api:lancamento_financeiro_detail_update_delete_api', kwargs={'pk': lancamento.pk}))
        self.assertEqual(response.status_code, 200)

    def test_lancamento_financeiro_update(self):
        """Testa a atualização de um lançamento financeiro."""
        lancamento = LancamentoFinanceiro.objects.create(
            descricao='Material de Escritório',
            valor='200.00',
            tipo='DESPESA',
            data_vencimento=date.today()
        )
        updated_data = {
            'descricao': 'Material de Limpeza',
            'valor': '250.00',
            'tipo': 'DESPESA',
            'data_vencimento': date.today().isoformat()
        }
        response = self.client.put(reverse('clinica_api:lancamento_financeiro_detail_update_delete_api', kwargs={'pk': lancamento.pk}), updated_data, format='json')
        self.assertEqual(response.status_code, 200)
        lancamento.refresh_from_db()
        self.assertEqual(lancamento.descricao, 'Material de Limpeza')

    def test_lancamento_financeiro_delete(self):
        """Testa a exclusão de um lançamento financeiro."""
        lancamento = LancamentoFinanceiro.objects.create(
            descricao='Conta de Luz',
            valor='500.00',
            tipo='DESPESA',
            data_vencimento=date.today()
        )
        response = self.client.delete(reverse('clinica_api:lancamento_financeiro_detail_update_delete_api', kwargs={'pk': lancamento.pk}))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(LancamentoFinanceiro.objects.count(), 0)