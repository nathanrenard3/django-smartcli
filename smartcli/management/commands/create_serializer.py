import os
from typing import List, Tuple

from django.core.management.base import CommandError, BaseCommand

from smartcli.templates import SerializerTemplates
from smartcli.config import FILE_SUFFIXES, IMPORT_SUFFIXES, SUCCESS_MESSAGES, WARNING_MESSAGES
from smartcli.utils import (
    validate_pascal_case_name, validate_app_exists, validate_directory_exists,
    get_app_path, pascal_to_snake_case, check_file_exists, ensure_directory_exists,
    write_file_content, add_import_to_content, update_all_list, clean_up_files,
    extract_model_name_from_name
)


class Command(BaseCommand):
    """
    Custom command to create a new Django serializer with proper template and imports.

    Usage:
        python manage.py create_serializer <serializer_name> <app_name>

    This command creates a new serializer file in the specified app's serializers directory
    with a template that follows the project conventions, and updates the __init__.py
    file to include the new serializer in imports and __all__. It also creates the
    corresponding test file.
    """

    help = "Creates a new Django serializer with proper template and imports"

    def add_arguments(self, parser):
        """Add command arguments."""
        parser.add_argument(
            "serializer_name",
            type=str,
            help="Name of the serializer to create (PascalCase)",
        )
        parser.add_argument(
            "app_name", type=str, help="Name of the app where to create the serializer"
        )
        parser.add_argument(
            "--model",
            type=str,
            help="Name of the model to attach the serializer to (defaults to serializer name without 'Serializer' suffix)",
        )

    def get_required_directory(self) -> str:
        """Return the required directory name for this command."""
        return "serializers"

    def get_name_type(self) -> str:
        """Return the type of name for validation messages."""
        return "Serializer"

    def get_filename_suffix(self) -> str:
        """Return the suffix for generated filenames."""
        return FILE_SUFFIXES["serializer"]

    def get_import_suffix(self) -> str:
        """Return the suffix for import statements."""
        return IMPORT_SUFFIXES["serializer"]

    def _get_model_name_from_serializer(self, serializer_name: str) -> str:
        """
        Extract model name from serializer name (remove 'Serializer' suffix if present).

        Args:
            serializer_name: The serializer name

        Returns:
            str: The model name
        """
        return extract_model_name_from_name(serializer_name, "Serializer")

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
        model_name = kwargs.get("model")
        
        # Get model name - use provided model name or extract from serializer name
        if model_name is None:
            model_name = self._get_model_name_from_serializer(name)
        
        return SerializerTemplates.serializer_template(name, model_name, app_name)

    def generate_test_template(self, **kwargs) -> str:
        """Generate the test template content."""
        name = kwargs["name"]
        app_name = kwargs["app_name"]
        model_name = kwargs.get("model")
        
        # Get model name - use provided model name or extract from serializer name
        if model_name is None:
            model_name = self._get_model_name_from_serializer(name)
        
        return SerializerTemplates.serializer_test_template(name, model_name, app_name)

    def get_additional_files(self, **kwargs) -> List[Tuple[str, str, str]]:
        """Get additional files to create."""
        return []

    def handle(self, *args, **options):
        """Handle the command execution."""
        serializer_name = options["serializer_name"]
        app_name = options["app_name"]
        model_name = options.get("model")

        # Validate inputs using utils
        validate_pascal_case_name(serializer_name, self.get_name_type())
        validate_app_exists(app_name)
        validate_directory_exists(app_name, self.get_required_directory())

        # Get model name - use provided model name or extract from serializer name
        if model_name is None:
            model_name = self._get_model_name_from_serializer(serializer_name)
        else:
            # Validate that the provided model name follows conventions
            validate_pascal_case_name(model_name, "Model")

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
        serializers_path = os.path.join(app_path, "serializers")
        tests_path = os.path.join(app_path, "tests", "serializers")

        # Convert serializer name to snake_case for filename using utils
        serializer_filename = pascal_to_snake_case(serializer_name)
        serializer_file = os.path.join(
            serializers_path, f"{serializer_filename}{self.get_filename_suffix()}.py"
        )
        test_file = os.path.join(
            tests_path, f"test_{serializer_filename}{self.get_filename_suffix()}.py"
        )

        # Check if serializer file already exists using utils
        if check_file_exists(serializer_file):
            filename = os.path.basename(serializer_file)
            directory = os.path.dirname(serializer_file)
            raise CommandError(f"{self.get_name_type()} file '{filename}' already exists in {directory}")

        # Create directories if they don't exist using utils
        ensure_directory_exists(tests_path)

        # Prepare file paths for cleanup
        file_paths = [serializer_file, test_file]

        try:
            # Generate templates
            serializer_content = self.generate_main_template(
                name=serializer_name, app_name=app_name, model=model_name
            )
            test_content = self.generate_test_template(
                name=serializer_name, app_name=app_name, model=model_name
            )

            # Create files using utils
            write_file_content(serializer_file, serializer_content)
            write_file_content(test_file, test_content)

            # Update __init__.py files using utils
            self._update_init_files_with_utils(
                serializers_path, tests_path, serializer_name, serializer_filename
            )

            # Success message using config
            self.stdout.write(
                self.style.SUCCESS(
                    SUCCESS_MESSAGES["serializer_created"].format(name=serializer_name, app_name=app_name)
                )
            )
            self.stdout.write(f"Created files:")
            self.stdout.write(f"  - Serializer: {serializer_file}")
            self.stdout.write(f"  - Test: {test_file}")

            # Show which model the serializer is attached to
            self.stdout.write(f"Serializer attached to model: '{model_name}'")

            if not self._check_model_exists(app_name, model_name):
                self.stdout.write(
                    self.style.WARNING(
                        f"Note: Model '{model_name}' was not found. "
                        f"Make sure the model exists before using this serializer."
                    )
                )

        except Exception as e:
            # Clean up on error using utils
            clean_up_files(file_paths)
            raise CommandError(f"Error creating serializer: {str(e)}")

    def _update_init_files_with_utils(self, serializers_path, tests_path, serializer_name, serializer_filename):
        """Update __init__.py files using utils functions."""
        # Update serializers __init__.py
        serializers_init_file = os.path.join(serializers_path, "__init__.py")
        serializers_content = self._read_or_create_init_file(serializers_init_file)
        serializers_content = add_import_to_content(
            serializers_content, 
            f"from .{serializer_filename}{FILE_SUFFIXES['serializer']} import {serializer_name}{IMPORT_SUFFIXES['serializer']}"
        )
        serializers_content = update_all_list(serializers_content, f"{serializer_name}{IMPORT_SUFFIXES['serializer']}")
        write_file_content(serializers_init_file, serializers_content)
        self.stdout.write(f"Updated imports in: {serializers_init_file}")

        # Update tests __init__.py
        tests_init_file = os.path.join(tests_path, "__init__.py")
        tests_content = self._read_or_create_init_file(tests_init_file)
        tests_content = add_import_to_content(
            tests_content, 
            f"from .test_{serializer_filename}{FILE_SUFFIXES['serializer']} import {serializer_name}{IMPORT_SUFFIXES['serializer']}Test"
        )
        tests_content = update_all_list(tests_content, f"{serializer_name}{IMPORT_SUFFIXES['serializer']}Test")
        write_file_content(tests_init_file, tests_content)
        self.stdout.write(f"Updated imports in: {tests_init_file}")

    def _read_or_create_init_file(self, init_file_path):
        """Read existing __init__.py file or create empty one."""
        if os.path.exists(init_file_path):
            with open(init_file_path, "r", encoding="utf-8") as f:
                return f.read()
        return ""
