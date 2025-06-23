from unittest.mock import patch
from django.test import TestCase

from smartcli import utils


class GetAppImportPathTest(TestCase):
    """Test the get_app_import_path function."""

    @patch('smartcli.utils.get_apps_directory')
    def test_centralized_structure(self, mock_get_apps_dir):
        """Test import path for centralized structure."""
        mock_get_apps_dir.return_value = "apps"
        
        result = utils.get_app_import_path("users")
        self.assertEqual(result, "apps.users")

    @patch('smartcli.utils.get_apps_directory')
    def test_decentralized_structure(self, mock_get_apps_dir):
        """Test import path for decentralized structure."""
        mock_get_apps_dir.return_value = ""
        
        result = utils.get_app_import_path("users")
        self.assertEqual(result, "users")