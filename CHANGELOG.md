# Changelog

All notable changes to Django SmartCLI will be documented in this file.

## [0.2.0] - 2025-06-23

### 🚀 Added

- **New CLI Interface**: Direct command-line interface with `django-smartcli` command
  - Modern kebab-case commands (e.g., `create-module` instead of `create_module`)
  - Smart naming conventions (automatic suffix addition)
  - Built-in help and version commands
- **New `create-views` Command**: Generate DRF ViewSets with full CRUD operations
  - Automatic model detection
  - Complete CRUD endpoints generation
  - Proper URL routing setup
- **Enhanced Test Command**: Organized test execution with category filters
  - `--models`: Run only model tests
  - `--services`: Run only service tests
  - `--serializers`: Run only serializer tests
  - `--views`: Run only view tests
- **Comprehensive Test Suite**: Full test coverage for all components
  - Unit tests for all utility functions
  - Template class tests
  - CLI interface tests
  - Management command tests
- **CI/CD Pipeline**: GitHub Actions workflow for automated testing
  - Runs on Python 3.11
  - Triggered on push and pull requests
  - Ready for multi-version testing
- **Django 5.2 Compatibility**: Full support for the latest Django LTS version
  - Tested and verified with Django 5.2.x
  - Compatible with Django 4.2+ through 5.2.x
  - Future-ready for Django 5.3 when released

### 🔧 Improved

- **Better Error Handling**: More descriptive error messages and validation
- **Enhanced Documentation**: Updated README with CLI examples and best practices
- **Code Quality**: Improved code structure and maintainability
- **Django Version Support**: Extended compatibility range to include latest Django versions

### 🐛 Fixed

- Various minor bugs and edge cases in command execution
- Template generation improvements

## [0.1.1] - 2025-06-21

### 🚀 Added

- Initial release with core commands
- `create_module`, `create_model`, `create_serializer`, `create_service`, `create_factory`
- Standardized microservice architecture templates

### 🔧 Features

- UUID primary keys for models
- Automatic timestamps and soft delete support
- Custom model managers
- Factory Boy integration for testing
- Django REST Framework serializer templates
