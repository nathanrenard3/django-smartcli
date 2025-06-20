import os
from typing import List, Tuple

from django.core.management.base import CommandError, BaseCommand

from smartcli.templates import ServiceTemplates
from smartcli.config import FILE_SUFFIXES, IMPORT_SUFFIXES, SUCCESS_MESSAGES
from smartcli.utils import (
    validate_pascal_case_name, validate_app_exists, validate_directory_exists,
    get_app_path, pascal_to_snake_case, check_file_exists, ensure_directory_exists,
    write_file_content, add_import_to_content, update_all_list, clean_up_files
)


class Command(BaseCommand):
    """
    Custom command to create a new Django service with proper template and imports.

    Usage:
        python manage.py create_service <service_name> <app_name>

    This command creates a new service file in the specified app's services directory
    with a template that follows the project conventions, and updates the __init__.py
    file to include the new service in imports and __all__. It also creates the
    corresponding test file.
    """

    help = "Creates a new Django service with proper template and imports"

    def add_arguments(self, parser):
        """Add command arguments."""
        parser.add_argument(
            "service_name", type=str, help="Name of the service to create (PascalCase)"
        )
        parser.add_argument(
            "app_name", type=str, help="Name of the app where to create the service"
        )

    def get_required_directory(self) -> str:
        """Return the required directory name for this command."""
        return "services"

    def get_name_type(self) -> str:
        """Return the type of name for validation messages."""
        return "Service"

    def get_filename_suffix(self) -> str:
        """Return the suffix for generated filenames."""
        return FILE_SUFFIXES["service"]

    def get_import_suffix(self) -> str:
        """Return the suffix for import statements."""
        return IMPORT_SUFFIXES["service"]

    def generate_main_template(self, **kwargs) -> str:
        """Generate the main template content."""
        return ServiceTemplates.service_template(kwargs["name"])

    def generate_test_template(self, **kwargs) -> str:
        """Generate the test template content."""
        return ServiceTemplates.service_test_template(kwargs["name"], kwargs["app_name"])

    def get_additional_files(self, **kwargs) -> List[Tuple[str, str, str]]:
        """Get additional files to create."""
        return []

    def handle(self, *args, **options):
        """Handle the command execution."""
        service_name = options["service_name"]
        app_name = options["app_name"]

        # Validate inputs using utils
        validate_pascal_case_name(service_name, self.get_name_type())
        validate_app_exists(app_name)
        validate_directory_exists(app_name, self.get_required_directory())

        # Define paths using utils
        app_path = get_app_path(app_name)
        services_path = os.path.join(app_path, "services")
        tests_path = os.path.join(app_path, "tests", "services")

        # Convert service name to snake_case for filename using utils
        service_filename = pascal_to_snake_case(service_name)
        service_file = os.path.join(services_path, f"{service_filename}{self.get_filename_suffix()}.py")
        test_file = os.path.join(tests_path, f"test_{service_filename}{self.get_filename_suffix()}.py")

        # Check if service file already exists using utils
        if check_file_exists(service_file):
            filename = os.path.basename(service_file)
            directory = os.path.dirname(service_file)
            raise CommandError(f"{self.get_name_type()} file '{filename}' already exists in {directory}")

        # Create directories if they don't exist using utils
        ensure_directory_exists(tests_path)

        # Prepare file paths for cleanup
        file_paths = [service_file, test_file]

        try:
            # Generate templates
            service_content = self.generate_main_template(name=service_name, app_name=app_name)
            test_content = self.generate_test_template(name=service_name, app_name=app_name)

            # Create files using utils
            write_file_content(service_file, service_content)
            write_file_content(test_file, test_content)

            # Update __init__.py files using utils
            self._update_init_files_with_utils(
                services_path, tests_path, service_name, service_filename
            )

            # Success message using config
            self.stdout.write(
                self.style.SUCCESS(
                    SUCCESS_MESSAGES["service_created"].format(name=service_name, app_name=app_name)
                )
            )
            self.stdout.write(f"Created files:")
            self.stdout.write(f"  - Service: {service_file}")
            self.stdout.write(f"  - Test: {test_file}")

        except Exception as e:
            # Clean up on error using utils
            clean_up_files(file_paths)
            raise CommandError(f"Error creating service: {str(e)}")

    def _update_init_files_with_utils(self, services_path, tests_path, service_name, service_filename):
        """Update __init__.py files using utils functions."""
        # Update services __init__.py
        services_init_file = os.path.join(services_path, "__init__.py")
        services_content = self._read_or_create_init_file(services_init_file)
        services_content = add_import_to_content(
            services_content, 
            f"from .{service_filename}{FILE_SUFFIXES['service']} import {service_name}{IMPORT_SUFFIXES['service']}"
        )
        services_content = update_all_list(services_content, f"{service_name}{IMPORT_SUFFIXES['service']}")
        write_file_content(services_init_file, services_content)
        self.stdout.write(f"Updated imports in: {services_init_file}")

        # Update tests __init__.py
        tests_init_file = os.path.join(tests_path, "__init__.py")
        tests_content = self._read_or_create_init_file(tests_init_file)
        tests_content = add_import_to_content(
            tests_content, 
            f"from .test_{service_filename}{FILE_SUFFIXES['service']} import {service_name}{IMPORT_SUFFIXES['service']}Test"
        )
        tests_content = update_all_list(tests_content, f"{service_name}{IMPORT_SUFFIXES['service']}Test")
        write_file_content(tests_init_file, tests_content)
        self.stdout.write(f"Updated imports in: {tests_init_file}")

    def _read_or_create_init_file(self, init_file_path):
        """Read existing __init__.py file or create empty one."""
        if os.path.exists(init_file_path):
            with open(init_file_path, "r", encoding="utf-8") as f:
                return f.read()
        return ""
