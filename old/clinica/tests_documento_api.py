from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from clinica.models import DocumentoArquivo, PastaDocumento, Paciente, Clinica, User
from django.core.files.uploadedfile import SimpleUploadedFile

class DocumentoArquivoAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.clinica = Clinica.objects.create(nome='Clinica Teste')
        self.admin_user = User.objects.create_superuser('admin_documento_api', 'admin_documento_api@example.com', 'password', perfil='ADMIN', clinica=self.clinica)
        self.paciente = Paciente.objects.create(
            nome='Paciente Documento Teste',
            cpf='111.222.333-44',
            data_nascimento='1990-01-01',
            clinica=self.clinica
        )
        self.pasta = PastaDocumento.objects.create(nome='Pasta Teste', clinica=self.clinica)
        self.client.login(username='admin_documento_api', password='password')

    def test_documento_list(self):
        """Testa a listagem de documentos."""
        response = self.client.get(reverse('clinica_api:documento_list_create_api'))
        self.assertEqual(response.status_code, 200)

    def test_documento_create(self):
        """Testa a criação de um documento."""
        file_content = b'Este  um contedo de teste.'
        test_file = SimpleUploadedFile("file.txt", file_content, content_type="text/plain")
        data = {
            'pasta': self.pasta.id,
            'paciente': self.paciente.id,
            'arquivo': test_file
        }
        response = self.client.post(reverse('clinica_api:documento_list_create_api'), data, format='multipart')
        self.assertEqual(response.status_code, 201)

    def test_documento_detail(self):
        """Testa o detalhe de um documento."""
        file_content = b'Contedo do documento de detalhe.'
        test_file = SimpleUploadedFile("detail.txt", file_content, content_type="text/plain")
        documento = DocumentoArquivo.objects.create(pasta=self.pasta, paciente=self.paciente, arquivo=test_file)
        response = self.client.get(reverse('clinica_api:documento_detail_update_delete_api', kwargs={'pk': documento.pk}))
        self.assertEqual(response.status_code, 200)

    def test_documento_update(self):
        """Testa a atualização de um documento."""
        file_content = b'Contedo original.'
        test_file = SimpleUploadedFile("original.txt", file_content, content_type="text/plain")
        documento = DocumentoArquivo.objects.create(pasta=self.pasta, paciente=self.paciente, arquivo=test_file)
        original_hash = documento.hash_arquivo # Capture o hash original

        updated_file_content = b'Contedo atualizado.'
        updated_test_file = SimpleUploadedFile("updated.txt", updated_file_content, content_type="text/plain")
        updated_data = {
            'pasta': self.pasta.id,
            'paciente': self.paciente.id,
            'arquivo': updated_test_file
        }
        response = self.client.put(reverse('clinica_api:documento_detail_update_delete_api', kwargs={'pk': documento.pk}), updated_data, format='multipart')
        self.assertEqual(response.status_code, 200)
        documento.refresh_from_db()
        # Verifica se o hash do arquivo foi atualizado, indicando que um novo arquivo foi salvo
        self.assertNotEqual(original_hash, documento.hash_arquivo)

    def test_documento_delete(self):
        """Testa a exclusão de um documento."""
        file_content = b'Contedo a ser deletado.'
        test_file = SimpleUploadedFile("delete.txt", file_content, content_type="text/plain")
        documento = DocumentoArquivo.objects.create(pasta=self.pasta, paciente=self.paciente, arquivo=test_file)
        response = self.client.delete(reverse('clinica_api:documento_detail_update_delete_api', kwargs={'pk': documento.pk}))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(DocumentoArquivo.objects.count(), 0)