from django.test import TestCase

from smartcli import utils


class ImportSectionTest(TestCase):
    """Test import section manipulation functions."""

    def test_find_import_section_end(self):
        """Test find_import_section_end function."""
        content = """import os
import sys
from django.conf import settings

class MyClass:
    pass
"""
        result = utils.find_import_section_end(content)
        self.assertEqual(result, 3)  # After the last import line

    def test_find_import_section_end_with_comments(self):
        """Test find_import_section_end with comments."""
        content = """# This is a comment
import os
# Another comment
import sys
from django.conf import settings

class MyClass:
    pass
"""
        result = utils.find_import_section_end(content)
        self.assertEqual(result, 5)  # After the last import line

    def test_find_import_section_end_no_imports(self):
        """Test find_import_section_end with no imports."""
        content = """class MyClass:
    pass

def my_function():
    pass
"""
        result = utils.find_import_section_end(content)
        self.assertEqual(result, 0)  # No imports found

    def test_add_import_to_content(self):
        """Test add_import_to_content function."""
        original_content = """import os
import sys

class MyClass:
    pass
"""
        new_import = "from django.conf import settings"
        
        result = utils.add_import_to_content(original_content, new_import)
        
        expected = """import os
import sys
from django.conf import settings

class MyClass:
    pass
"""
        self.assertEqual(result, expected)

    def test_add_import_to_content_already_exists(self):
        """Test add_import_to_content when import already exists."""
        original_content = """import os
from django.conf import settings

class MyClass:
    pass
"""
        new_import = "from django.conf import settings"
        
        result = utils.add_import_to_content(original_content, new_import)
        
        # Should return original content unchanged
        self.assertEqual(result, original_content)
