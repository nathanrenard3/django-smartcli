from django.test import TestCase

from smartcli import utils


class ExtractModelNameFromNameTest(TestCase):
    """Test the extract_model_name_from_name function."""

    def test_extract_with_suffix(self):
        """Test extracting model name when suffix is present."""
        test_cases = [
            ("UserSerializer", "Serializer", "User"),
            ("ProductService", "Service", "Product"),
            ("OrderFactory", "Factory", "Order"),
            ("CategoryView", "View", "Category")
        ]
        
        for name, suffix, expected in test_cases:
            with self.subTest(name=name, suffix=suffix):
                result = utils.extract_model_name_from_name(name, suffix)
                self.assertEqual(result, expected)

    def test_extract_without_suffix(self):
        """Test extracting model name when suffix is not present."""
        test_cases = [
            ("User", "Serializer", "User"),
            ("Product", "Service", "Product"),
            ("Order", "Factory", "Order")
        ]
        
        for name, suffix, expected in test_cases:
            with self.subTest(name=name, suffix=suffix):
                result = utils.extract_model_name_from_name(name, suffix)
                self.assertEqual(result, expected)
