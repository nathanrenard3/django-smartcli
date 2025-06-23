import os
import tempfile
from django.test import TestCase

from smartcli import utils


class FileOperationsTest(TestCase):
    """Test file operation functions."""

    def setUp(self):
        """Set up temporary directory for file tests."""
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.temp_dir, "test.txt")

    def tearDown(self):
        """Clean up temporary files."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        if os.path.exists(self.temp_dir):
            os.rmdir(self.temp_dir)

    def test_check_file_exists(self):
        """Test check_file_exists function."""
        # File doesn't exist
        self.assertFalse(utils.check_file_exists(self.test_file))
        
        # Create file
        with open(self.test_file, 'w') as f:
            f.write("test content")
        
        # File exists
        self.assertTrue(utils.check_file_exists(self.test_file))

    def test_ensure_directory_exists(self):
        """Test ensure_directory_exists function."""
        new_dir = os.path.join(self.temp_dir, "new_subdir")
        
        # Directory doesn't exist initially
        self.assertFalse(os.path.exists(new_dir))
        
        # Create directory
        utils.ensure_directory_exists(new_dir)
        
        # Directory should exist now
        self.assertTrue(os.path.exists(new_dir))
        
        # Clean up
        os.rmdir(new_dir)

    def test_read_file_content(self):
        """Test read_file_content function."""
        test_content = "Hello, World!\nThis is a test file."
        
        # Read non-existent file
        self.assertEqual(utils.read_file_content(self.test_file), "")
        
        # Create and read file
        with open(self.test_file, 'w', encoding='utf-8') as f:
            f.write(test_content)
        
        result = utils.read_file_content(self.test_file)
        self.assertEqual(result, test_content)

    def test_write_file_content(self):
        """Test write_file_content function."""
        test_content = "Hello, World!\nThis is a test file."
        
        # Write content to file
        utils.write_file_content(self.test_file, test_content)
        
        # Verify content was written
        with open(self.test_file, 'r', encoding='utf-8') as f:
            result = f.read()
        
        self.assertEqual(result, test_content)

    def test_write_file_content_creates_directory(self):
        """Test that write_file_content creates parent directories."""
        sub_dir = os.path.join(self.temp_dir, "subdir")
        file_in_sub_dir = os.path.join(sub_dir, "test.txt")
        test_content = "Test content"
        
        # Write to file in non-existent directory
        utils.write_file_content(file_in_sub_dir, test_content)
        
        # Verify directory and file were created
        self.assertTrue(os.path.exists(sub_dir))
        self.assertTrue(os.path.exists(file_in_sub_dir))
        
        # Clean up
        os.remove(file_in_sub_dir)
        os.rmdir(sub_dir)
