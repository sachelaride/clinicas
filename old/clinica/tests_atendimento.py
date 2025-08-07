from django.test import TestCase
from clinica.models import Atendimento, Agendamento, Paciente, Profissional, Clinica, User
from datetime import datetime

class AtendimentoModelTestCase(TestCase):
    def setUp(self):
        self.clinica = Clinica.objects.create(nome='Clinica Teste')
        self.paciente_user = User.objects.create_user('paciente_user_atendimento', 'paciente_atendimento@teste.com', 'senha123', perfil='PACIENTE', clinica=self.clinica)
        self.paciente = Paciente.objects.create(
            nome='Paciente Atendimento Teste',
            cpf='123.456.789-11',
            data_nascimento='1990-01-01',
            clinica=self.clinica
        )
        self.profissional_user = User.objects.create_user('profissional_user_atendimento', 'profissional_atendimento@teste.com', 'senha123', perfil='PROFISSIONAL', clinica=self.clinica)
        self.profissional = Profissional.objects.create(user=self.profissional_user, especialidade='Cardiologia')
        self.agendamento = Agendamento.objects.create(
            paciente=self.paciente,
            profissional=self.profissional,
            data=datetime.now(),
            status='AGENDADO'
        )

    def test_atendimento_creation(self):
        """Testa se um atendimento pode ser criado com sucesso."""
        atendimento = Atendimento.objects.create(agendamento=self.agendamento)
        self.assertIsNotNone(atendimento)
        self.assertEqual(Atendimento.objects.count(), 1)

    def test_atendimento_str(self):
        """Testa a representação em string do modelo Atendimento."""
        atendimento = Atendimento.objects.create(agendamento=self.agendamento)
        expected_str = f"Atendimento de {self.agendamento.paciente.nome} por {self.agendamento.profissional.user.username}"
        self.assertEqual(str(atendimento), expected_str)