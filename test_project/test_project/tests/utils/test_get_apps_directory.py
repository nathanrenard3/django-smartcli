from django.test import TestCase, override_settings
from django.conf import settings

from smartcli import utils


class GetAppsDirectoryTest(TestCase):
    """Test the get_apps_directory function."""

    @override_settings(USE_CENTRALIZED_APPS=True)
    def test_centralized_apps_enabled(self):
        """Test when centralized apps are enabled."""
        result = utils.get_apps_directory()
        self.assertEqual(result, "apps")

    @override_settings(USE_CENTRALIZED_APPS=False)
    def test_centralized_apps_disabled(self):
        """Test when centralized apps are disabled."""
        result = utils.get_apps_directory()
        self.assertEqual(result, "")

    def test_centralized_apps_not_set(self):
        """Test when USE_CENTRALIZED_APPS is not set (defaults to True)."""
        # Temporarily remove the setting to test default behavior
        original_setting = getattr(settings, 'USE_CENTRALIZED_APPS', None)
        
        # Remove the setting if it exists
        if hasattr(settings, 'USE_CENTRALIZED_APPS'):
            delattr(settings, 'USE_CENTRALIZED_APPS')
        
        try:
            result = utils.get_apps_directory()
            self.assertEqual(result, "apps")
        finally:
            # Restore the original setting
            if original_setting is not None:
                setattr(settings, 'USE_CENTRALIZED_APPS', original_setting)
