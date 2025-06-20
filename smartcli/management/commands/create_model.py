import os
from typing import List, Tuple

from django.core.management.base import CommandError, BaseCommand

from smartcli.templates import ModelTemplates
from smartcli.config import FILE_SUFFIXES, IMPORT_SUFFIXES, SUCCESS_MESSAGES, MIGRATION_MESSAGES
from smartcli.utils import (
    validate_pascal_case_name, validate_app_exists, validate_directory_exists,
    get_app_path, get_app_import_path, pascal_to_snake_case, check_file_exists, ensure_directory_exists,
    write_file_content, add_import_to_content, update_all_list, clean_up_files
)


class Command(BaseCommand):
    """
    Custom command to create a new Django model with proper template and imports.

    Usage:
        python manage.py create_model <model_name> <app_name>

    This command creates a new model file in the specified app's models directory
    with a template that follows the project conventions, and updates the __init__.py
    file to include the new model in imports and __all__. It also creates the
    corresponding factory and test files.
    """

    help = "Creates a new Django model with proper template and imports"

    def add_arguments(self, parser):
        """Add command arguments."""
        parser.add_argument(
            "model_name", type=str, help="Name of the model to create (PascalCase)"
        )
        parser.add_argument(
            "app_name", type=str, help="Name of the app where to create the model"
        )

    def get_required_directory(self) -> str:
        """Return the required directory name for this command."""
        return "models"

    def get_name_type(self) -> str:
        """Return the type of name for validation messages."""
        return "Model"

    def get_filename_suffix(self) -> str:
        """Return the suffix for generated filenames."""
        return FILE_SUFFIXES["model"]

    def get_import_suffix(self) -> str:
        """Return the suffix for import statements."""
        return IMPORT_SUFFIXES["model"]

    def generate_main_template(self, **kwargs) -> str:
        """Generate the main template content."""
        return ModelTemplates.model_template(kwargs["name"])

    def generate_test_template(self, **kwargs) -> str:
        """Generate the test template content."""
        app_import_path = get_app_import_path(kwargs["app_name"])
        return ModelTemplates.model_test_template(kwargs["name"], app_import_path)

    def get_additional_files(self, **kwargs) -> List[Tuple[str, str, str]]:
        """Get additional files to create."""
        name = kwargs["name"]
        app_name = kwargs["app_name"]
        app_import_path = get_app_import_path(app_name)
        
        # Get app path
        app_path = get_app_path(app_name)
        factories_path = os.path.join(app_path, "factories")
        
        # Generate factory file path and content
        factory_filename = pascal_to_snake_case(name)
        factory_file = os.path.join(factories_path, f"{factory_filename}{FILE_SUFFIXES['factory']}.py")
        factory_content = ModelTemplates.factory_template(f"{name}Factory", name, app_import_path)
        
        return [(factory_file, factory_content, "Factory")]

    def handle(self, *args, **options):
        """Handle the command execution."""
        model_name = options["model_name"]
        app_name = options["app_name"]

        # Validate inputs using utils
        validate_pascal_case_name(model_name, self.get_name_type())
        validate_app_exists(app_name)
        validate_directory_exists(app_name, self.get_required_directory())

        # Define paths using utils
        app_path = get_app_path(app_name)
        models_path = os.path.join(app_path, "models")
        factories_path = os.path.join(app_path, "factories")
        tests_path = os.path.join(app_path, "tests", "models")

        # Convert model name to snake_case for filename using utils
        model_filename = pascal_to_snake_case(model_name)
        model_file = os.path.join(models_path, f"{model_filename}{self.get_filename_suffix()}.py")
        factory_file = os.path.join(factories_path, f"{model_filename}{FILE_SUFFIXES['factory']}.py")
        test_file = os.path.join(tests_path, f"test_{model_filename}{self.get_filename_suffix()}.py")

        # Check if files already exist using utils
        if check_file_exists(model_file):
            filename = os.path.basename(model_file)
            directory = os.path.dirname(model_file)
            raise CommandError(f"{self.get_name_type()} file '{filename}' already exists in {directory}")

        # Create directories if they don't exist using utils
        ensure_directory_exists(factories_path)
        ensure_directory_exists(tests_path)

        # Prepare file paths for cleanup
        file_paths = [model_file, factory_file, test_file]

        try:
            # Generate templates
            model_content = self.generate_main_template(name=model_name, app_name=app_name)
            factory_content = ModelTemplates.factory_template(f"{model_name}Factory", model_name, app_name)
            test_content = self.generate_test_template(name=model_name, app_name=app_name)

            # Create files using utils
            write_file_content(model_file, model_content)
            write_file_content(factory_file, factory_content)
            write_file_content(test_file, test_content)

            # Update __init__.py files using utils
            self._update_init_files_with_utils(
                models_path, factories_path, tests_path, 
                model_name, model_filename
            )

            # Success message using config
            self.stdout.write(
                self.style.SUCCESS(
                    SUCCESS_MESSAGES["model_created"].format(name=model_name, app_name=app_name)
                )
            )
            self.stdout.write(f"Created files:")
            self.stdout.write(f"  - Model: {model_file}")
            self.stdout.write(f"  - Factory: {factory_file}")
            self.stdout.write(f"  - Test: {test_file}")
            self.stdout.write(MIGRATION_MESSAGES["model"].format(app_name=app_name))

        except Exception as e:
            # Clean up on error using utils
            clean_up_files(file_paths)
            raise CommandError(f"Error creating model: {str(e)}")

    def _update_init_files_with_utils(self, models_path, factories_path, tests_path, model_name, model_filename):
        """Update __init__.py files using utils functions."""
        # Update models __init__.py
        models_init_file = os.path.join(models_path, "__init__.py")
        models_content = self._read_or_create_init_file(models_init_file)
        models_content = add_import_to_content(models_content, f"from .{model_filename} import {model_name}")
        models_content = update_all_list(models_content, model_name)
        write_file_content(models_init_file, models_content)
        self.stdout.write(f"Updated imports in: {models_init_file}")

        # Update factories __init__.py
        factories_init_file = os.path.join(factories_path, "__init__.py")
        factories_content = self._read_or_create_init_file(factories_init_file)
        factories_content = add_import_to_content(factories_content, f"from .{model_filename}{FILE_SUFFIXES['factory']} import {model_name}{IMPORT_SUFFIXES['factory']}")
        factories_content = update_all_list(factories_content, f"{model_name}{IMPORT_SUFFIXES['factory']}")
        write_file_content(factories_init_file, factories_content)
        self.stdout.write(f"Updated imports in: {factories_init_file}")

        # Update tests __init__.py
        tests_init_file = os.path.join(tests_path, "__init__.py")
        tests_content = self._read_or_create_init_file(tests_init_file)
        tests_content = add_import_to_content(tests_content, f"from .test_{model_filename} import {model_name}ModelTest, {model_name}ManagerTest")
        tests_content = update_all_list(tests_content, f"{model_name}ModelTest")
        tests_content = update_all_list(tests_content, f"{model_name}ManagerTest")
        write_file_content(tests_init_file, tests_content)
        self.stdout.write(f"Updated imports in: {tests_init_file}")

    def _read_or_create_init_file(self, init_file_path):
        """Read existing __init__.py file or create empty one."""
        if os.path.exists(init_file_path):
            with open(init_file_path, "r", encoding="utf-8") as f:
                return f.read()
        return ""
