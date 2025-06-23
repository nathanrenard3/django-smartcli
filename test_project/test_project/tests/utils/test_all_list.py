from django.test import TestCase

from smartcli import utils


class AllListTest(TestCase):
    """Test __all__ list manipulation functions."""

    def test_update_all_list_new_list(self):
        """Test update_all_list when __all__ doesn't exist."""
        content = """class MyClass:
    pass
"""
        result = utils.update_all_list(content, "MyClass")
        
        expected = """class MyClass:
    pass

__all__ = [
    "MyClass"
]
"""
        self.assertEqual(result, expected)

    def test_update_all_list_existing_list(self):
        """Test update_all_list when __all__ already exists."""
        content = """class MyClass:
    pass

class AnotherClass:
    pass

__all__ = [
    "AnotherClass"
]
"""
        result = utils.update_all_list(content, "MyClass")
        
        # Should add MyClass and sort alphabetically
        self.assertIn('"AnotherClass"', result)
        self.assertIn('"MyClass"', result)
        self.assertIn("__all__", result)

    def test_update_all_list_item_already_exists(self):
        """Test update_all_list when item already exists."""
        content = """class MyClass:
    pass

__all__ = [
    "MyClass"
]
"""
        result = utils.update_all_list(content, "MyClass")
        
        # Should return unchanged content
        self.assertEqual(result, content)
