from django.test import TestCase

from smartcli import config


class DirectoryStructureTest(TestCase):
    """Test directory structure constants."""

    def test_directories_list(self):
        """Test that DIRECTORIES contains all expected directories."""
        expected_directories = [
            "factories",
            "migrations", 
            "models",
            "serializers",
            "services",
            "views",
            "tests",
        ]
        
        self.assertEqual(config.DIRECTORIES, expected_directories)
        self.assertEqual(len(config.DIRECTORIES), 7)

    def test_directories_are_strings(self):
        """Test that all directories are strings."""
        for directory in config.DIRECTORIES:
            with self.subTest(directory=directory):
                self.assertIsInstance(directory, str)

    def test_directories_are_lowercase(self):
        """Test that all directories use lowercase naming."""
        for directory in config.DIRECTORIES:
            with self.subTest(directory=directory):
                self.assertEqual(directory, directory.lower())

    def test_test_subdirectories_list(self):
        """Test that TEST_SUBDIRECTORIES contains all expected test subdirectories."""
        expected_test_dirs = [
            "models",
            "serializers", 
            "services",
            "views",
        ]
        
        self.assertEqual(config.TEST_SUBDIRECTORIES, expected_test_dirs)
        self.assertEqual(len(config.TEST_SUBDIRECTORIES), 4)

    def test_test_subdirectories_are_in_directories(self):
        """Test that all test subdirectories are also in the main directories list."""
        for test_dir in config.TEST_SUBDIRECTORIES:
            with self.subTest(test_dir=test_dir):
                self.assertIn(test_dir, config.DIRECTORIES)

    def test_directories_no_duplicates(self):
        """Test that there are no duplicate directories."""
        self.assertEqual(len(config.DIRECTORIES), len(set(config.DIRECTORIES)))

    def test_test_subdirectories_no_duplicates(self):
        """Test that there are no duplicate test subdirectories."""
        self.assertEqual(len(config.TEST_SUBDIRECTORIES), len(set(config.TEST_SUBDIRECTORIES)))

    def test_test_subdirectories_sorted_alphabetically(self):
        """Test that test subdirectories are sorted alphabetically."""
        sorted_test_dirs = sorted(config.TEST_SUBDIRECTORIES)
        self.assertEqual(config.TEST_SUBDIRECTORIES, sorted_test_dirs) 