from django.core.management import call_command
from django.core.management.base import CommandError
from unittest import TestCase
from unittest.mock import patch, MagicMock

class TestCommandTest(TestCase):
    @patch("smartcli.management.commands.test.subprocess.run")
    def test_test_command_success(self, mock_subprocess):
        # Mock successful test execution
        mock_subprocess.return_value.returncode = 0
        mock_subprocess.return_value.stdout = b"Tests passed successfully"
        
        with patch("builtins.print") as mock_print:
            call_command("test")
            # Verify that subprocess.run was called with correct arguments
            mock_subprocess.assert_called_once()
            args, kwargs = mock_subprocess.call_args
            self.assertIn("python", args[0])
            self.assertIn("manage.py", args[0])
            self.assertIn("test", args[0])
            # Verify success message
            mock_print.assert_any_call("Tests completed successfully!")

    @patch("smartcli.management.commands.test.subprocess.run")
    def test_test_command_with_app_argument(self, mock_subprocess):
        # Mock successful test execution for specific app
        mock_subprocess.return_value.returncode = 0
        mock_subprocess.return_value.stdout = b"Tests passed successfully"
        
        with patch("builtins.print") as mock_print:
            call_command("test", "users")
            # Verify that subprocess.run was called with app argument
            mock_subprocess.assert_called_once()
            args, kwargs = mock_subprocess.call_args
            self.assertIn("users", args[0])

    @patch("smartcli.management.commands.test.subprocess.run")
    def test_test_command_with_verbose_option(self, mock_subprocess):
        # Mock successful test execution with verbose output
        mock_subprocess.return_value.returncode = 0
        mock_subprocess.return_value.stdout = b"Detailed test output"
        
        with patch("builtins.print") as mock_print:
            call_command("test", verbosity=2)
            # Verify that subprocess.run was called with verbose flag
            mock_subprocess.assert_called_once()
            args, kwargs = mock_subprocess.call_args
            self.assertIn("--verbosity=2", args[0])

    @patch("smartcli.management.commands.test.subprocess.run")
    def test_test_command_failure(self, mock_subprocess):
        # Mock failed test execution
        mock_subprocess.return_value.returncode = 1
        mock_subprocess.return_value.stderr = b"Test failures occurred"
        
        with self.assertRaises(CommandError) as cm:
            call_command("test")
        self.assertIn("Tests failed", str(cm.exception))

    @patch("smartcli.management.commands.test.subprocess.run")
    def test_test_command_with_coverage_option(self, mock_subprocess):
        # Mock successful test execution with coverage
        mock_subprocess.return_value.returncode = 0
        mock_subprocess.return_value.stdout = b"Coverage report generated"
        
        with patch("builtins.print") as mock_print:
            call_command("test", coverage=True)
            # Verify that subprocess.run was called with coverage arguments
            mock_subprocess.assert_called_once()
            args, kwargs = mock_subprocess.call_args
            self.assertIn("coverage", args[0])
            self.assertIn("run", args[0])

    @patch("smartcli.management.commands.test.subprocess.run")
    def test_test_command_with_parallel_option(self, mock_subprocess):
        # Mock successful parallel test execution
        mock_subprocess.return_value.returncode = 0
        mock_subprocess.return_value.stdout = b"Parallel tests completed"
        
        with patch("builtins.print") as mock_print:
            call_command("test", parallel=True)
            # Verify that subprocess.run was called with parallel flag
            mock_subprocess.assert_called_once()
            args, kwargs = mock_subprocess.call_args
            self.assertIn("--parallel", args[0])

    @patch("smartcli.management.commands.test.subprocess.run")
    def test_test_command_with_keepdb_option(self, mock_subprocess):
        # Mock successful test execution with keepdb
        mock_subprocess.return_value.returncode = 0
        mock_subprocess.return_value.stdout = b"Tests with preserved database"
        
        with patch("builtins.print") as mock_print:
            call_command("test", keepdb=True)
            # Verify that subprocess.run was called with keepdb flag
            mock_subprocess.assert_called_once()
            args, kwargs = mock_subprocess.call_args
            self.assertIn("--keepdb", args[0]) 