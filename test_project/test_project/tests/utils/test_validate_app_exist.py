from unittest.mock import patch
from django.test import TestCase

from smartcli import utils

class ValidateAppExistsTest(TestCase):
    """Test the validate_app_exists function."""

    @patch('smartcli.utils.get_app_path')
    @patch('os.path.exists')
    def test_app_exists(self, mock_exists, mock_get_app_path):
        """Test validation when app exists."""
        mock_get_app_path.return_value = "/path/to/app"
        mock_exists.return_value = True
        
        # Should not raise any exception
        utils.validate_app_exists("test_app")

    @patch('smartcli.utils.get_app_path')
    @patch('os.path.exists')
    def test_app_does_not_exist(self, mock_exists, mock_get_app_path):
        """Test validation when app does not exist."""
        mock_get_app_path.return_value = "/path/to/app"
        mock_exists.return_value = False
        
        with self.assertRaises(ValueError) as cm:
            utils.validate_app_exists("test_app")
        self.assertIn("does not exist", str(cm.exception))
