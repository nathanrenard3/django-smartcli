import os
from typing import List, Tuple

from django.core.management.base import CommandError, BaseCommand

from smartcli.templates import ModelTemplates
from smartcli.config import FILE_SUFFIXES, IMPORT_SUFFIXES, SUCCESS_MESSAGES, WARNING_MESSAGES
from smartcli.utils import (
    validate_pascal_case_name, validate_app_exists, validate_directory_exists,
    get_app_path, pascal_to_snake_case, check_file_exists,
    write_file_content, add_import_to_content, update_all_list, clean_up_files,
    extract_model_name_from_name
)


class Command(BaseCommand):
    """
    Custom command to create a new Django factory with proper template and imports.

    Usage:
        python manage.py create_factory <factory_name> <app_name>

    This command creates a new factory file in the specified app's factories directory
    with a template that follows the project conventions, and updates the __init__.py
    file to include the new factory in imports and __all__.
    """

    help = "Creates a new Django factory with proper template and imports"

    def add_arguments(self, parser):
        """Add command arguments."""
        parser.add_argument(
            "factory_name", type=str, help="Name of the factory to create (PascalCase)"
        )
        parser.add_argument(
            "app_name", type=str, help="Name of the app where to create the factory"
        )

    def get_required_directory(self) -> str:
        """Return the required directory name for this command."""
        return "factories"

    def get_name_type(self) -> str:
        """Return the type of name for validation messages."""
        return "Factory"

    def get_filename_suffix(self) -> str:
        """Return the suffix for generated filenames."""
        return FILE_SUFFIXES["factory"]

    def get_import_suffix(self) -> str:
        """Return the suffix for import statements."""
        return IMPORT_SUFFIXES["factory"]

    def _get_model_name_from_factory(self, factory_name: str) -> str:
        """
        Extract model name from factory name (remove 'Factory' suffix if present).

        Args:
            factory_name: The factory name

        Returns:
            str: The model name
        """
        return extract_model_name_from_name(factory_name, "Factory")

    def _check_model_exists(self, app_name: str, model_name: str) -> bool:
        """
        Check if the model exists in the app.

        Args:
            app_name: The app name
            model_name: The model name

        Returns:
            bool: True if model exists, False otherwise
        """
        models_path = os.path.join(get_app_path(app_name), "models")
        model_file = os.path.join(models_path, f"{pascal_to_snake_case(model_name)}.py")
        return check_file_exists(model_file)

    def generate_main_template(self, **kwargs) -> str:
        """Generate the main template content."""
        name = kwargs["name"]
        app_name = kwargs["app_name"]
        
        # Get model name from factory name
        model_name = self._get_model_name_from_factory(name)
        
        return ModelTemplates.factory_template(name, model_name, app_name)

    def generate_test_template(self, **kwargs) -> str:
        """Generate the test template content."""
        # Factories don't have separate test files, they're tested with models
        return ""

    def get_additional_files(self, **kwargs) -> List[Tuple[str, str, str]]:
        """Get additional files to create."""
        return []

    def handle(self, *args, **options):
        """Handle the command execution."""
        factory_name = options["factory_name"]
        app_name = options["app_name"]

        # Validate inputs using utils
        validate_pascal_case_name(factory_name, self.get_name_type())
        validate_app_exists(app_name)
        validate_directory_exists(app_name, self.get_required_directory())

        # Get model name from factory name
        model_name = self._get_model_name_from_factory(factory_name)

        # Check if model exists using utils
        if not self._check_model_exists(app_name, model_name):
            self.stdout.write(
                self.style.WARNING(
                    WARNING_MESSAGES["model_not_found"].format(
                        model_name=model_name, 
                        app_name=app_name
                    )
                )
            )

        # Define paths using utils
        app_path = get_app_path(app_name)
        factories_path = os.path.join(app_path, "factories")
        
        # Convert factory name to snake_case for filename using utils
        factory_filename = pascal_to_snake_case(factory_name)
        factory_file = os.path.join(factories_path, f"{factory_filename}{self.get_filename_suffix()}.py")

        # Check if factory file already exists using utils
        if check_file_exists(factory_file):
            filename = os.path.basename(factory_file)
            directory = os.path.dirname(factory_file)
            raise CommandError(f"{self.get_name_type()} file '{filename}' already exists in {directory}")

        # Prepare file paths for cleanup
        file_paths = [factory_file]

        try:
            # Generate factory template
            factory_content = self.generate_main_template(name=factory_name, app_name=app_name)

            # Create factory file using utils
            write_file_content(factory_file, factory_content)

            # Update __init__.py using utils
            self._update_init_file_with_utils(factories_path, factory_name, factory_filename)

            # Success message using config
            self.stdout.write(
                self.style.SUCCESS(
                    SUCCESS_MESSAGES["factory_created"].format(name=factory_name, app_name=app_name)
                )
            )

            if not self._check_model_exists(app_name, model_name):
                self.stdout.write(
                    self.style.WARNING(
                        f"Note: Model '{model_name}' was not found. "
                        f"Make sure the model exists before using this factory."
                    )
                )

        except Exception as e:
            # Clean up on error using utils
            clean_up_files(file_paths)
            raise CommandError(f"Error creating factory: {str(e)}")

    def _update_init_file_with_utils(self, factories_path, factory_name, factory_filename):
        """Update __init__.py file using utils functions."""
        factories_init_file = os.path.join(factories_path, "__init__.py")
        factories_content = self._read_or_create_init_file(factories_init_file)
        factories_content = add_import_to_content(
            factories_content, 
            f"from .{factory_filename}{FILE_SUFFIXES['factory']} import {factory_name}{IMPORT_SUFFIXES['factory']}"
        )
        factories_content = update_all_list(factories_content, f"{factory_name}{IMPORT_SUFFIXES['factory']}")
        write_file_content(factories_init_file, factories_content)
        self.stdout.write(f"Updated imports in: {factories_init_file}")

    def _read_or_create_init_file(self, init_file_path):
        """Read existing __init__.py file or create empty one."""
        if os.path.exists(init_file_path):
            with open(init_file_path, "r", encoding="utf-8") as f:
                return f.read()
        return ""
