import os
from typing import List, Tuple

from django.core.management.base import CommandError, BaseCommand

from smartcli.templates import ViewTemplates
from smartcli.config import FILE_SUFFIXES, IMPORT_SUFFIXES, SUCCESS_MESSAGES, WARNING_MESSAGES
from smartcli.utils import (
    validate_pascal_case_name, validate_app_exists, validate_directory_exists,
    get_app_path, pascal_to_snake_case, check_file_exists, ensure_directory_exists,
    write_file_content, add_import_to_content, update_all_list, clean_up_files,
    extract_model_name_from_name
)


class Command(BaseCommand):
    """
    Custom command to create a new Django view with proper template and imports.

    Usage:
        python manage.py create_views <view_name> <app_name>

    This command creates a new view file in the specified app's views directory
    with a template that follows the project conventions, and updates the __init__.py
    file to include the new view in imports and __all__. It also creates the
    corresponding test file.
    """

    help = "Creates a new Django view with proper template and imports"

    def add_arguments(self, parser):
        """Add command arguments."""
        parser.add_argument(
            "view_name", type=str, help="Name of the view to create (PascalCase)"
        )
        parser.add_argument(
            "app_name", type=str, help="Name of the app where to create the view"
        )
        parser.add_argument(
            "--model",
            type=str,
            help="Name of the model to attach the view to (defaults to view name without 'View' suffix)",
        )

    def get_required_directory(self) -> str:
        """Return the required directory name for this command."""
        return "views"

    def get_name_type(self) -> str:
        """Return the type of name for validation messages."""
        return "View"

    def get_filename_suffix(self) -> str:
        """Return the suffix for generated filenames."""
        return FILE_SUFFIXES["view"]

    def get_import_suffix(self) -> str:
        """Return the suffix for import statements."""
        return IMPORT_SUFFIXES["view"]

    def _get_model_name_from_view(self, view_name: str) -> str:
        """
        Extract model name from view name (remove 'View' suffix if present).

        Args:
            view_name: The view name

        Returns:
            str: The model name
        """
        return extract_model_name_from_name(view_name, "View")

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

    def _check_serializer_exists(self, app_name: str, model_name: str) -> bool:
        """
        Check if the serializer exists in the app.

        Args:
            app_name: The app name
            model_name: The model name

        Returns:
            bool: True if serializer exists, False otherwise
        """
        serializers_path = os.path.join(get_app_path(app_name), "serializers")
        serializer_file = os.path.join(serializers_path, f"{pascal_to_snake_case(model_name)}_serializer.py")
        return check_file_exists(serializer_file)

    def _check_service_exists(self, app_name: str, model_name: str) -> bool:
        """
        Check if the service exists in the app.

        Args:
            app_name: The app name
            model_name: The model name

        Returns:
            bool: True if service exists, False otherwise
        """
        services_path = os.path.join(get_app_path(app_name), "services")
        service_file = os.path.join(services_path, f"{pascal_to_snake_case(model_name)}_service.py")
        return check_file_exists(service_file)

    def generate_main_template(self, **kwargs) -> str:
        """Generate the main template content."""
        name = kwargs["name"]
        app_name = kwargs["app_name"]
        model_name = kwargs.get("model")
        
        # Get model name - use provided model name or extract from view name
        if model_name is None:
            model_name = self._get_model_name_from_view(name)
        
        return ViewTemplates.view_template(name, model_name, app_name)

    def generate_test_template(self, **kwargs) -> str:
        """Generate the test template content."""
        name = kwargs["name"]
        app_name = kwargs["app_name"]
        model_name = kwargs.get("model")
        
        # Get model name - use provided model name or extract from view name
        if model_name is None:
            model_name = self._get_model_name_from_view(name)
        
        return ViewTemplates.view_test_template(name, model_name, app_name)

    def get_additional_files(self, **kwargs) -> List[Tuple[str, str, str]]:
        """Get additional files to create."""
        return []

    def handle(self, *args, **options):
        """Handle the command execution."""
        view_name = options["view_name"]
        app_name = options["app_name"]
        model_name = options.get("model")

        # Validate inputs using utils
        validate_pascal_case_name(view_name, self.get_name_type())
        validate_app_exists(app_name)
        validate_directory_exists(app_name, self.get_required_directory())

        # Get model name - use provided model name or extract from view name
        if model_name is None:
            model_name = self._get_model_name_from_view(view_name)
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

        # Check if serializer exists
        if not self._check_serializer_exists(app_name, model_name):
            self.stdout.write(
                self.style.WARNING(
                    f"Serializer '{model_name}Serializer' not found in app '{app_name}'. "
                    f"Make sure to create the serializer first with: python manage.py create_serializer {model_name}Serializer {app_name}"
                )
            )

        # Check if service exists
        if not self._check_service_exists(app_name, model_name):
            self.stdout.write(
                self.style.WARNING(
                    f"Service '{model_name}Service' not found in app '{app_name}'. "
                    f"Make sure to create the service first with: python manage.py create_service {model_name}Service {app_name}"
                )
            )

        # Define paths using utils
        app_path = get_app_path(app_name)
        views_path = os.path.join(app_path, "views")
        tests_path = os.path.join(app_path, "tests", "views")

        # Convert view name to snake_case for filename using utils
        view_filename = pascal_to_snake_case(view_name)
        view_file = os.path.join(views_path, f"{view_filename}{self.get_filename_suffix()}.py")
        test_file = os.path.join(tests_path, f"test_{view_filename}{self.get_filename_suffix()}.py")

        # Check if view file already exists using utils
        if check_file_exists(view_file):
            filename = os.path.basename(view_file)
            directory = os.path.dirname(view_file)
            raise CommandError(f"{self.get_name_type()} file '{filename}' already exists in {directory}")

        # Create directories if they don't exist using utils
        ensure_directory_exists(tests_path)

        # Prepare file paths for cleanup
        file_paths = [view_file, test_file]

        try:
            # Generate templates
            view_content = self.generate_main_template(
                name=view_name, app_name=app_name, model=model_name
            )
            test_content = self.generate_test_template(
                name=view_name, app_name=app_name, model=model_name
            )

            # Create files using utils
            write_file_content(view_file, view_content)
            write_file_content(test_file, test_content)

            # Update __init__.py files using utils
            self._update_init_files_with_utils(
                views_path, tests_path, view_name, view_filename
            )

            # Success message using config
            self.stdout.write(
                self.style.SUCCESS(
                    SUCCESS_MESSAGES["view_created"].format(name=view_name, app_name=app_name)
                )
            )
            self.stdout.write(f"Created files:")
            self.stdout.write(f"  - View: {view_file}")
            self.stdout.write(f"  - Test: {test_file}")

            # Show which model the view is attached to
            self.stdout.write(f"View attached to model: '{model_name}'")

            if not self._check_model_exists(app_name, model_name):
                self.stdout.write(
                    self.style.WARNING(
                        f"Note: Model '{model_name}' was not found. "
                        f"Make sure the model exists before using this view."
                    )
                )

            if not self._check_serializer_exists(app_name, model_name):
                self.stdout.write(
                    self.style.WARNING(
                        f"Note: Serializer '{model_name}Serializer' was not found. "
                        f"Make sure the serializer exists before using this view."
                    )
                )

            if not self._check_service_exists(app_name, model_name):
                self.stdout.write(
                    self.style.WARNING(
                        f"Note: Service '{model_name}Service' was not found. "
                        f"Make sure the service exists before using this view."
                    )
                )

        except Exception as e:
            # Clean up on error using utils
            clean_up_files(file_paths)
            raise CommandError(f"Error creating view: {str(e)}")

    def _update_init_files_with_utils(self, views_path, tests_path, view_name, view_filename):
        """Update __init__.py files using utils functions."""
        # Update views __init__.py
        views_init_file = os.path.join(views_path, "__init__.py")
        views_content = self._read_or_create_init_file(views_init_file)
        views_content = add_import_to_content(
            views_content, 
            f"from .{view_filename}{FILE_SUFFIXES['view']} import {view_name}{IMPORT_SUFFIXES['view']}"
        )
        views_content = update_all_list(views_content, f"{view_name}{IMPORT_SUFFIXES['view']}")
        write_file_content(views_init_file, views_content)
        self.stdout.write(f"Updated imports in: {views_init_file}")

        # Update tests __init__.py
        tests_init_file = os.path.join(tests_path, "__init__.py")
        tests_content = self._read_or_create_init_file(tests_init_file)
        tests_content = add_import_to_content(
            tests_content, 
            f"from .test_{view_filename}{FILE_SUFFIXES['view']} import {view_name}{IMPORT_SUFFIXES['view']}Test"
        )
        tests_content = update_all_list(tests_content, f"{view_name}{IMPORT_SUFFIXES['view']}Test")
        write_file_content(tests_init_file, tests_content)
        self.stdout.write(f"Updated imports in: {tests_init_file}")

    def _read_or_create_init_file(self, init_file_path):
        """Read existing __init__.py file or create empty one."""
        if os.path.exists(init_file_path):
            with open(init_file_path, "r", encoding="utf-8") as f:
                return f.read()
        return "" 