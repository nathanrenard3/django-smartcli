import re
from django.test import TestCase

from smartcli import config


class ValidationPatternsTest(TestCase):
    """Test validation patterns configuration."""

    def test_validation_patterns_keys(self):
        """Test that VALIDATION_PATTERNS contains all expected keys."""
        expected_keys = ["pascal_case", "snake_case", "app_name"]
        
        for key in expected_keys:
            with self.subTest(key=key):
                self.assertIn(key, config.VALIDATION_PATTERNS)

    def test_validation_patterns_are_strings(self):
        """Test that all validation patterns are strings."""
        for pattern in config.VALIDATION_PATTERNS.values():
            with self.subTest(pattern=pattern):
                self.assertIsInstance(pattern, str)

    def test_validation_patterns_are_valid_regex(self):
        """Test that all validation patterns are valid regex patterns."""
        for pattern_name, pattern in config.VALIDATION_PATTERNS.items():
            with self.subTest(pattern_name=pattern_name):
                try:
                    re.compile(pattern)
                except re.error:
                    self.fail(f"Invalid regex pattern for {pattern_name}: {pattern}")

    def test_pascal_case_pattern_valid_cases(self):
        """Test that pascal_case pattern matches valid PascalCase strings."""
        pattern = re.compile(config.VALIDATION_PATTERNS["pascal_case"])
        valid_cases = [
            "User",
            "UserProfile", 
            "ProductCategory",
            "OrderItem",
            "APIEndpoint",
            "User123",
            "Product_With_Underscore"
        ]
        
        for case in valid_cases:
            with self.subTest(case=case):
                self.assertIsNotNone(pattern.match(case))

    def test_pascal_case_pattern_invalid_cases(self):
        """Test that pascal_case pattern rejects invalid cases."""
        pattern = re.compile(config.VALIDATION_PATTERNS["pascal_case"])
        invalid_cases = [
            "user",  # starts with lowercase
            "userProfile",  # starts with lowercase
            "product-category",  # contains hyphen
            "Order.Item",  # contains dot
            "User#123",  # contains special character
            "Product$Name",  # contains special character
            "",  # empty string
        ]
        
        for case in invalid_cases:
            with self.subTest(case=case):
                self.assertIsNone(pattern.match(case))

    def test_snake_case_pattern_valid_cases(self):
        """Test that snake_case pattern matches valid snake_case strings."""
        pattern = re.compile(config.VALIDATION_PATTERNS["snake_case"])
        valid_cases = [
            "user",
            "user_profile",
            "product_category",
            "order_item",
            "api_endpoint",
            "user123",
            "product_with_underscore"
        ]
        
        for case in valid_cases:
            with self.subTest(case=case):
                self.assertIsNotNone(pattern.match(case))

    def test_snake_case_pattern_invalid_cases(self):
        """Test that snake_case pattern rejects invalid cases."""
        pattern = re.compile(config.VALIDATION_PATTERNS["snake_case"])
        invalid_cases = [
            "User",  # starts with uppercase
            "UserProfile",  # contains uppercase
            "product-category",  # contains hyphen
            "order.item",  # contains dot
            "user#123",  # contains special character
            "product$name",  # contains special character
            "",  # empty string
        ]
        
        for case in invalid_cases:
            with self.subTest(case=case):
                self.assertIsNone(pattern.match(case))

    def test_app_name_pattern_valid_cases(self):
        """Test that app_name pattern matches valid app names."""
        pattern = re.compile(config.VALIDATION_PATTERNS["app_name"])
        valid_cases = [
            "users",
            "user_profiles",
            "product_categories",
            "order_items",
            "api_endpoints",
            "user123",
            "product_with_underscore"
        ]
        
        for case in valid_cases:
            with self.subTest(case=case):
                self.assertIsNotNone(pattern.match(case))

    def test_app_name_pattern_invalid_cases(self):
        """Test that app_name pattern rejects invalid app names."""
        pattern = re.compile(config.VALIDATION_PATTERNS["app_name"])
        invalid_cases = [
            "Users",  # starts with uppercase
            "UserProfiles",  # contains uppercase
            "product-categories",  # contains hyphen
            "order.items",  # contains dot
            "user#123",  # contains special character
            "product$name",  # contains special character
            "",  # empty string
        ]
        
        for case in invalid_cases:
            with self.subTest(case=case):
                self.assertIsNone(pattern.match(case))

    def test_pascal_case_pattern_starts_with_uppercase(self):
        """Test that pascal_case pattern requires uppercase first letter."""
        pattern = re.compile(config.VALIDATION_PATTERNS["pascal_case"])
        
        # Should match uppercase first letter
        self.assertIsNotNone(pattern.match("User"))
        
        # Should not match lowercase first letter
        self.assertIsNone(pattern.match("user"))

    def test_snake_case_pattern_starts_with_lowercase(self):
        """Test that snake_case pattern requires lowercase first letter."""
        pattern = re.compile(config.VALIDATION_PATTERNS["snake_case"])
        
        # Should match lowercase first letter
        self.assertIsNotNone(pattern.match("user"))
        
        # Should not match uppercase first letter
        self.assertIsNone(pattern.match("User"))

    def test_app_name_pattern_starts_with_lowercase(self):
        """Test that app_name pattern requires lowercase first letter."""
        pattern = re.compile(config.VALIDATION_PATTERNS["app_name"])
        
        # Should match lowercase first letter
        self.assertIsNotNone(pattern.match("users"))
        
        # Should not match uppercase first letter
        self.assertIsNone(pattern.match("Users"))

    def test_patterns_allow_underscores(self):
        """Test that all patterns allow underscores."""
        pascal_pattern = re.compile(config.VALIDATION_PATTERNS["pascal_case"])
        snake_pattern = re.compile(config.VALIDATION_PATTERNS["snake_case"])
        app_pattern = re.compile(config.VALIDATION_PATTERNS["app_name"])
        
        # Test with underscores
        self.assertIsNotNone(pascal_pattern.match("User_Profile"))
        self.assertIsNotNone(snake_pattern.match("user_profile"))
        self.assertIsNotNone(app_pattern.match("user_profiles"))

    def test_patterns_allow_numbers(self):
        """Test that all patterns allow numbers."""
        pascal_pattern = re.compile(config.VALIDATION_PATTERNS["pascal_case"])
        snake_pattern = re.compile(config.VALIDATION_PATTERNS["snake_case"])
        app_pattern = re.compile(config.VALIDATION_PATTERNS["app_name"])
        
        # Test with numbers
        self.assertIsNotNone(pascal_pattern.match("User123"))
        self.assertIsNotNone(snake_pattern.match("user123"))
        self.assertIsNotNone(app_pattern.match("user123")) 