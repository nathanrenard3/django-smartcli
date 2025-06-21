import glob
import os

from django.core.management.base import CommandError
from django.core.management.commands.test import Command as TestCommand


class Command(TestCommand):
    """
    Custom command that extends Django's test command.
    Allows filtering tests by type (models, services, serializers, views).

    Usage:
        python manage.py test --models
        python manage.py test --services
        python manage.py test --serializers
        python manage.py test --views
    """

    def add_arguments(self, parser):
        """Add custom arguments to the command."""
        super().add_arguments(parser)

        # Add filtering options
        parser.add_argument(
            "--models",
            action="store_true",
            help='Run only tests in "models" directories',
        )
        parser.add_argument(
            "--services",
            action="store_true",
            help='Run only tests in "services" directories',
        )
        parser.add_argument(
            "--serializers",
            action="store_true",
            help='Run only tests in "serializers" directories',
        )
        parser.add_argument(
            "--views",
            action="store_true",
            help='Run only tests in "views" directories',
        )

    def handle(self, *test_labels, **options):
        """Handle command execution with filtering."""
        # Get filtering options
        filter_options = {
            "models": options.get("models", False),
            "services": options.get("services", False),
            "serializers": options.get("serializers", False),
            "views": options.get("views", False),
        }

        # Check that only one filtering option is used
        active_filters = [k for k, v in filter_options.items() if v]
        if len(active_filters) > 1:
            raise CommandError(
                f"You can only use one filtering option at a time. "
                f"Active options: {', '.join(active_filters)}"
            )

        # If a filter is active, modify test_labels
        if active_filters:
            filter_type = active_filters[0]
            filtered_labels = self._get_filtered_test_labels(filter_type)

            if not filtered_labels:
                self.stdout.write(
                    self.style.WARNING(f"No tests found for filter '{filter_type}'")
                )
                return

            # Replace test_labels with filtered labels
            test_labels = filtered_labels
            self.stdout.write(
                self.style.SUCCESS(
                    f"Running tests filtered by '{filter_type}': {len(test_labels)} files with tests found"
                )
            )

        # Call parent method with potentially modified labels
        super().handle(*test_labels, **options)

    def _get_filtered_test_labels(self, filter_type: str) -> list:
        """
        Get filtered test labels by type.

        Args:
            filter_type: The filter type (models, services, etc.)

        Returns:
            List of test labels to execute
        """
        test_labels = []

        # Iterate through all Django apps
        from django.conf import settings

        for app_config in settings.INSTALLED_APPS:
            if app_config.startswith("apps."):
                app_name = app_config.replace("apps.", "")
                test_dir = f"apps/{app_name}/tests/{filter_type}"

                if os.path.exists(test_dir):
                    # Find all test files in this directory
                    test_files = glob.glob(f"{test_dir}/test_*.py")
                    test_files.extend(glob.glob(f"{test_dir}/*/test_*.py"))

                    for test_file in test_files:
                        # Convert path to Django test label
                        # Ex: apps/account/tests/models/test_user.py -> apps.account.tests.models.test_user
                        relative_path = test_file.replace("/", ".").replace(".py", "")
                        test_labels.append(relative_path)

        return test_labels
