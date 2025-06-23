from django.test import TestCase

from smartcli import utils


class CaseConversionTest(TestCase):
    """Test case conversion functions."""

    def test_pascal_to_snake_case(self):
        """Test PascalCase to snake_case conversion."""
        test_cases = [
            ("User", "user"),
            ("UserProfile", "user_profile"),
            ("ProductCategory", "product_category"),
            ("OrderItem", "order_item"),
            ("APIEndpoint", "a_p_i_endpoint"),
            ("User123", "user123"),
            ("Product_With_Underscore", "product_with_underscore")
        ]
        
        for pascal, expected_snake in test_cases:
            with self.subTest(pascal=pascal):
                result = utils.pascal_to_snake_case(pascal)
                self.assertEqual(result, expected_snake)

    def test_snake_to_pascal_case(self):
        """Test snake_case to PascalCase conversion."""
        test_cases = [
            ("user", "User"),
            ("user_profile", "UserProfile"),
            ("product_category", "ProductCategory"),
            ("order_item", "OrderItem"),
            ("api_endpoint", "ApiEndpoint"),
            ("user123", "User123"),
            ("product_with_underscore", "ProductWithUnderscore")
        ]
        
        for snake, expected_pascal in test_cases:
            with self.subTest(snake=snake):
                result = utils.snake_to_pascal_case(snake)
                self.assertEqual(result, expected_pascal)

