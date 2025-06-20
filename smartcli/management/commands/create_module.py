import os
import re

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from smartcli.config import DIRECTORIES, TEST_SUBDIRECTORIES, FILE_TEMPLATES, SUCCESS_MESSAGES
from smartcli.utils import (
    check_file_exists, ensure_directory_exists,
    write_file_content, detect_django_project_settings, find_installed_apps_in_settings,
    get_apps_directory, get_app_path, get_app_import_path
)


class Command(BaseCommand):
    """
    Custom command to create a new Django app with a complete structure.

    Usage:
        python manage.py create_module <module_name>

    This command creates a new app with the following structure:
    - docs/
    - factories/
    - migrations/
    - models/
    - serializers/
    - services/
    - tests/ (with subdirectories: models/, serializers/, services/, views/)
    - views/
    - apps.py
    - urls.py
    - __init__.py

    The location depends on USE_CENTRALIZED_APPS setting:
    - If True (default): apps/module_name/
    - If False: module_name/ (at project root)
    """

    help = "Creates a new Django app with complete structure"

    def add_arguments(self, parser):
        """Add command arguments."""
        parser.add_argument(
            "module_name", type=str, help="Name of the module to create"
        )

    def _add_app_to_settings(self, module_name: str) -> None:
        """
        Add the new app to INSTALLED_APPS in settings file.

        Args:
            module_name: Name of the module to add
        """
        # Detect Django project and settings file
        project_dir, settings_file = detect_django_project_settings()
        
        if not settings_file:
            app_import_path = get_app_import_path(module_name)
            self.stdout.write(
                self.style.WARNING(
                    "Could not detect Django settings file. "
                    f"Please manually add '{app_import_path}' to INSTALLED_APPS."
                )
            )
            return

        # Check if INSTALLED_APPS exists in settings
        has_installed_apps, content = find_installed_apps_in_settings(settings_file)
        
        if not has_installed_apps:
            app_import_path = get_app_import_path(module_name)
            self.stdout.write(
                self.style.WARNING(
                    f"INSTALLED_APPS not found in {settings_file}. "
                    f"Please manually add '{app_import_path}' to INSTALLED_APPS."
                )
            )
            return

        try:
            # Get the correct import path for the app
            app_import_path = get_app_import_path(module_name)
            app_entry = f'"{app_import_path}"'
            
            # Check if app is already in INSTALLED_APPS
            if app_entry in content:
                self.stdout.write(
                    self.style.WARNING(
                        f"App {app_entry} is already in INSTALLED_APPS"
                    )
                )
                return

            # Find INSTALLED_APPS list and add the new app
            # Pattern to match INSTALLED_APPS = [ ... ]
            pattern = r"(INSTALLED_APPS\s*=\s*\[)([^\]]*)(\])"
            match = re.search(pattern, content, re.MULTILINE | re.DOTALL)

            if match:
                prefix = match.group(1)
                apps_list = match.group(2)
                suffix = match.group(3)

                # Parse existing apps properly
                lines = apps_list.split("\n")
                existing_apps = []

                for line in lines:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        # Remove trailing comma if present
                        if line.endswith(","):
                            line = line[:-1]
                        # Remove quotes and clean up
                        line = line.strip("\"'")
                        existing_apps.append(line)

                # Add the new app
                existing_apps.append(app_import_path)

                # Sort alphabetically
                existing_apps.sort()

                # Reconstruct the INSTALLED_APPS list with proper formatting
                formatted_apps = []
                for app in existing_apps:
                    formatted_apps.append(f'    "{app}",')

                # Remove trailing comma from last item
                if formatted_apps:
                    formatted_apps[-1] = formatted_apps[-1].rstrip(",")

                # Reconstruct the content
                new_apps_list = "\n".join(formatted_apps)
                new_content = (
                    content[: match.start()]
                    + prefix
                    + "\n"
                    + new_apps_list
                    + "\n"
                    + suffix
                    + content[match.end() :]
                )

                # Write back to file using utils
                write_file_content(settings_file, new_content)

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Added '{app_import_path}' to INSTALLED_APPS in {settings_file}"
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"Could not find INSTALLED_APPS list in {settings_file}. "
                        f"Please manually add '{app_import_path}' to INSTALLED_APPS."
                    )
                )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"Error updating settings file: {str(e)}")
            )

    def handle(self, *args, **options):
        """Handle the command execution."""
        module_name = options["module_name"]

        # Validate module name
        if not module_name.isidentifier():
            raise CommandError(
                f"'{module_name}' is not a valid Python identifier. "
                "Module names must contain only letters, digits, and underscores, "
                "and cannot start with a digit."
            )

        # Get the app path based on user settings
        module_path = get_app_path(module_name)
        apps_dir = get_apps_directory()

        # Check if module already exists using utils
        if check_file_exists(module_path):
            raise CommandError(
                f"Module '{module_name}' already exists at {module_path}"
            )

        try:
            # Create the main module directory using utils
            ensure_directory_exists(module_path)
            self.stdout.write(f"Created directory: {module_path}")

            # Create all subdirectories using config
            for directory in DIRECTORIES:
                dir_path = os.path.join(module_path, directory)
                ensure_directory_exists(dir_path)
                self.stdout.write(f"Created directory: {dir_path}")

                # Create __init__.py in each directory using utils
                init_file = os.path.join(dir_path, "__init__.py")
                write_file_content(init_file, "")
                self.stdout.write(f"Created file: {init_file}")

                # Create test subdirectories if this is the tests directory
                if directory == "tests":
                    for subdir in TEST_SUBDIRECTORIES:
                        subdir_path = os.path.join(dir_path, subdir)
                        ensure_directory_exists(subdir_path)
                        self.stdout.write(f"Created directory: {subdir_path}")

                        # Create __init__.py in test subdirectories using utils
                        subdir_init_file = os.path.join(subdir_path, "__init__.py")
                        write_file_content(subdir_init_file, "")
                        self.stdout.write(f"Created file: {subdir_init_file}")

            # Create __init__.py in the main module directory using utils
            main_init_file = os.path.join(module_path, "__init__.py")
            write_file_content(main_init_file, "")
            self.stdout.write(f"Created file: {main_init_file}")

            # Get the correct import path for templates
            app_import_path = get_app_import_path(module_name)

            # Create apps.py using config template
            apps_content = FILE_TEMPLATES["apps_py"].format(
                app_name=module_name.capitalize(),
                app_name_lower=module_name,
                app_import_path=app_import_path
            )
            apps_file = os.path.join(module_path, "apps.py")
            write_file_content(apps_file, apps_content)
            self.stdout.write(f"Created file: {apps_file}")

            # Create urls.py using config template
            urls_content = FILE_TEMPLATES["urls_py"].format(
                app_name=module_name.capitalize(),
                app_name_lower=module_name
            )
            urls_file = os.path.join(module_path, "urls.py")
            write_file_content(urls_file, urls_content)
            self.stdout.write(f"Created file: {urls_file}")

            # Add app to settings
            self._add_app_to_settings(module_name)

            # Success message using config
            self.stdout.write(
                self.style.SUCCESS(
                    SUCCESS_MESSAGES["module_created"].format(name=module_name)
                )
            )
            
            # Show structure info
            if apps_dir:
                self.stdout.write(
                    f"Module '{module_name}' created in centralized structure (apps/{module_name}/)"
                )
            else:
                self.stdout.write(
                    f"Module '{module_name}' created in decentralized structure ({module_name}/)"
                )
            
            self.stdout.write(
                f"Module has been automatically added to INSTALLED_APPS."
            )

        except Exception as e:
            # Clean up on error
            if check_file_exists(module_path):
                import shutil
                shutil.rmtree(module_path)
            raise CommandError(f"Error creating module: {str(e)}")
