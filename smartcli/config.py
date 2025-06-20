"""
Configuration constants for Django SmartCLI.

This module contains configuration constants used across different commands.
"""

# Directory structure constants
DIRECTORIES = [
    "factories", 
    "migrations",
    "models",
    "serializers",
    "services",
    "views",
    "tests",
]

# Test subdirectories
TEST_SUBDIRECTORIES = [
    "models",
    "serializers",
    "services",
    "views",
]

# File suffixes for different types
FILE_SUFFIXES = {
    "model": "",
    "serializer": "_serializer",
    "service": "_service", 
    "factory": "_factory",
    "view": "_view",
}

# Import suffixes for different types
IMPORT_SUFFIXES = {
    "model": "",
    "serializer": "Serializer",
    "service": "Service",
    "factory": "Factory", 
    "view": "View",
}

# Test class suffixes
TEST_SUFFIXES = {
    "model": ["ModelTest", "ManagerTest"],
    "serializer": ["SerializerTest"],
    "service": ["ServiceTest"],
    "factory": ["FactoryTest"],
    "view": ["ViewTest"],
}

# Template configurations
TEMPLATE_CONFIGS = {
    "model": {
        "base_fields": ["id", "created_at", "deleted_at"],
        "read_only_fields": ["id", "created_at"],
        "manager_methods": ["get_active", "get_by_id"],
    },
    "serializer": {
        "base_fields": ["id", "created_at", "deleted_at"],
        "read_only_fields": ["id", "created_at"],
    },
    "service": {
        "base_methods": ["create"],
        "decorators": ["@classmethod", "@transaction.atomic"],
    },
    "factory": {
        "base_fields": ["created_at", "deleted_at"],
    },
}

# Validation patterns
VALIDATION_PATTERNS = {
    "pascal_case": r"^[A-Z][a-zA-Z0-9_]*$",
    "snake_case": r"^[a-z][a-z0-9_]*$",
    "app_name": r"^[a-z][a-z0-9_]*$",
}

# Error messages
ERROR_MESSAGES = {
    "invalid_pascal_case": "{name_type} name '{name}' must start with an uppercase letter (PascalCase)",
    "invalid_characters": "{name_type} name '{name}' can only contain letters, numbers, and underscores",
    "app_not_found": "App '{app_name}' does not exist at {app_path}",
    "directory_not_found": "{directory} directory does not exist in app '{app_name}'",
    "file_exists": "{file_type} file '{filename}' already exists in {directory}",
    "model_not_found": "Model '{model_name}' not found in app '{app_name}'",
}

# Success messages
SUCCESS_MESSAGES = {
    "model_created": "Successfully created model '{name}' in app '{app_name}'!",
    "serializer_created": "Successfully created serializer '{name}Serializer' in app '{app_name}'!",
    "service_created": "Successfully created service '{name}Service' in app '{app_name}'!",
    "factory_created": "Successfully created factory '{name}Factory' in app '{app_name}'!",
    "view_created": "Successfully created view '{name}ViewSet' in app '{app_name}'!",
    "module_created": "Successfully created module '{name}' with complete structure!",
}

# Warning messages
WARNING_MESSAGES = {
    "model_not_found": "Model '{model_name}' not found in app '{app_name}'. Make sure to create the model first with: python manage.py create_model {model_name} {app_name}",
    "settings_not_found": "Settings file not found: {settings_file}",
    "my_apps_not_found": "Could not find MY_APPS in settings file",
    "app_already_in_my_apps": "App {app_entry} is already in MY_APPS",
}

# File templates
FILE_TEMPLATES = {
    "apps_py": """from django.apps import AppConfig


class {app_name}Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = '{app_import_path}'
""",
    
    "urls_py": """from django.urls import include, path
from rest_framework.routers import DefaultRouter

app_name = "{app_name_lower}"

router = DefaultRouter()

urlpatterns = [
    path("", include(router.urls)),
]
""",
    
    "init_py": "",
}

# Migration reminder messages
MIGRATION_MESSAGES = {
    "model": "Don't forget to create and run migrations: python manage.py makemigrations {app_name}",
    "serializer": "Don't forget to update your views to use the new serializer",
    "service": "Don't forget to implement the business logic in your service methods",
    "factory": "Don't forget to add custom fields to your factory if needed",
} 