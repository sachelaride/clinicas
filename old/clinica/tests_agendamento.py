from django.test import TestCase
from clinica.models import Agendamento, Paciente, Profissional, Clinica, User
from datetime import datetime

class AgendamentoModelTestCase(TestCase):
    def setUp(self):
        self.clinica = Clinica.objects.create(nome='Clinica Teste')
        self.paciente_user = User.objects.create_user('paciente_user', 'paciente@teste.com', 'senha123', perfil='PACIENTE', clinica=self.clinica)
        self.paciente = Paciente.objects.create(
            nome='Paciente Teste',
            cpf='123.456.789-10',
            data_nascimento='1990-01-01',
            clinica=self.clinica
        )
        self.profissional_user = User.objects.create_user('profissional_user', 'profissional@teste.com', 'senha123', perfil='PROFISSIONAL', clinica=self.clinica)
        self.profissional = Profissional.objects.create(user=self.profissional_user, especialidade='Cardiologia')

    def test_agendamento_creation(self):
        """Testa se um agendamento pode ser criado com sucesso."""
        agendamento = Agendamento.objects.create(
            paciente=self.paciente,
            profissional=self.profissional,
            data=datetime.now(),
            status='AGENDADO'
        )
        self.assertIsNotNone(agendamento)
        self.assertEqual(Agendamento.objects.count(), 1)

    def test_agendamento_str(self):
        """Testa a representação em string do modelo Agendamento."""
        data_agendamento = datetime.now()
        agendamento = Agendamento.objects.create(
            paciente=self.paciente,
            profissional=self.profissional,
            data=data_agendamento
        )
        expected_str = f"Agendamento de {self.paciente.nome} com {self.profissional.user.username} em {data_agendamento}"
        self.assertEqual(str(agendamento), expected_str)