from django.test import TestCase

from smartcli import config


class ErrorMessagesTest(TestCase):
    """Test error messages configuration."""

    def test_error_messages_keys(self):
        """Test that ERROR_MESSAGES contains all expected keys."""
        expected_keys = [
            "invalid_pascal_case",
            "invalid_characters", 
            "app_not_found",
            "directory_not_found",
            "file_exists",
            "model_not_found"
        ]
        
        for key in expected_keys:
            with self.subTest(key=key):
                self.assertIn(key, config.ERROR_MESSAGES)

    def test_error_messages_are_strings(self):
        """Test that all error messages are strings."""
        for message in config.ERROR_MESSAGES.values():
            with self.subTest(message=message):
                self.assertIsInstance(message, str)

    def test_error_messages_not_empty(self):
        """Test that all error messages are not empty."""
        for key, message in config.ERROR_MESSAGES.items():
            with self.subTest(key=key):
                self.assertGreater(len(message.strip()), 0)

    def test_error_messages_contain_placeholders(self):
        """Test that error messages contain expected placeholders."""
        expected_placeholders = {
            "invalid_pascal_case": ["{name_type}", "{name}"],
            "invalid_characters": ["{name_type}", "{name}"],
            "app_not_found": ["{app_name}", "{app_path}"],
            "directory_not_found": ["{directory}", "{app_name}"],
            "file_exists": ["{file_type}", "{filename}", "{directory}"],
            "model_not_found": ["{model_name}", "{app_name}"]
        }
        
        for key, placeholders in expected_placeholders.items():
            with self.subTest(key=key):
                message = config.ERROR_MESSAGES[key]
                for placeholder in placeholders:
                    self.assertIn(placeholder, message)

    def test_error_messages_formatting(self):
        """Test that error messages can be formatted with placeholders."""
        test_cases = [
            ("invalid_pascal_case", {"name_type": "Model", "name": "user"}, 
             "Model name 'user' must start with an uppercase letter (PascalCase)"),
            ("app_not_found", {"app_name": "testapp", "app_path": "/path/to/app"}, 
             "App 'testapp' does not exist at /path/to/app"),
            ("model_not_found", {"model_name": "User", "app_name": "users"}, 
             "Model 'User' not found in app 'users'")
        ]
        
        for key, params, expected in test_cases:
            with self.subTest(key=key):
                message = config.ERROR_MESSAGES[key]
                formatted = message.format(**params)
                self.assertEqual(formatted, expected)


class SuccessMessagesTest(TestCase):
    """Test success messages configuration."""

    def test_success_messages_keys(self):
        """Test that SUCCESS_MESSAGES contains all expected keys."""
        expected_keys = [
            "model_created",
            "serializer_created",
            "service_created", 
            "factory_created",
            "view_created",
            "module_created"
        ]
        
        for key in expected_keys:
            with self.subTest(key=key):
                self.assertIn(key, config.SUCCESS_MESSAGES)

    def test_success_messages_are_strings(self):
        """Test that all success messages are strings."""
        for message in config.SUCCESS_MESSAGES.values():
            with self.subTest(message=message):
                self.assertIsInstance(message, str)

    def test_success_messages_not_empty(self):
        """Test that all success messages are not empty."""
        for key, message in config.SUCCESS_MESSAGES.items():
            with self.subTest(key=key):
                self.assertGreater(len(message.strip()), 0)

    def test_success_messages_contain_placeholders(self):
        """Test that success messages contain expected placeholders."""
        expected_placeholders = {
            "model_created": ["{name}", "{app_name}"],
            "serializer_created": ["{name}", "{app_name}"],
            "service_created": ["{name}", "{app_name}"],
            "factory_created": ["{name}", "{app_name}"],
            "view_created": ["{name}", "{app_name}"],
            "module_created": ["{name}"]
        }
        
        for key, placeholders in expected_placeholders.items():
            with self.subTest(key=key):
                message = config.SUCCESS_MESSAGES[key]
                for placeholder in placeholders:
                    self.assertIn(placeholder, message)

    def test_success_messages_formatting(self):
        """Test that success messages can be formatted with placeholders."""
        test_cases = [
            ("model_created", {"name": "User", "app_name": "users"}, 
             "Successfully created model 'User' in app 'users'!"),
            ("serializer_created", {"name": "User", "app_name": "users"}, 
             "Successfully created serializer 'UserSerializer' in app 'users'!"),
            ("service_created", {"name": "User", "app_name": "users"}, 
             "Successfully created service 'UserService' in app 'users'!"),
            ("module_created", {"name": "users"}, 
             "Successfully created module 'users' with complete structure!")
        ]
        
        for key, params, expected in test_cases:
            with self.subTest(key=key):
                message = config.SUCCESS_MESSAGES[key]
                formatted = message.format(**params)
                self.assertEqual(formatted, expected)

    def test_success_messages_end_with_exclamation(self):
        """Test that success messages end with exclamation mark."""
        for key, message in config.SUCCESS_MESSAGES.items():
            with self.subTest(key=key):
                self.assertTrue(message.strip().endswith("!"))


class WarningMessagesTest(TestCase):
    """Test warning messages configuration."""

    def test_warning_messages_keys(self):
        """Test that WARNING_MESSAGES contains all expected keys."""
        expected_keys = [
            "model_not_found",
            "settings_not_found",
            "my_apps_not_found",
            "app_already_in_my_apps"
        ]
        
        for key in expected_keys:
            with self.subTest(key=key):
                self.assertIn(key, config.WARNING_MESSAGES)

    def test_warning_messages_are_strings(self):
        """Test that all warning messages are strings."""
        for message in config.WARNING_MESSAGES.values():
            with self.subTest(message=message):
                self.assertIsInstance(message, str)

    def test_warning_messages_not_empty(self):
        """Test that all warning messages are not empty."""
        for key, message in config.WARNING_MESSAGES.items():
            with self.subTest(key=key):
                self.assertGreater(len(message.strip()), 0)

    def test_warning_messages_contain_placeholders(self):
        """Test that warning messages contain expected placeholders."""
        expected_placeholders = {
            "model_not_found": ["{model_name}", "{app_name}"],
            "settings_not_found": ["{settings_file}"],
            "my_apps_not_found": [],
            "app_already_in_my_apps": ["{app_entry}"]
        }
        
        for key, placeholders in expected_placeholders.items():
            with self.subTest(key=key):
                message = config.WARNING_MESSAGES[key]
                for placeholder in placeholders:
                    self.assertIn(placeholder, message)

    def test_warning_messages_formatting(self):
        """Test that warning messages can be formatted with placeholders."""
        test_cases = [
            ("model_not_found", {"model_name": "User", "app_name": "users"}, 
             "Model 'User' not found in app 'users'. Make sure to create the model first with: python manage.py create_model User users"),
            ("settings_not_found", {"settings_file": "/path/settings.py"}, 
             "Settings file not found: /path/settings.py"),
            ("app_already_in_my_apps", {"app_entry": "apps.users"}, 
             "App apps.users is already in MY_APPS")
        ]
        
        for key, params, expected in test_cases:
            with self.subTest(key=key):
                message = config.WARNING_MESSAGES[key]
                formatted = message.format(**params)
                self.assertEqual(formatted, expected)

    def test_warning_messages_contain_helpful_commands(self):
        """Test that warning messages contain helpful command suggestions."""
        model_not_found_message = config.WARNING_MESSAGES["model_not_found"]
        self.assertIn("python manage.py create_model", model_not_found_message)


class MigrationMessagesTest(TestCase):
    """Test migration messages configuration."""

    def test_migration_messages_keys(self):
        """Test that MIGRATION_MESSAGES contains all expected keys."""
        expected_keys = ["model", "serializer", "service", "factory"]
        
        for key in expected_keys:
            with self.subTest(key=key):
                self.assertIn(key, config.MIGRATION_MESSAGES)

    def test_migration_messages_are_strings(self):
        """Test that all migration messages are strings."""
        for message in config.MIGRATION_MESSAGES.values():
            with self.subTest(message=message):
                self.assertIsInstance(message, str)

    def test_migration_messages_not_empty(self):
        """Test that all migration messages are not empty."""
        for key, message in config.MIGRATION_MESSAGES.items():
            with self.subTest(key=key):
                self.assertGreater(len(message.strip()), 0)

    def test_migration_messages_contain_placeholders(self):
        """Test that migration messages contain expected placeholders."""
        expected_placeholders = {
            "model": ["{app_name}"],
            "serializer": [],
            "service": [],
            "factory": []
        }
        
        for key, placeholders in expected_placeholders.items():
            with self.subTest(key=key):
                message = config.MIGRATION_MESSAGES[key]
                for placeholder in placeholders:
                    self.assertIn(placeholder, message)

    def test_migration_messages_formatting(self):
        """Test that migration messages can be formatted with placeholders."""
        test_cases = [
            ("model", {"app_name": "users"}, 
             "Don't forget to create and run migrations: python manage.py makemigrations users"),
            ("serializer", {}, 
             "Don't forget to update your views to use the new serializer"),
            ("service", {}, 
             "Don't forget to implement the business logic in your service methods"),
            ("factory", {}, 
             "Don't forget to add custom fields to your factory if needed")
        ]
        
        for key, params, expected in test_cases:
            with self.subTest(key=key):
                message = config.MIGRATION_MESSAGES[key]
                formatted = message.format(**params)
                self.assertEqual(formatted, expected)

    def test_migration_messages_contain_helpful_commands(self):
        """Test that migration messages contain helpful command suggestions."""
        model_message = config.MIGRATION_MESSAGES["model"]
        self.assertIn("python manage.py makemigrations", model_message)

    def test_migration_messages_start_with_reminder(self):
        """Test that migration messages start with 'Don't forget to'."""
        for key, message in config.MIGRATION_MESSAGES.items():
            with self.subTest(key=key):
                self.assertTrue(message.strip().startswith("Don't forget to")) 