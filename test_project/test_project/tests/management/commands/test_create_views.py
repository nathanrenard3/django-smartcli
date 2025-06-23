from django.core.management import call_command
from django.core.management.base import CommandError
from unittest import TestCase
from unittest.mock import patch, MagicMock

class CreateViewsCommandTest(TestCase):
    @patch("smartcli.management.commands.create_views.ensure_directory_exists")
    @patch("smartcli.management.commands.create_views.write_file_content")
    @patch("smartcli.management.commands.create_views.get_app_path", return_value="/fake/path/apps/users")
    @patch("smartcli.management.commands.create_views.check_file_exists", return_value=False)
    @patch("smartcli.management.commands.create_views.validate_pascal_case_name")
    @patch("smartcli.management.commands.create_views.validate_app_exists")
    @patch("smartcli.management.commands.create_views.validate_directory_exists")
    def test_create_views_success(self, mock_validate_dir, mock_validate_app, mock_validate_name, mock_check_exists, mock_get_app_path, mock_write_file, mock_ensure_dir):
        # Test successful view creation without errors
        with patch("builtins.print") as mock_print:
            call_command("create_views", "UserViewSet", "users")
            # Verify that directories and files are created
            self.assertTrue(mock_ensure_dir.called)
            self.assertTrue(mock_write_file.called)
            # Verify that validation functions are called
            mock_validate_name.assert_called_once_with("UserViewSet", "View")
            mock_validate_app.assert_called_once_with("users")
            mock_validate_dir.assert_called_once_with("users", "views")

    @patch("smartcli.management.commands.create_views.get_app_path", return_value="/fake/path/apps/users")
    @patch("smartcli.management.commands.create_views.check_file_exists", return_value=True)
    def test_create_views_already_exists(self, mock_check_exists, mock_get_app_path):
        with self.assertRaises(CommandError) as cm:
            call_command("create_views", "UserViewSet", "users")
        self.assertIn("already exists", str(cm.exception))

    @patch("smartcli.management.commands.create_views.validate_pascal_case_name", side_effect=ValueError("View name 'userViewSet' must start with an uppercase letter"))
    def test_create_views_invalid_name(self, mock_validate_name):
        with self.assertRaises(CommandError) as cm:
            call_command("create_views", "userViewSet", "users")
        self.assertIn("View name 'userViewSet' must start with an uppercase letter", str(cm.exception))

    @patch("smartcli.management.commands.create_views.validate_app_exists", side_effect=ValueError("App 'nonexistent' does not exist"))
    def test_create_views_app_not_found(self, mock_validate_app):
        with self.assertRaises(CommandError) as cm:
            call_command("create_views", "UserViewSet", "nonexistent")
        self.assertIn("App 'nonexistent' does not exist", str(cm.exception))

    @patch("smartcli.management.commands.create_views.ensure_directory_exists")
    @patch("smartcli.management.commands.create_views.write_file_content")
    @patch("smartcli.management.commands.create_views.get_app_path", return_value="/fake/path/apps/users")
    @patch("smartcli.management.commands.create_views.check_file_exists", return_value=False)
    @patch("smartcli.management.commands.create_views.validate_pascal_case_name")
    @patch("smartcli.management.commands.create_views.validate_app_exists")
    @patch("smartcli.management.commands.create_views.validate_directory_exists")
    def test_create_views_with_model_option(self, mock_validate_dir, mock_validate_app, mock_validate_name, mock_check_exists, mock_get_app_path, mock_write_file, mock_ensure_dir):
        # Test view creation with --model option
        with patch("builtins.print") as mock_print:
            call_command("create_views", "UserViewSet", "users", model="CustomUser")
            # Verify that validation functions are called with correct parameters
            mock_validate_name.assert_any_call("UserViewSet", "View")
            mock_validate_name.assert_any_call("CustomUser", "Model")

    @patch("smartcli.management.commands.create_views.ensure_directory_exists")
    @patch("smartcli.management.commands.create_views.write_file_content")
    @patch("smartcli.management.commands.create_views.get_app_path", return_value="/fake/path/apps/users")
    @patch("smartcli.management.commands.create_views.check_file_exists", return_value=False)
    @patch("smartcli.management.commands.create_views.validate_pascal_case_name")
    @patch("smartcli.management.commands.create_views.validate_app_exists")
    @patch("smartcli.management.commands.create_views.validate_directory_exists")
    def test_create_views_dependencies_warnings(self, mock_validate_dir, mock_validate_app, mock_validate_name, mock_check_exists, mock_get_app_path, mock_write_file, mock_ensure_dir):
        # Test view creation with missing dependencies (should show warnings but not fail)
        with patch("smartcli.management.commands.create_views._check_model_exists", return_value=False):
            with patch("smartcli.management.commands.create_views._check_serializer_exists", return_value=False):
                with patch("smartcli.management.commands.create_views._check_service_exists", return_value=False):
                    with patch("builtins.print") as mock_print:
                        call_command("create_views", "UserViewSet", "users")
                        # Verify that warning messages are displayed for missing dependencies
                        mock_print.assert_any_call("Note: Model 'User' was not found. Make sure the model exists before using this view.")
                        mock_print.assert_any_call("Note: Serializer 'UserSerializer' was not found. Make sure the serializer exists before using this view.")
                        mock_print.assert_any_call("Note: Service 'UserService' was not found. Make sure the service exists before using this view.") 