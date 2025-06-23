from django.core.management import call_command
from django.core.management.base import CommandError
from unittest import TestCase
from unittest.mock import patch, MagicMock

class CreateModuleCommandTest(TestCase):
    @patch("smartcli.management.commands.create_module.ensure_directory_exists")
    @patch("smartcli.management.commands.create_module.write_file_content")
    @patch("smartcli.management.commands.create_module.get_app_path", return_value="/fake/path/apps/users")
    @patch("smartcli.management.commands.create_module.get_apps_directory", return_value="apps")
    @patch("smartcli.management.commands.create_module.check_file_exists", return_value=False)
    @patch("smartcli.management.commands.create_module.get_app_import_path", return_value="apps.users")
    @patch("smartcli.management.commands.create_module.detect_django_project_settings", return_value=("test_project", "/fake/path/settings.py"))
    @patch("smartcli.management.commands.create_module.find_installed_apps_in_settings", return_value=(True, "INSTALLED_APPS = [\n    'django.contrib.admin',\n]") )
    def test_create_module_success(self, mock_find_installed, mock_detect_settings, mock_get_import, mock_check_exists, mock_get_apps_dir, mock_get_app_path, mock_write_file, mock_ensure_dir):
        # Test successful module creation without errors
        with patch("builtins.print") as mock_print:
            call_command("create_module", "users")
            # Verify that directories and files are created
            self.assertTrue(mock_ensure_dir.called)
            self.assertTrue(mock_write_file.called)
            # Verify that a success message is displayed
            mock_print.assert_any_call("Module 'users' created in centralized structure (apps/users/)")

    @patch("smartcli.management.commands.create_module.get_app_path", return_value="/fake/path/apps/users")
    @patch("smartcli.management.commands.create_module.check_file_exists", return_value=True)
    def test_create_module_already_exists(self, mock_check_exists, mock_get_app_path):
        with self.assertRaises(CommandError) as cm:
            call_command("create_module", "users")
        self.assertIn("already exists", str(cm.exception))

    def test_create_module_invalid_name(self):
        with self.assertRaises(CommandError) as cm:
            call_command("create_module", "123invalid")
        self.assertIn("is not a valid Python identifier", str(cm.exception)) 