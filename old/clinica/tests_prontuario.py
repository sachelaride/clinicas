from django.test import TestCase
from clinica.models import Prontuario, Paciente, Clinica, User

class ProntuarioModelTestCase(TestCase):
    def setUp(self):
        self.clinica = Clinica.objects.create(nome='Clinica Teste')
        self.paciente_user = User.objects.create_user('paciente_user_prontuario', 'paciente_prontuario@teste.com', 'senha123', perfil='PACIENTE', clinica=self.clinica)
        self.paciente = Paciente.objects.create(
            nome='Paciente Prontuario Teste',
            cpf='123.456.789-12',
            data_nascimento='1990-01-01',
            clinica=self.clinica
        )

    def test_prontuario_creation(self):
        """Testa se um prontuário pode ser criado com sucesso."""
        prontuario = Prontuario.objects.create(paciente=self.paciente)
        self.assertIsNotNone(prontuario)
        self.assertEqual(Prontuario.objects.count(), 1)

    def test_prontuario_str(self):
        """Testa a representação em string do modelo Prontuario."""
        prontuario = Prontuario.objects.create(paciente=self.paciente)
        expected_str = f"Prontuário de {self.paciente} - {prontuario.data_criacao}"
        self.assertEqual(str(prontuario), expected_str)

    def test_prontuario_finalizado_nao_editavel(self):
        """Testa se um prontuário finalizado não é editável."""
        prontuario = Prontuario.objects.create(paciente=self.paciente, is_finalized=True)
        self.assertFalse(prontuario.editavel)