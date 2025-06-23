from django.test import TestCase

from smartcli import config


class FileSuffixesTest(TestCase):
    """Test file suffixes configuration."""

    def test_file_suffixes_keys(self):
        """Test that FILE_SUFFIXES contains all expected keys."""
        expected_keys = ["model", "serializer", "service", "factory", "view"]
        
        for key in expected_keys:
            with self.subTest(key=key):
                self.assertIn(key, config.FILE_SUFFIXES)

    def test_file_suffixes_values(self):
        """Test that FILE_SUFFIXES contains expected values."""
        expected_values = {
            "model": "",
            "serializer": "_serializer",
            "service": "_service",
            "factory": "_factory",
            "view": "_view",
        }
        
        for key, expected_value in expected_values.items():
            with self.subTest(key=key):
                self.assertEqual(config.FILE_SUFFIXES[key], expected_value)

    def test_file_suffixes_are_strings(self):
        """Test that all file suffixes are strings."""
        for suffix in config.FILE_SUFFIXES.values():
            with self.subTest(suffix=suffix):
                self.assertIsInstance(suffix, str)

    def test_file_suffixes_no_duplicates(self):
        """Test that there are no duplicate file suffixes."""
        suffixes = list(config.FILE_SUFFIXES.values())
        self.assertEqual(len(suffixes), len(set(suffixes)))

    def test_model_suffix_is_empty(self):
        """Test that model suffix is empty string."""
        self.assertEqual(config.FILE_SUFFIXES["model"], "")

    def test_serializer_suffix_has_underscore(self):
        """Test that serializer suffix starts with underscore."""
        self.assertTrue(config.FILE_SUFFIXES["serializer"].startswith("_"))

    def test_service_suffix_has_underscore(self):
        """Test that service suffix starts with underscore."""
        self.assertTrue(config.FILE_SUFFIXES["service"].startswith("_"))

    def test_factory_suffix_has_underscore(self):
        """Test that factory suffix starts with underscore."""
        self.assertTrue(config.FILE_SUFFIXES["factory"].startswith("_"))

    def test_view_suffix_has_underscore(self):
        """Test that view suffix starts with underscore."""
        self.assertTrue(config.FILE_SUFFIXES["view"].startswith("_"))


class ImportSuffixesTest(TestCase):
    """Test import suffixes configuration."""

    def test_import_suffixes_keys(self):
        """Test that IMPORT_SUFFIXES contains all expected keys."""
        expected_keys = ["model", "serializer", "service", "factory", "view"]
        
        for key in expected_keys:
            with self.subTest(key=key):
                self.assertIn(key, config.IMPORT_SUFFIXES)

    def test_import_suffixes_values(self):
        """Test that IMPORT_SUFFIXES contains expected values."""
        expected_values = {
            "model": "",
            "serializer": "Serializer",
            "service": "Service",
            "factory": "Factory",
            "view": "View",
        }
        
        for key, expected_value in expected_values.items():
            with self.subTest(key=key):
                self.assertEqual(config.IMPORT_SUFFIXES[key], expected_value)

    def test_import_suffixes_are_strings(self):
        """Test that all import suffixes are strings."""
        for suffix in config.IMPORT_SUFFIXES.values():
            with self.subTest(suffix=suffix):
                self.assertIsInstance(suffix, str)

    def test_import_suffixes_no_duplicates(self):
        """Test that there are no duplicate import suffixes."""
        suffixes = list(config.IMPORT_SUFFIXES.values())
        self.assertEqual(len(suffixes), len(set(suffixes)))

    def test_model_import_suffix_is_empty(self):
        """Test that model import suffix is empty string."""
        self.assertEqual(config.IMPORT_SUFFIXES["model"], "")

    def test_serializer_import_suffix_is_pascal_case(self):
        """Test that serializer import suffix is PascalCase."""
        suffix = config.IMPORT_SUFFIXES["serializer"]
        self.assertTrue(suffix[0].isupper())
        self.assertEqual(suffix, "Serializer")

    def test_service_import_suffix_is_pascal_case(self):
        """Test that service import suffix is PascalCase."""
        suffix = config.IMPORT_SUFFIXES["service"]
        self.assertTrue(suffix[0].isupper())
        self.assertEqual(suffix, "Service")

    def test_factory_import_suffix_is_pascal_case(self):
        """Test that factory import suffix is PascalCase."""
        suffix = config.IMPORT_SUFFIXES["factory"]
        self.assertTrue(suffix[0].isupper())
        self.assertEqual(suffix, "Factory")

    def test_view_import_suffix_is_pascal_case(self):
        """Test that view import suffix is PascalCase."""
        suffix = config.IMPORT_SUFFIXES["view"]
        self.assertTrue(suffix[0].isupper())
        self.assertEqual(suffix, "View")


class TestSuffixesTest(TestCase):
    """Test test suffixes configuration."""

    def test_test_suffixes_keys(self):
        """Test that TEST_SUFFIXES contains all expected keys."""
        expected_keys = ["model", "serializer", "service", "factory", "view"]
        
        for key in expected_keys:
            with self.subTest(key=key):
                self.assertIn(key, config.TEST_SUFFIXES)

    def test_test_suffixes_values(self):
        """Test that TEST_SUFFIXES contains expected values."""
        expected_values = {
            "model": ["ModelTest", "ManagerTest"],
            "serializer": ["SerializerTest"],
            "service": ["ServiceTest"],
            "factory": ["FactoryTest"],
            "view": ["ViewTest"],
        }
        
        for key, expected_value in expected_values.items():
            with self.subTest(key=key):
                self.assertEqual(config.TEST_SUFFIXES[key], expected_value)

    def test_test_suffixes_are_lists(self):
        """Test that all test suffixes are lists."""
        for suffixes in config.TEST_SUFFIXES.values():
            with self.subTest(suffixes=suffixes):
                self.assertIsInstance(suffixes, list)

    def test_test_suffixes_contain_strings(self):
        """Test that all test suffix lists contain strings."""
        for suffixes in config.TEST_SUFFIXES.values():
            for suffix in suffixes:
                with self.subTest(suffix=suffix):
                    self.assertIsInstance(suffix, str)

    def test_model_test_suffixes_count(self):
        """Test that model has exactly 2 test suffixes."""
        self.assertEqual(len(config.TEST_SUFFIXES["model"]), 2)

    def test_other_test_suffixes_count(self):
        """Test that other types have exactly 1 test suffix."""
        single_suffix_types = ["serializer", "service", "factory", "view"]
        for suffix_type in single_suffix_types:
            with self.subTest(suffix_type=suffix_type):
                self.assertEqual(len(config.TEST_SUFFIXES[suffix_type]), 1)

    def test_all_test_suffixes_end_with_test(self):
        """Test that all test suffixes end with 'Test'."""
        for suffixes in config.TEST_SUFFIXES.values():
            for suffix in suffixes:
                with self.subTest(suffix=suffix):
                    self.assertTrue(suffix.endswith("Test"))

    def test_model_test_suffixes_contain_manager_test(self):
        """Test that model test suffixes include ManagerTest."""
        self.assertIn("ManagerTest", config.TEST_SUFFIXES["model"]) 