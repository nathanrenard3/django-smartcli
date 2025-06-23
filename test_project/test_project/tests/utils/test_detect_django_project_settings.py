from unittest.mock import patch
from django.test import TestCase

from smartcli import utils


class DetectDjangoProjectSettingsTest(TestCase):
    """Test detect_django_project_settings function."""

    @patch('smartcli.utils.settings')
    @patch('os.path.exists')
    def test_detect_standard_structure(self, mock_exists, mock_settings):
        """Test detection of standard Django project structure."""
        mock_settings.BASE_DIR = "/project/test_project"
        mock_exists.side_effect = lambda path: path.endswith("settings.py")
        
        project_dir, settings_file = utils.detect_django_project_settings()
        
        self.assertEqual(project_dir, "test_project")
        self.assertEqual(settings_file, "/project/test_project/test_project/settings.py")

    @patch('smartcli.utils.settings')
    @patch('os.path.exists')
    def test_detect_direct_settings(self, mock_exists, mock_settings):
        """Test detection of direct settings.py file."""
        mock_settings.BASE_DIR = "/project/test_project"
        mock_exists.side_effect = lambda path: path == "/project/test_project/settings.py"
        
        project_dir, settings_file = utils.detect_django_project_settings()
        
        self.assertEqual(project_dir, "test_project")
        self.assertEqual(settings_file, "/project/test_project/settings.py")

    @patch('smartcli.utils.settings')
    @patch('os.path.exists')
    def test_detect_settings_module(self, mock_exists, mock_settings):
        """Test detection of settings module structure."""
        mock_settings.BASE_DIR = "/project/test_project"
        mock_exists.side_effect = lambda path: path.endswith("__init__.py")
        
        project_dir, settings_file = utils.detect_django_project_settings()
        
        self.assertEqual(project_dir, "test_project")
        self.assertEqual(settings_file, "/project/test_project/settings/__init__.py")

    @patch('smartcli.utils.settings')
    @patch('os.path.exists')
    def test_detect_no_settings_found(self, mock_exists, mock_settings):
        """Test when no settings file is found."""
        mock_settings.BASE_DIR = "/project/test_project"
        mock_exists.return_value = False
        
        project_dir, settings_file = utils.detect_django_project_settings()
        
        self.assertIsNone(project_dir)
        self.assertIsNone(settings_file)
