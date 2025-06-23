from django.core.management import call_command
from django.core.management.base import CommandError
from unittest import TestCase
from unittest.mock import patch, MagicMock

class CreateModelCommandTest(TestCase):
    @patch("smartcli.management.commands.create_model.ensure_directory_exists")
    @patch("smartcli.management.commands.create_model.write_file_content")
    @patch("smartcli.management.commands.create_model.get_app_path", return_value="/fake/path/apps/users")
    @patch("smartcli.management.commands.create_model.get_app_import_path", return_value="apps.users")
    @patch("smartcli.management.commands.create_model.check_file_exists", return_value=False)
    @patch("smartcli.management.commands.create_model.validate_pascal_case_name")
    @patch("smartcli.management.commands.create_model.validate_app_exists")
    @patch("smartcli.management.commands.create_model.validate_directory_exists")
    def test_create_model_success(self, mock_validate_dir, mock_validate_app, mock_validate_name, mock_check_exists, mock_get_import, mock_get_app_path, mock_write_file, mock_ensure_dir):
        # Test successful model creation without errors
        with patch("builtins.print") as mock_print:
            call_command("create_model", "User", "users")
            # Verify that directories and files are created
            self.assertTrue(mock_ensure_dir.called)
            self.assertTrue(mock_write_file.called)
            # Verify that validation functions are called
            mock_validate_name.assert_called_once_with("User", "Model")
            mock_validate_app.assert_called_once_with("users")
            mock_validate_dir.assert_called_once_with("users", "models")

    @patch("smartcli.management.commands.create_model.get_app_path", return_value="/fake/path/apps/users")
    @patch("smartcli.management.commands.create_model.check_file_exists", return_value=True)
    def test_create_model_already_exists(self, mock_check_exists, mock_get_app_path):
        with self.assertRaises(CommandError) as cm:
            call_command("create_model", "User", "users")
        self.assertIn("already exists", str(cm.exception))

    @patch("smartcli.management.commands.create_model.validate_pascal_case_name", side_effect=ValueError("Model name 'user' must start with an uppercase letter"))
    def test_create_model_invalid_name(self, mock_validate_name):
        with self.assertRaises(CommandError) as cm:
            call_command("create_model", "user", "users")
        self.assertIn("Model name 'user' must start with an uppercase letter", str(cm.exception))

    @patch("smartcli.management.commands.create_model.validate_app_exists", side_effect=ValueError("App 'nonexistent' does not exist"))
    def test_create_model_app_not_found(self, mock_validate_app):
        with self.assertRaises(CommandError) as cm:
            call_command("create_model", "User", "nonexistent")
        self.assertIn("App 'nonexistent' does not exist", str(cm.exception)) 