import sys
import builtins
from unittest import TestCase
from unittest.mock import patch, MagicMock

from smartcli import cli


class CLIMainTest(TestCase):
    def setUp(self):
        self.stdout_patch = patch("sys.stdout")
        self.stderr_patch = patch("sys.stderr")
        self.mock_stdout = self.stdout_patch.start()
        self.mock_stderr = self.stderr_patch.start()

    def tearDown(self):
        self.stdout_patch.stop()
        self.stderr_patch.stop()

    @patch("smartcli.cli.print_help")
    def test_main_no_args_prints_help(self, mock_print_help):
        exit_code = cli.main([])
        mock_print_help.assert_called_once()
        self.assertEqual(exit_code, 0)

    @patch("smartcli.cli.print_help")
    def test_main_help_command(self, mock_print_help):
        exit_code = cli.main(["help"])
        mock_print_help.assert_called_once()
        self.assertEqual(exit_code, 0)

    @patch("smartcli.cli.print_version")
    def test_main_version_command(self, mock_print_version):
        for version_cmd in ["version", "--version", "-v"]:
            with self.subTest(cmd=version_cmd):
                exit_code = cli.main([version_cmd])
                mock_print_version.assert_called()
                self.assertEqual(exit_code, 0)
                mock_print_version.reset_mock()

    @patch("smartcli.cli.run_django_command")
    @patch("smartcli.cli.is_django_project", return_value=True)
    def test_main_known_commands(self, mock_is_django, mock_run_django):
        commands = [
            ("create-module", "create_module"),
            ("create-model", "create_model"),
            ("create-serializer", "create_serializer"),
            ("create-service", "create_service"),
            ("create-factory", "create_factory"),
            ("create-views", "create_views"),
            ("test", "test"),
        ]
        for cli_cmd, django_cmd in commands:
            with self.subTest(cli_cmd=cli_cmd):
                mock_run_django.reset_mock()
                exit_code = cli.main([cli_cmd, "foo", "bar"])
                mock_run_django.assert_called_once_with(django_cmd, ["foo", "bar"])

    @patch("smartcli.cli.print_help")
    def test_main_unknown_command(self, mock_print_help):
        with patch("builtins.print") as mock_print:
            exit_code = cli.main(["unknowncmd"])
            mock_print.assert_any_call("❌ Unknown command: unknowncmd")
            mock_print_help.assert_called_once()
            self.assertEqual(exit_code, 1)

    @patch("smartcli.cli.is_django_project", return_value=False)
    def test_run_django_command_not_in_django_project(self, mock_is_django):
        with patch("builtins.print") as mock_print:
            exit_code = cli.run_django_command("create_model", ["User", "users"])
            self.assertEqual(exit_code, 1)
            mock_print.assert_any_call("❌ Error: Not in a Django project directory")

    @patch("smartcli.cli.is_django_project", return_value=True)
    @patch("subprocess.run")
    def test_run_django_command_success(self, mock_subprocess, mock_is_django):
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "output"
        mock_result.stderr = ""
        mock_subprocess.return_value = mock_result
        with patch("builtins.print") as mock_print:
            exit_code = cli.run_django_command("create_model", ["User", "users"])
            self.assertEqual(exit_code, 0)
            mock_print.assert_any_call("output")

    @patch("smartcli.cli.is_django_project", return_value=True)
    @patch("subprocess.run", side_effect=FileNotFoundError)
    def test_run_django_command_python_not_found(self, mock_subprocess, mock_is_django):
        with patch("builtins.print") as mock_print:
            exit_code = cli.run_django_command("create_model", ["User", "users"])
            self.assertEqual(exit_code, 1)
            mock_print.assert_any_call("❌ Error: 'python' command not found")

    @patch("smartcli.cli.is_django_project", return_value=True)
    @patch("subprocess.run", side_effect=Exception("fail"))
    def test_run_django_command_other_exception(self, mock_subprocess, mock_is_django):
        with patch("builtins.print") as mock_print:
            exit_code = cli.run_django_command("create_model", ["User", "users"])
            self.assertEqual(exit_code, 1)
            mock_print.assert_any_call("❌ Error running Django command: fail")

    def test_is_django_project_true(self):
        with patch("os.path.exists", return_value=True):
            self.assertTrue(cli.is_django_project())

    def test_is_django_project_false(self):
        with patch("os.path.exists", return_value=False):
            self.assertFalse(cli.is_django_project())

    def test_print_help(self):
        with patch("builtins.print") as mock_print:
            cli.print_help()
            mock_print.assert_any_call("""
🚀 Django SmartCLI - Smart Command Line Interface for Django

USAGE:
    django-smartcli <command> [options]

COMMANDS:
    create-module <name>           Create a new Django module with complete structure
    create-model <name> <app>      Create a Django model with best practices
    create-serializer <name> <app> Create a DRF serializer
    create-service <name> <app>    Create a business logic service
    create-factory <name> <app>    Create a factory_boy factory
    create-views <name> <app>      Create a DRF ViewSet

OPTIONS:
    -h, --help     Show this help message
    -v, --version  Show version information

EXAMPLES:
    django-smartcli create-module users
    django-smartcli create-model UserProfile users
    django-smartcli create-serializer UserProfileSerializer users
    django-smartcli create-service UserProfileService users

For more information, visit: https://github.com/nathanrenard3/django-smartcli
""")

    def test_print_version(self):
        with patch("builtins.print") as mock_print:
            cli.print_version()
            mock_print.assert_any_call("Django SmartCLI v0.1.0")
            mock_print.assert_any_call("A smart CLI for Django to help you create and manage microservices")
            mock_print.assert_any_call("https://github.com/nathanrenard3/django-smartcli") 