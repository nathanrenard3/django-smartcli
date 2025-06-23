from django.test import TestCase

from smartcli import utils


class ValidatePascalCaseNameTest(TestCase):
    """Test the validate_pascal_case_name function."""

    def test_valid_pascal_case_names(self):
        """Test that valid PascalCase names pass validation."""
        valid_names = [
            "User",
            "UserProfile",
            "ProductCategory",
            "OrderItem",
            "APIEndpoint",
            "User123",
            "Product_With_Underscore"
        ]
        
        for name in valid_names:
            with self.subTest(name=name):
                # Should not raise any exception
                utils.validate_pascal_case_name(name, "Model")

    def test_invalid_names_starting_with_lowercase(self):
        """Test that names starting with lowercase fail validation."""
        invalid_names = [
            "user",
            "userProfile",
            "productCategory",
            "orderItem"
        ]
        
        for name in invalid_names:
            with self.subTest(name=name):
                with self.assertRaises(ValueError) as cm:
                    utils.validate_pascal_case_name(name, "Model")
                self.assertIn("must start with an uppercase letter", str(cm.exception))

    def test_invalid_names_with_special_characters(self):
        """Test that names with special characters fail validation."""
        invalid_names = [
            "User@Profile",
            "Product-Category",
            "Order.Item",
            "User#123",
            "Product$Name"
        ]
        
        for name in invalid_names:
            with self.subTest(name=name):
                with self.assertRaises(ValueError) as cm:
                    utils.validate_pascal_case_name(name, "Model")
                self.assertIn("can only contain letters, numbers, and underscores", str(cm.exception))

    def test_empty_name(self):
        """Test that empty names fail validation."""
        with self.assertRaises(IndexError):
            utils.validate_pascal_case_name("", "Model")