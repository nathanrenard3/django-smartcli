"""
Utility functions for Django SmartCLI commands.

This module contains common utility functions used across different commands.
"""

import os
import re
from typing import Optional

from django.conf import settings


def validate_pascal_case_name(name: str, name_type: str) -> None:
    """
    Validate that a name follows PascalCase conventions.

    Args:
        name: The name to validate
        name_type: The type of name (e.g., "Model", "Serializer", "Service")

    Raises:
        ValueError: If the name is invalid
    """
    if not name[0].isupper():
        raise ValueError(
            f"{name_type} name '{name}' must start with an uppercase letter (PascalCase)"
        )

    if not name.replace("_", "").isalnum():
        raise ValueError(
            f"{name_type} name '{name}' can only contain letters, numbers, and underscores"
        )


def validate_app_exists(app_name: str) -> None:
    """Validate that the app exists."""
    app_path = get_app_path(app_name)
    if not os.path.exists(app_path):
        raise ValueError(f"App '{app_name}' does not exist at {app_path}")


def validate_directory_exists(app_name: str, directory: str) -> None:
    """Validate that a directory exists in the app."""
    app_path = get_app_path(app_name)
    dir_path = os.path.join(app_path, directory)
    if not os.path.exists(dir_path):
        raise ValueError(
            f"{directory.capitalize()} directory does not exist in app '{app_name}'"
        )


def get_apps_directory() -> str:
    """
    Get the apps directory based on user settings.
    
    Returns:
        str: Path to the apps directory (either 'apps' or project root)
    """
    # Check if user has disabled centralized apps
    use_centralized = getattr(settings, 'USE_CENTRALIZED_APPS', True)
    
    if use_centralized:
        return "apps"
    else:
        # Return project root directory
        return ""


def get_app_path(app_name: str) -> str:
    """
    Get the full path to an app directory.
    
    Args:
        app_name: Name of the app
        
    Returns:
        str: Full path to the app directory
    """
    apps_dir = get_apps_directory()
    base_dir = settings.BASE_DIR
    
    if apps_dir:
        # Centralized structure: apps/app_name/
        return os.path.join(base_dir, apps_dir, app_name)
    else:
        # Decentralized structure: app_name/ (at project root)
        return os.path.join(base_dir, app_name)


def get_app_import_path(app_name: str) -> str:
    """
    Get the import path for an app based on user settings.
    
    Args:
        app_name: Name of the app
        
    Returns:
        str: Import path for the app (e.g., 'apps.users' or 'users')
    """
    apps_dir = get_apps_directory()
    
    if apps_dir:
        # Centralized structure: apps.users
        return f"{apps_dir}.{app_name}"
    else:
        # Decentralized structure: users
        return app_name


def pascal_to_snake_case(name: str) -> str:
    """Convert PascalCase to snake_case."""
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()


def snake_to_pascal_case(name: str) -> str:
    """Convert snake_case to PascalCase."""
    return "".join(word.capitalize() for word in name.split("_"))


def extract_model_name_from_name(name: str, suffix: str) -> str:
    """
    Extract model name from a name with suffix (e.g., "UserSerializer" -> "User").

    Args:
        name: The name with suffix
        suffix: The suffix to remove

    Returns:
        str: The name without suffix
    """
    if name.endswith(suffix):
        return name[:-len(suffix)]
    return name


def check_file_exists(file_path: str) -> bool:
    """
    Check if a file exists.

    Args:
        file_path: Path to the file

    Returns:
        bool: True if file exists, False otherwise
    """
    return os.path.exists(file_path)


def ensure_directory_exists(directory_path: str) -> None:
    """
    Ensure a directory exists, create it if it doesn't.

    Args:
        directory_path: Path to the directory
    """
    os.makedirs(directory_path, exist_ok=True)


def read_file_content(file_path: str) -> str:
    """
    Read content from a file.

    Args:
        file_path: Path to the file

    Returns:
        str: File content
    """
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    return ""


def write_file_content(file_path: str, content: str) -> None:
    """
    Write content to a file.

    Args:
        file_path: Path to the file
        content: Content to write
    """
    ensure_directory_exists(os.path.dirname(file_path))
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)


def find_import_section_end(content: str) -> int:
    """
    Find the end of the import section in a Python file.

    Args:
        content: File content

    Returns:
        int: Index where imports end
    """
    lines = content.split("\n")
    import_section_end = 0

    for i, line in enumerate(lines):
        if line.strip().startswith("from ") or line.strip().startswith("import "):
            import_section_end = i + 1
        elif line.strip() and not line.strip().startswith("#"):
            break

    return import_section_end


def add_import_to_content(content: str, import_line: str) -> str:
    """
    Add an import line to file content.

    Args:
        content: Original file content
        import_line: Import line to add

    Returns:
        str: Updated content
    """
    if import_line in content:
        return content

    lines = content.split("\n")
    import_section_end = find_import_section_end(content)
    lines.insert(import_section_end, import_line)
    return "\n".join(lines)


def update_all_list(content: str, new_item: str) -> str:
    """
    Update the __all__ list in file content.

    Args:
        content: Original file content
        new_item: New item to add to __all__

    Returns:
        str: Updated content
    """
    if "__all__" not in content:
        if content and not content.endswith("\n"):
            content += "\n"
        content += f'\n__all__ = [\n    "{new_item}"\n]\n'
        return content

    # Update existing __all__
    pattern = r"__all__\s*=\s*\[(.*?)\]"
    match = re.search(pattern, content, re.DOTALL)
    if match:
        all_content = match.group(1)
        all_items = [
            item.strip().strip("\"'")
            for item in all_content.split(",")
            if item.strip()
        ]
        if new_item not in all_items:
            all_items.append(new_item)
            all_items.sort()  # Keep alphabetical order
            new_all_content = ",\n    ".join([f'"{item}"' for item in all_items])
            content = re.sub(
                pattern,
                f"__all__ = [\n    {new_all_content}\n]",
                content,
                flags=re.DOTALL,
            )

    return content


def clean_up_files(file_paths: list) -> None:
    """
    Remove files if they exist.

    Args:
        file_paths: List of file paths to remove
    """
    for file_path in file_paths:
        if os.path.exists(file_path):
            os.remove(file_path)


def detect_django_project_settings() -> tuple[Optional[str], Optional[str]]:
    """
    Detect the Django project directory and settings file.
    
    Returns:
        tuple: (project_dir_name, settings_file_path) or (None, None) if not found
    """
    base_dir = settings.BASE_DIR
    
    # Look for common settings file patterns
    possible_settings_files = [
        # Standard Django project structure (project_name/project_name/settings.py)
        os.path.join(base_dir, os.path.basename(base_dir), "settings.py"),
        # Direct settings.py in base directory
        os.path.join(base_dir, "settings.py"),
        # Project with settings module
        os.path.join(base_dir, "settings", "__init__.py"),
        # Project with settings/base.py (common pattern)
        os.path.join(base_dir, "settings", "base.py"),
        # Project with core/settings/base.py
        os.path.join(base_dir, "core", "settings", "base.py"),
    ]
    
    # Check if any of these files exist
    for settings_file in possible_settings_files:
        if os.path.exists(settings_file):
            # Extract project directory name from the path
            if settings_file.endswith("settings.py"):
                # Direct settings.py file
                project_dir = os.path.basename(base_dir)
                return project_dir, settings_file
            elif settings_file.endswith("__init__.py"):
                # settings/__init__.py
                project_dir = os.path.basename(base_dir)
                return project_dir, settings_file
            elif settings_file.endswith("base.py"):
                # settings/base.py or core/settings/base.py
                project_dir = os.path.basename(base_dir)
                return project_dir, settings_file
    
    return None, None


def find_installed_apps_in_settings(settings_file_path: str) -> tuple[bool, Optional[str]]:
    """
    Find INSTALLED_APPS in settings file.
    
    Args:
        settings_file_path: Path to the settings file
        
    Returns:
        tuple: (found, content) - whether INSTALLED_APPS was found and the file content
    """
    if not os.path.exists(settings_file_path):
        return False, None
    
    try:
        with open(settings_file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Look for INSTALLED_APPS
        if "INSTALLED_APPS" in content:
            return True, content
        
        return False, content
    except Exception:
        return False, None 