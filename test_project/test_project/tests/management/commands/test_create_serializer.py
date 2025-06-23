from django.core.management import call_command
from django.core.management.base import CommandError
from unittest import TestCase
from unittest.mock import patch, MagicMock

class CreateSerializerCommandTest(TestCase):
    @patch("smartcli.management.commands.create_serializer.ensure_directory_exists")
    @patch("smartcli.management.commands.create_serializer.write_file_content")
    @patch("smartcli.management.commands.create_serializer.get_app_path", return_value="/fake/path/apps/users")
    @patch("smartcli.management.commands.create_serializer.check_file_exists", return_value=False)
    @patch("smartcli.management.commands.create_serializer.validate_pascal_case_name")
    @patch("smartcli.management.commands.create_serializer.validate_app_exists")
    @patch("smartcli.management.commands.create_serializer.validate_directory_exists")
    def test_create_serializer_success(self, mock_validate_dir, mock_validate_app, mock_validate_name, mock_check_exists, mock_get_app_path, mock_write_file, mock_ensure_dir):
        # Test successful serializer creation without errors
        with patch("builtins.print") as mock_print:
            call_command("create_serializer", "UserSerializer", "users")
            # Verify that directories and files are created
            self.assertTrue(mock_ensure_dir.called)
            self.assertTrue(mock_write_file.called)
            # Verify that validation functions are called
            mock_validate_name.assert_called_once_with("UserSerializer", "Serializer")
            mock_validate_app.assert_called_once_with("users")
            mock_validate_dir.assert_called_once_with("users", "serializers")

    @patch("smartcli.management.commands.create_serializer.get_app_path", return_value="/fake/path/apps/users")
    @patch("smartcli.management.commands.create_serializer.check_file_exists", return_value=True)
    def test_create_serializer_already_exists(self, mock_check_exists, mock_get_app_path):
        with self.assertRaises(CommandError) as cm:
            call_command("create_serializer", "UserSerializer", "users")
        self.assertIn("already exists", str(cm.exception))

    @patch("smartcli.management.commands.create_serializer.validate_pascal_case_name", side_effect=ValueError("Serializer name 'userSerializer' must start with an uppercase letter"))
    def test_create_serializer_invalid_name(self, mock_validate_name):
        with self.assertRaises(CommandError) as cm:
            call_command("create_serializer", "userSerializer", "users")
        self.assertIn("Serializer name 'userSerializer' must start with an uppercase letter", str(cm.exception))

    @patch("smartcli.management.commands.create_serializer.validate_app_exists", side_effect=ValueError("App 'nonexistent' does not exist"))
    def test_create_serializer_app_not_found(self, mock_validate_app):
        with self.assertRaises(CommandError) as cm:
            call_command("create_serializer", "UserSerializer", "nonexistent")
        self.assertIn("App 'nonexistent' does not exist", str(cm.exception))

    @patch("smartcli.management.commands.create_serializer.ensure_directory_exists")
    @patch("smartcli.management.commands.create_serializer.write_file_content")
    @patch("smartcli.management.commands.create_serializer.get_app_path", return_value="/fake/path/apps/users")
    @patch("smartcli.management.commands.create_serializer.check_file_exists", return_value=False)
    @patch("smartcli.management.commands.create_serializer.validate_pascal_case_name")
    @patch("smartcli.management.commands.create_serializer.validate_app_exists")
    @patch("smartcli.management.commands.create_serializer.validate_directory_exists")
    def test_create_serializer_with_model_option(self, mock_validate_dir, mock_validate_app, mock_validate_name, mock_check_exists, mock_get_app_path, mock_write_file, mock_ensure_dir):
        # Test serializer creation with --model option
        with patch("builtins.print") as mock_print:
            call_command("create_serializer", "UserSerializer", "users", model="CustomUser")
            # Verify that validation functions are called with correct parameters
            mock_validate_name.assert_any_call("UserSerializer", "Serializer")
            mock_validate_name.assert_any_call("CustomUser", "Model") 