import os
from django.test import TestCase, override_settings
from django.utils import timezone
from clinica.utils import get_upload_path
from unittest.mock import patch, MagicMock

@override_settings(MEDIA_ROOT=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_media'))
class GetUploadPathTestCase(TestCase):
    def tearDown(self):
        # Limpa o diretório de mídia de teste
        test_media_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_media')
        if os.path.exists(test_media_dir):
            for root, dirs, files in os.walk(test_media_dir, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir(test_media_dir)

    @patch('os.listdir')
    @patch('os.path.isfile')
    def test_get_upload_path_basic(self, mock_isfile, mock_listdir):
        """Testa o caminho de upload básico."""
        mock_listdir.return_value = []
        mock_isfile.return_value = True
        instance = MagicMock()
        filename = 'test.txt'
        model_name = 'documentos'
        today = timezone.now()
        expected_path = os.path.join('uploads', model_name, str(today.year), str(today.month).zfill(2), str(today.day).zfill(2), filename)
        path = get_upload_path(instance, filename, model_name)
        self.assertEqual(path, expected_path)

    @patch('os.listdir')
    @patch('os.path.isfile')
    def test_get_upload_path_new_directory(self, mock_isfile, mock_listdir):
        """Testa a criação de um novo diretório quando o limite de arquivos é atingido."""
        # Simula um diretório cheio
        mock_listdir.return_value = [f'file_{i}.txt' for i in range(1000)]
        mock_isfile.return_value = True
        instance = MagicMock()
        filename = 'test.txt'
        model_name = 'documentos'
        today = timezone.now()
        expected_path = os.path.join('uploads', model_name, str(today.year), str(today.month).zfill(2), str(today.day).zfill(2), '1', filename)
        path = get_upload_path(instance, filename, model_name)
        self.assertEqual(path, expected_path)