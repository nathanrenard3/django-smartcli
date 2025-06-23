import os
import tempfile
from django.test import TestCase

from smartcli import utils


class CleanUpFilesTest(TestCase):
    """Test clean_up_files function."""

    def setUp(self):
        """Set up temporary directory for file tests."""
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up temporary files."""
        for file_name in os.listdir(self.temp_dir):
            file_path = os.path.join(self.temp_dir, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
        os.rmdir(self.temp_dir)

    def test_clean_up_files(self):
        """Test clean_up_files function."""
        # Create test files
        file1 = os.path.join(self.temp_dir, "test1.txt")
        file2 = os.path.join(self.temp_dir, "test2.txt")
        
        with open(file1, 'w') as f:
            f.write("test1")
        with open(file2, 'w') as f:
            f.write("test2")
        
        # Verify files exist
        self.assertTrue(os.path.exists(file1))
        self.assertTrue(os.path.exists(file2))
        
        # Clean up files
        utils.clean_up_files([file1, file2])
        
        # Verify files were removed
        self.assertFalse(os.path.exists(file1))
        self.assertFalse(os.path.exists(file2))

    def test_clean_up_files_nonexistent(self):
        """Test clean_up_files with non-existent files."""
        nonexistent_file = os.path.join(self.temp_dir, "nonexistent.txt")
        
        # Should not raise an exception
        utils.clean_up_files([nonexistent_file])
