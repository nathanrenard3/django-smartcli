# Django SmartCLI

A powerful Django command library inspired by modern CLIs like NestJS, AdonisJS, and Laravel.
Django SmartCLI automates the creation of Django microservices with a complete and consistent structure.

## 🚀 Features

### Complete Microservice Creation

- **`create_module`**: Creates a new Django app with complete folder structure
- **`create_model`**: Generates Django models with custom managers and UUID primary keys
- **`create_serializer`**: Creates DRF serializers with proper field configuration
- **`create_service`**: Generates business logic services with transaction support
- **`create_factory`**: Creates factory_boy factories for testing
- **`create_views`**: Generates DRF ViewSets with full CRUD operations

### Standardized Architecture

- Consistent folder structure across all modules
- Automatic `__init__.py` file management
- Organized test structure by category (models, serializers, services, views)
- Automatic integration with Django settings

### Best Practices Included

- UUID primary keys for all models
- Automatic timestamps (created_at, deleted_at)
- Soft delete support
- Custom model managers with useful methods
- Atomic transactions in services
- Comprehensive test templates

### 🚦 Modern CLI-first Workflow

- **Direct CLI Commands**: Use `django-smartcli` for all operations (recommended)
- **Django Compatibility**: You can also use `python manage.py` if you prefer
- **Smart Naming**: The CLI automatically adds suffixes (e.g., `Product` becomes `ProductService`)

## 📦 Installation

```bash
pip install django-smartcli
```

## ⚡ Quick Start

### 1. Add to your Django project

```python
# settings.py
INSTALLED_APPS = [
    # ... other apps
    'smartcli',
]
```

### 2. Create your first microservice (recommended method)

```bash
# Create a new module with complete structure
django-smartcli create-module users

# Create models, serializers, services (smart naming)
django-smartcli create-model UserProfile users
django-smartcli create-serializer UserProfile users  # → UserProfileSerializer
django-smartcli create-service UserProfile users     # → UserProfileService
```

### 3. (Optional) Alternative usage with manage.py

If you prefer, all commands are also available via Django:

```bash
python manage.py create_module users
python manage.py create_model UserProfile users
python manage.py create_serializer UserProfileSerializer users
python manage.py create_service UserProfileService users
```

## 🛠️ Available Commands (CLI recommended)

### `create-module`

Creates a complete Django app structure.

```bash
django-smartcli create-module <module_name>
```

### `create-model`

Creates a Django model with best practices.

```bash
django-smartcli create-model <model_name> <app_name>
```

### `create-serializer`

Creates a DRF serializer. The CLI automatically adds "Serializer" suffix.

```bash
django-smartcli create-serializer <name> <app_name> [--model <model_name>]

# Examples:
django-smartcli create-serializer Product products     # → ProductSerializer
django-smartcli create-serializer UserProfile users    # → UserProfileSerializer
```

### `create-service`

Creates a business logic service. The CLI automatically adds "Service" suffix.

```bash
django-smartcli create-service <name> <app_name>

# Examples:
django-smartcli create-service Product products        # → ProductService
django-smartcli create-service UserProfile users       # → UserProfileService
```

### `create-factory`

Creates a factory_boy factory. The CLI automatically adds "Factory" suffix.

```bash
django-smartcli create-factory <name> <app_name>

# Examples:
django-smartcli create-factory Product products        # → ProductFactory
django-smartcli create-factory UserProfile users       # → UserProfileFactory
```

### `create-views`

Creates a DRF ViewSet. The CLI automatically adds "ViewSet" suffix.

```bash
django-smartcli create-views <name> <app_name> [--model <model_name>]

# Examples:
django-smartcli create-views Product products          # → ProductViewSet
django-smartcli create-views UserProfile users         # → UserProfileViewSet
```

### `test`

Runs Django tests with custom filters for organized test execution:

```bash
# Run all tests
django-smartcli test

# Run tests by category (only one filter at a time)
django-smartcli test --models        # Run only model tests
django-smartcli test --services      # Run only service tests
django-smartcli test --serializers   # Run only serializer tests
django-smartcli test --views         # Run only view tests
```

**Available Test Filters:**

- **`--models`**: Tests in `tests/models/` directories
- **`--services`**: Tests in `tests/services/` directories
- **`--serializers`**: Tests in `tests/serializers/` directories
- **`--views`**: Tests in `tests/views/` directories

> **💡 Note:** You can only use one filter at a time. The command will automatically detect and run tests from the appropriate directories in your Django apps.

---

> **💡 Tip:** All these commands are also available with `python manage.py ...` if you prefer the classic Django syntax.

---

## 🎯 CLI Interface (highlighted)

### Getting Help

```bash
django-smartcli --help
django-smartcli --version
```

### Command Examples

```bash
# Create a complete microservice with smart naming
django-smartcli create-module products
django-smartcli create-model Product products
django-smartcli create-serializer Product products     # → ProductSerializer
django-smartcli create-service Product products        # → ProductService
django-smartcli create-factory Product products        # → ProductFactory
django-smartcli create-views Product products          # → ProductViewSet
django-smartcli test --models
```

### CLI Features

- **Modern Interface**: Uses kebab-case commands (e.g., `create-module` instead of `create_module`)
- **Smart Naming**: Automatically adds appropriate suffixes to class names
- **Error Handling**: Clear error messages and validation
- **Django Project Detection**: Automatically detects if you're in a Django project
- **Help System**: Built-in help and version information
- **Cross-Platform**: Works on Windows, macOS, and Linux

## 🎯 Naming Conventions

### Models

- **Format:** PascalCase (e.g., `UserProfile`)
- **File:** snake_case (e.g., `user_profile.py`)
- **Manager:** `<ModelName>Manager`

### Serializers

- **Format:** PascalCase + "Serializer" (e.g., `UserProfileSerializer`)
- **File:** snake_case + "\_serializer" (e.g., `user_profile_serializer.py`)
- **CLI Input:** Just the base name (e.g., `UserProfile` → `UserProfileSerializer`)

### Services

- **Format:** PascalCase + "Service" (e.g., `UserProfileService`)
- **File:** snake_case + "\_service" (e.g., `user_profile_service.py`)
- **CLI Input:** Just the base name (e.g., `UserProfile` → `UserProfileService`)

### Factories

- **Format:** PascalCase + "Factory" (e.g., `UserProfileFactory`)
- **File:** snake_case + "\_factory" (e.g., `user_profile_factory.py`)
- **CLI Input:** Just the base name (e.g., `UserProfile` → `UserProfileFactory`)

## 🧪 Testing

The library includes comprehensive test templates for all generated components:

```bash
# Run all tests
django-smartcli test
# or
python manage.py test

# Run tests by category (only one filter at a time)
django-smartcli test --models        # Model tests
django-smartcli test --services      # Service tests
django-smartcli test --serializers   # Serializer tests
django-smartcli test --views         # View tests

# Same with manage.py
python manage.py test --models
python manage.py test --services
python manage.py test --serializers
python manage.py test --views
```

## 📋 Requirements

- Python 3.8+
- Django 4.2+ (including Django 5.2.3)
- Django REST Framework 3.14+
- factory_boy 3.3+

## 🔧 Development

### Installation for development

```bash
git clone https://github.com/nathanrenard3/django-smartcli.git
cd django-smartcli
pip install -e ".[dev]"
```

### Running tests

```bash
pytest
```

### Code formatting

```bash
black smartcli/
flake8 smartcli/
```

### Testing the CLI

```bash
django-smartcli --help
django-smartcli --version
cd your-django-project
django-smartcli create-module test-module
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by modern CLIs like NestJS, AdonisJS, and Laravel
- Built with Django and Django REST Framework
- Uses factory_boy for test factories

## 📞 Support

- **Issues:** [GitHub Issues](https://github.com/nathanrenard3/django-smartcli/issues)
- **Documentation:** [GitHub Wiki](https://github.com/nathanrenard3/django-smartcli/wiki)
- **Discussions:** [GitHub Discussions](https://github.com/nathanrenard3/django-smartcli/discussions)
