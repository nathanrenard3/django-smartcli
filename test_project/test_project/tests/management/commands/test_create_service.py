from django.core.management import call_command
from django.core.management.base import CommandError
from unittest import TestCase
from unittest.mock import patch, MagicMock

class CreateServiceCommandTest(TestCase):
    @patch("smartcli.management.commands.create_service.ensure_directory_exists")
    @patch("smartcli.management.commands.create_service.write_file_content")
    @patch("smartcli.management.commands.create_service.get_app_path", return_value="/fake/path/apps/users")
    @patch("smartcli.management.commands.create_service.check_file_exists", return_value=False)
    @patch("smartcli.management.commands.create_service.validate_pascal_case_name")
    @patch("smartcli.management.commands.create_service.validate_app_exists")
    @patch("smartcli.management.commands.create_service.validate_directory_exists")
    def test_create_service_success(self, mock_validate_dir, mock_validate_app, mock_validate_name, mock_check_exists, mock_get_app_path, mock_write_file, mock_ensure_dir):
        # Test successful service creation without errors
        with patch("builtins.print") as mock_print:
            call_command("create_service", "UserService", "users")
            # Verify that directories and files are created
            self.assertTrue(mock_ensure_dir.called)
            self.assertTrue(mock_write_file.called)
            # Verify that validation functions are called
            mock_validate_name.assert_called_once_with("UserService", "Service")
            mock_validate_app.assert_called_once_with("users")
            mock_validate_dir.assert_called_once_with("users", "services")

    @patch("smartcli.management.commands.create_service.get_app_path", return_value="/fake/path/apps/users")
    @patch("smartcli.management.commands.create_service.check_file_exists", return_value=True)
    def test_create_service_already_exists(self, mock_check_exists, mock_get_app_path):
        with self.assertRaises(CommandError) as cm:
            call_command("create_service", "UserService", "users")
        self.assertIn("already exists", str(cm.exception))

    @patch("smartcli.management.commands.create_service.validate_pascal_case_name", side_effect=ValueError("Service name 'userService' must start with an uppercase letter"))
    def test_create_service_invalid_name(self, mock_validate_name):
        with self.assertRaises(CommandError) as cm:
            call_command("create_service", "userService", "users")
        self.assertIn("Service name 'userService' must start with an uppercase letter", str(cm.exception))

    @patch("smartcli.management.commands.create_service.validate_app_exists", side_effect=ValueError("App 'nonexistent' does not exist"))
    def test_create_service_app_not_found(self, mock_validate_app):
        with self.assertRaises(CommandError) as cm:
            call_command("create_service", "UserService", "nonexistent")
        self.assertIn("App 'nonexistent' does not exist", str(cm.exception)) 