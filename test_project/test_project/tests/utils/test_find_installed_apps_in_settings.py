import os
import tempfile
from django.test import TestCase

from smartcli import utils


class FindInstalledAppsInSettingsTest(TestCase):
    """Test find_installed_apps_in_settings function."""

    def test_find_installed_apps_found(self):
        """Test when INSTALLED_APPS is found in settings."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.py') as f:
            f.write("""INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'myapp',
]
""")
            settings_file = f.name
        
        try:
            found, content = utils.find_installed_apps_in_settings(settings_file)
            
            self.assertTrue(found)
            self.assertIn("INSTALLED_APPS", content)
        finally:
            os.unlink(settings_file)

    def test_find_installed_apps_not_found(self):
        """Test when INSTALLED_APPS is not found in settings."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.py') as f:
            f.write("""DEBUG = True
SECRET_KEY = 'test'
""")
            settings_file = f.name
        
        try:
            found, content = utils.find_installed_apps_in_settings(settings_file)
            
            self.assertFalse(found)
            self.assertIn("DEBUG", content)
        finally:
            os.unlink(settings_file)

    def test_find_installed_apps_file_not_found(self):
        """Test when settings file doesn't exist."""
        found, content = utils.find_installed_apps_in_settings("/nonexistent/path/settings.py")
        
        self.assertFalse(found)
        self.assertIsNone(content)
