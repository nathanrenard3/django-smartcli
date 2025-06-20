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

### 🎯 Dual Interface

- **Django Management Commands**: Traditional `python manage.py` interface
- **Direct CLI Commands**: Modern `django-smartcli` interface for faster workflow

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

### 2. Create your first microservice

#### Option A: Using Django Management Commands (Traditional)

```bash
# Create a new module with complete structure
python manage.py create_module users

# Create models, serializers, services
python manage.py create_model UserProfile users
python manage.py create_serializer UserProfileSerializer users
python manage.py create_service UserProfileService users
```

#### Option B: Using Direct CLI Commands (Modern)

```bash
# Create a new module with complete structure
django-smartcli create-module users

# Create models, serializers, services
django-smartcli create-model UserProfile users
django-smartcli create-serializer UserProfileSerializer users
django-smartcli create-service UserProfileService users
```

## 🛠️ Available Commands

### `create_module` / `create-module`

Creates a complete Django app structure.

```bash
# Django management command
python manage.py create_module <module_name>

# Direct CLI command
django-smartcli create-module <module_name>
```

**Features:**

- Creates all necessary directories
- Generates `apps.py` and `urls.py`
- Automatically adds to `INSTALLED_APPS`
- Creates `__init__.py` files in all directories

### `create_model` / `create-model`

Creates a Django model with best practices.

```bash
# Django management command
python manage.py create_model <model_name> <app_name>

# Direct CLI command
django-smartcli create-model <model_name> <app_name>
```

**Generated Features:**

- UUID primary key
- Automatic timestamps (`created_at`, `deleted_at`)
- Custom manager with `get_active()` and `get_by_id()` methods
- Soft delete support
- Automatic factory creation
- Model tests

### `create_serializer` / `create-serializer`

Creates a DRF serializer.

```bash
# Django management command
python manage.py create_serializer <serializer_name> <app_name> [--model <model_name>]

# Direct CLI command
django-smartcli create-serializer <serializer_name> <app_name> [--model <model_name>]
```

**Features:**

- ModelSerializer with proper field configuration
- Automatic model detection
- Read-only fields for timestamps
- Serializer tests

### `create_service` / `create-service`

Creates a business logic service.

```bash
# Django management command
python manage.py create_service <service_name> <app_name>

# Direct CLI command
django-smartcli create-service <service_name> <app_name>
```

**Features:**

- Class with static methods
- Atomic transaction support
- CRUD operation templates
- Service tests

### `create_factory` / `create-factory`

Creates a factory_boy factory.

```bash
# Django management command
python manage.py create_factory <factory_name> <app_name>

# Direct CLI command
django-smartcli create-factory <factory_name> <app_name>
```

**Features:**

- DjangoModelFactory
- Automatic timestamp handling
- Model association

### `create_views` / `create-views`

Creates a DRF ViewSet.

```bash
# Django management command
python manage.py create_views <view_name> <app_name> [--model <model_name>]

# Direct CLI command
django-smartcli create-views <view_name> <app_name> [--model <model_name>]
```

**Features:**

- Complete CRUD operations
- Permission classes
- Model, serializer, and service integration
- View tests

## 🎯 CLI Interface

### Getting Help

```bash
# Show all available commands
django-smartcli --help

# Show version information
django-smartcli --version
```

### Command Examples

```bash
# Create a complete microservice
django-smartcli create-module products

# Create models
django-smartcli create-model Product products
django-smartcli create-model Category products

# Create serializers
django-smartcli create-serializer ProductSerializer products
django-smartcli create-serializer CategorySerializer products

# Create services
django-smartcli create-service ProductService products
django-smartcli create-service CategoryService products

# Create factories
django-smartcli create-factory ProductFactory products
django-smartcli create-factory CategoryFactory products

# Create views
django-smartcli create-views ProductViewSet products
django-smartcli create-views CategoryViewSet products
```

### CLI Features

- **Modern Interface**: Uses kebab-case commands (e.g., `create-module` instead of `create_module`)
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

### Services

- **Format:** PascalCase + "Service" (e.g., `UserProfileService`)
- **File:** snake_case + "\_service" (e.g., `user_profile_service.py`)
- **Methods:** snake_case (e.g., `create_user_profile`)

### Factories

- **Format:** PascalCase + "Factory" (e.g., `UserProfileFactory`)
- **File:** snake_case + "\_factory" (e.g., `user_profile_factory.py`)

## 🧪 Testing

The library includes comprehensive test templates for all generated components:

```bash
# Run all tests
python manage.py test

# Run specific test categories
python manage.py test --models
python manage.py test --serializers
python manage.py test --services
python manage.py test --views
```

## 📋 Requirements

- Python 3.8+
- Django 4.2+
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
# Test the CLI interface
django-smartcli --help
django-smartcli --version

# Test in a Django project
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
