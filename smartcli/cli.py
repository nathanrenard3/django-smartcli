"""
Command Line Interface for Django SmartCLI.

This module provides a direct CLI interface for Django SmartCLI commands,
allowing users to run commands without using python manage.py.
"""

import sys
import os
from typing import List, Optional


def main(args: Optional[List[str]] = None) -> int:
    """
    Main entry point for the Django SmartCLI command line interface.
    
    Args:
        args: Command line arguments (defaults to sys.argv[1:])
        
    Returns:
        int: Exit code (0 for success, 1 for error)
    """
    if args is None:
        args = sys.argv[1:]
    
    if not args:
        print_help()
        return 0
    
    command = args[0].lower()
    
    try:
        if command in ["help", "--help", "-h"]:
            print_help()
            return 0
        elif command in ["version", "--version", "-v"]:
            print_version()
            return 0
        elif command == "create-module":
            return run_django_command("create_module", args[1:])
        elif command == "create-model":
            return run_django_command("create_model", args[1:])
        elif command == "create-serializer":
            return run_django_command("create_serializer", args[1:])
        elif command == "create-service":
            return run_django_command("create_service", args[1:])
        elif command == "create-factory":
            return run_django_command("create_factory", args[1:])
        elif command == "create-views":
            return run_django_command("create_views", args[1:])
        else:
            print(f"❌ Unknown command: {command}")
            print_help()
            return 1
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return 1


def run_django_command(command: str, args: List[str]) -> int:
    """
    Run a Django management command.
    
    Args:
        command: The Django command to run
        args: Arguments for the command
        
    Returns:
        int: Exit code
    """
    try:
        # Check if we're in a Django project
        if not is_django_project():
            print("❌ Error: Not in a Django project directory")
            print("   Please run this command from your Django project root")
            return 1
        
        # Build the command
        cmd_args = ["python", "manage.py", command] + args
        
        # Execute the command
        import subprocess
        result = subprocess.run(cmd_args, capture_output=True, text=True)
        
        # Print output
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        
        return result.returncode
        
    except FileNotFoundError:
        print("❌ Error: 'python' command not found")
        return 1
    except Exception as e:
        print(f"❌ Error running Django command: {str(e)}")
        return 1


def is_django_project() -> bool:
    """
    Check if the current directory is a Django project.
    
    Returns:
        bool: True if this is a Django project directory
    """
    return os.path.exists("manage.py")


def print_help() -> None:
    """Print help information."""
    help_text = """
🚀 Django SmartCLI - Smart Command Line Interface for Django

USAGE:
    django-smartcli <command> [options]

COMMANDS:
    create-module <name>           Create a new Django module with complete structure
    create-model <name> <app>      Create a Django model with best practices
    create-serializer <name> <app> Create a DRF serializer
    create-service <name> <app>    Create a business logic service
    create-factory <name> <app>    Create a factory_boy factory
    create-views <name> <app>      Create a DRF ViewSet

OPTIONS:
    -h, --help     Show this help message
    -v, --version  Show version information

EXAMPLES:
    django-smartcli create-module users
    django-smartcli create-model UserProfile users
    django-smartcli create-serializer UserProfileSerializer users
    django-smartcli create-service UserProfileService users

For more information, visit: https://github.com/nathanrenard3/django-smartcli
"""
    print(help_text)


def print_version() -> None:
    """Print version information."""
    version = "0.1.0"
    print(f"Django SmartCLI v{version}")
    print("A smart CLI for Django to help you create and manage microservices")
    print("https://github.com/nathanrenard3/django-smartcli")


if __name__ == "__main__":
    sys.exit(main()) 