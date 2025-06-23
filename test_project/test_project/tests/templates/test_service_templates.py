from django.test import TestCase

from smartcli import templates


class ServiceTemplatesTest(TestCase):
    """Test ServiceTemplates class."""

    def test_service_template_basic(self):
        """Test basic service template generation."""
        result = templates.ServiceTemplates.service_template("UserService")
        
        # Check that the template contains expected elements
        self.assertIn("class UserServiceService:", result)
        self.assertIn("Service for UserService operations.", result)
        self.assertIn("@classmethod", result)
        self.assertIn("@transaction.atomic", result)
        self.assertIn("def create_user_service(cls):", result)
        self.assertIn("def update_user_service(cls):", result)
        self.assertIn("def delete_user_service(cls):", result)

    def test_service_template_with_complex_name(self):
        """Test service template with complex service name."""
        result = templates.ServiceTemplates.service_template("ProductCategoryService")
        
        # Check that the template contains expected elements
        self.assertIn("class ProductCategoryServiceService:", result)
        self.assertIn("Service for ProductCategoryService operations.", result)
        self.assertIn("def create_product_category_service(cls):", result)
        self.assertIn("def update_product_category_service(cls):", result)
        self.assertIn("def delete_product_category_service(cls):", result)

    def test_service_template_method_names(self):
        """Test that method names are properly converted from PascalCase to snake_case."""
        test_cases = [
            ("UserService", "user_service"),
            ("ProductCategoryService", "product_category_service"),
            ("OrderItemService", "order_item_service"),
            ("APIService", "a_p_i_service")
        ]
        
        for service_name, expected_method_name in test_cases:
            with self.subTest(service_name=service_name):
                result = templates.ServiceTemplates.service_template(service_name)
                self.assertIn(f"def create_{expected_method_name}(cls):", result)
                self.assertIn(f"def update_{expected_method_name}(cls):", result)
                self.assertIn(f"def delete_{expected_method_name}(cls):", result)

    def test_service_template_method_docstrings(self):
        """Test that service methods have proper docstrings."""
        result = templates.ServiceTemplates.service_template("UserService")
        
        # Check method docstrings
        self.assertIn('"""\n        Create a new userservice.\n        \n        Returns:\n            The created userservice\n        """', result)
        self.assertIn('"""\n        Update a userservice.\n        """', result)
        self.assertIn('"""\n        Delete a userservice.\n        """', result)

    def test_service_template_imports(self):
        """Test that service template includes necessary imports."""
        result = templates.ServiceTemplates.service_template("UserService")
        
        # Check imports
        self.assertIn("from django.db import transaction", result)

    def test_service_test_template_basic(self):
        """Test basic service test template generation."""
        result = templates.ServiceTemplates.service_test_template("UserService", "users")
        
        # Check that the template contains expected elements
        self.assertIn("class UserServiceServiceTest(TestCase):", result)
        self.assertIn("from users.services import UserServiceService", result)
        self.assertIn("def test_create_user_service_success(self):", result)
        self.assertIn("def test_update_user_service_success(self):", result)
        self.assertIn("def test_delete_user_service_success(self):", result)

    def test_service_test_template_with_complex_name(self):
        """Test service test template with complex service name."""
        result = templates.ServiceTemplates.service_test_template("ProductCategoryService", "products")
        
        # Check that the template contains expected elements
        self.assertIn("class ProductCategoryServiceServiceTest(TestCase):", result)
        self.assertIn("from products.services import ProductCategoryServiceService", result)
        self.assertIn("def test_create_product_category_service_success(self):", result)
        self.assertIn("def test_update_product_category_service_success(self):", result)
        self.assertIn("def test_delete_product_category_service_success(self):", result)

    def test_service_test_template_method_names(self):
        """Test that test method names are properly converted."""
        test_cases = [
            ("UserService", "user_service"),
            ("ProductCategoryService", "product_category_service"),
            ("OrderItemService", "order_item_service"),
            ("APIService", "a_p_i_service")
        ]
        
        for service_name, expected_method_name in test_cases:
            with self.subTest(service_name=service_name):
                result = templates.ServiceTemplates.service_test_template(service_name, "test_app")
                self.assertIn(f"def test_create_{expected_method_name}_success(self):", result)
                self.assertIn(f"def test_update_{expected_method_name}_success(self):", result)
                self.assertIn(f"def test_delete_{expected_method_name}_success(self):", result)

    def test_service_test_template_docstrings(self):
        """Test that service test methods have proper docstrings."""
        result = templates.ServiceTemplates.service_test_template("UserService", "users")
        
        # Check test method docstrings
        self.assertIn('"""Test successful creation of userservice."""', result)
        self.assertIn('"""Test successful update of userservice."""', result)
        self.assertIn('"""Test successful deletion of userservice."""', result)

    def test_service_test_template_imports(self):
        """Test that service test template includes necessary imports."""
        result = templates.ServiceTemplates.service_test_template("UserService", "users")
        
        # Check imports
        self.assertIn("from users.services import UserServiceService", result)
        self.assertIn("from rest_framework.test import TestCase", result)

    def test_service_template_class_docstring(self):
        """Test that service template includes proper class docstring."""
        result = templates.ServiceTemplates.service_template("UserService")
        
        # Check class docstring
        self.assertIn('"""', result)
        self.assertIn("Service for UserService operations.", result)

    def test_service_test_template_class_docstring(self):
        """Test that service test template includes proper class docstring."""
        result = templates.ServiceTemplates.service_test_template("UserService", "users")
        
        # Check class docstring
        self.assertIn('"""', result)
        self.assertIn("Tests for the UserServiceService.", result) 