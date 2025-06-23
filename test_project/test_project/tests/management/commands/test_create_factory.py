from django.core.management import call_command
from django.core.management.base import CommandError
from unittest import TestCase
from unittest.mock import patch, MagicMock

class CreateFactoryCommandTest(TestCase):
    @patch("smartcli.management.commands.create_factory.write_file_content")
    @patch("smartcli.management.commands.create_factory.get_app_path", return_value="/fake/path/apps/users")
    @patch("smartcli.management.commands.create_factory.check_file_exists", return_value=False)
    @patch("smartcli.management.commands.create_factory.validate_pascal_case_name")
    @patch("smartcli.management.commands.create_factory.validate_app_exists")
    @patch("smartcli.management.commands.create_factory.validate_directory_exists")
    def test_create_factory_success(self, mock_validate_dir, mock_validate_app, mock_validate_name, mock_check_exists, mock_get_app_path, mock_write_file):
        # Test successful factory creation without errors
        with patch("builtins.print") as mock_print:
            call_command("create_factory", "UserFactory", "users")
            # Verify that files are created
            self.assertTrue(mock_write_file.called)
            # Verify that validation functions are called
            mock_validate_name.assert_called_once_with("UserFactory", "Factory")
            mock_validate_app.assert_called_once_with("users")
            mock_validate_dir.assert_called_once_with("users", "factories")

    @patch("smartcli.management.commands.create_factory.get_app_path", return_value="/fake/path/apps/users")
    @patch("smartcli.management.commands.create_factory.check_file_exists", return_value=True)
    def test_create_factory_already_exists(self, mock_check_exists, mock_get_app_path):
        with self.assertRaises(CommandError) as cm:
            call_command("create_factory", "UserFactory", "users")
        self.assertIn("already exists", str(cm.exception))

    @patch("smartcli.management.commands.create_factory.validate_pascal_case_name", side_effect=ValueError("Factory name 'userFactory' must start with an uppercase letter"))
    def test_create_factory_invalid_name(self, mock_validate_name):
        with self.assertRaises(CommandError) as cm:
            call_command("create_factory", "userFactory", "users")
        self.assertIn("Factory name 'userFactory' must start with an uppercase letter", str(cm.exception))

    @patch("smartcli.management.commands.create_factory.validate_app_exists", side_effect=ValueError("App 'nonexistent' does not exist"))
    def test_create_factory_app_not_found(self, mock_validate_app):
        with self.assertRaises(CommandError) as cm:
            call_command("create_factory", "UserFactory", "nonexistent")
        self.assertIn("App 'nonexistent' does not exist", str(cm.exception))

    @patch("smartcli.management.commands.create_factory.write_file_content")
    @patch("smartcli.management.commands.create_factory.get_app_path", return_value="/fake/path/apps/users")
    @patch("smartcli.management.commands.create_factory.check_file_exists", return_value=False)
    @patch("smartcli.management.commands.create_factory.validate_pascal_case_name")
    @patch("smartcli.management.commands.create_factory.validate_app_exists")
    @patch("smartcli.management.commands.create_factory.validate_directory_exists")
    def test_create_factory_model_not_found_warning(self, mock_validate_dir, mock_validate_app, mock_validate_name, mock_check_exists, mock_get_app_path, mock_write_file):
        # Test factory creation when model doesn't exist (should show warning but not fail)
        with patch("smartcli.management.commands.create_factory._check_model_exists", return_value=False):
            with patch("builtins.print") as mock_print:
                call_command("create_factory", "UserFactory", "users")
                # Verify that a warning message is displayed
                mock_print.assert_any_call("Note: Model 'User' was not found. Make sure the model exists before using this factory.") 