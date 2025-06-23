from setuptools import setup, find_packages

# Read the README file for long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="django-smartcli",
    version="0.2.0",
    packages=find_packages(),
    include_package_data=True,
    
    # Core dependencies
    install_requires=[
        "Django>=4.2,<5.3",
        "djangorestframework>=3.14.0",
        "factory-boy>=3.3.0",
    ],
    
    # Development dependencies
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-django>=4.5.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
        "test": [
            "pytest>=7.0.0",
            "pytest-django>=4.5.0",
            "pytest-cov>=4.0.0",
        ],
    },
    
    # Metadata
    author="Nathan Renard",
    author_email="nathan.renard@example.com",
    description="A smart CLI for Django to help you create and manage microservices with consistent architecture",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nathanrenard3/django-smartcli",
    license="MIT",
    project_urls={
        "Bug Reports": "https://github.com/nathanrenard3/django-smartcli/issues",
        "Source": "https://github.com/nathanrenard3/django-smartcli",
        "Documentation": "https://github.com/nathanrenard3/django-smartcli#readme",
    },
    
    # Classifiers
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Framework :: Django",
        "Framework :: Django :: 4.2",
        "Framework :: Django :: 5.0",
        "Framework :: Django :: 5.1",
        "Framework :: Django :: 5.2",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    
    # Keywords for PyPI search
    keywords=[
        "django",
        "cli",
        "code-generation",
        "microservices",
        "rest-api",
        "django-rest-framework",
        "factory-boy",
        "testing",
        "scaffolding",
        "boilerplate",
    ],
    
    # Python version requirement
    python_requires=">=3.8",
    
    # Package data
    package_data={
        "smartcli": [
            "templates/*.py",
            "management/commands/*.py",
            "cli.py",
        ],
    },
    
    entry_points={
        "console_scripts": [
            "django-smartcli=smartcli.cli:main",
        ],
    },
    
    # Zip safe
    zip_safe=False,
)
