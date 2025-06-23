from unittest.mock import patch
from django.test import TestCase

from smartcli import utils


class ValidateDirectoryExistsTest(TestCase):
    """Test the validate_directory_exists function."""

    @patch('smartcli.utils.get_app_path')
    @patch('os.path.exists')
    def test_directory_exists(self, mock_exists, mock_get_app_path):
        """Test validation when directory exists."""
        mock_get_app_path.return_value = "/path/to/app"
        mock_exists.return_value = True
        
        # Should not raise any exception
        utils.validate_directory_exists("test_app", "models")

    @patch('smartcli.utils.get_app_path')
    @patch('os.path.exists')
    def test_directory_does_not_exist(self, mock_exists, mock_get_app_path):
        """Test validation when directory does not exist."""
        mock_get_app_path.return_value = "/path/to/app"
        mock_exists.return_value = False
        
        with self.assertRaises(ValueError) as cm:
            utils.validate_directory_exists("test_app", "models")
        self.assertIn("does not exist", str(cm.exception))
