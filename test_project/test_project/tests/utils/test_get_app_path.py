from unittest.mock import patch
from django.test import TestCase

import os
from smartcli import utils


class GetAppPathTest(TestCase):
    """Test the get_app_path function."""

    @patch('smartcli.utils.get_apps_directory')
    @patch('smartcli.utils.settings')
    def test_centralized_structure(self, mock_settings, mock_get_apps_dir):
        """Test app path for centralized structure."""
        mock_settings.BASE_DIR = "/project/root"
        mock_get_apps_dir.return_value = "apps"
        
        result = utils.get_app_path("users")
        expected = os.path.join("/project/root", "apps", "users")
        self.assertEqual(result, expected)

    @patch('smartcli.utils.get_apps_directory')
    @patch('smartcli.utils.settings')
    def test_decentralized_structure(self, mock_settings, mock_get_apps_dir):
        """Test app path for decentralized structure."""
        mock_settings.BASE_DIR = "/project/root"
        mock_get_apps_dir.return_value = ""
        
        result = utils.get_app_path("users")
        expected = os.path.join("/project/root", "users")
        self.assertEqual(result, expected)