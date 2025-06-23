from django.test import TestCase

from smartcli import templates


class ViewTemplatesTest(TestCase):
    """Test ViewTemplates class."""

    def test_view_template_basic(self):
        """Test basic view template generation."""
        result = templates.ViewTemplates.view_template("UserViewSet", "User", "users")
        
        # Check that the template contains expected elements
        self.assertIn("class UserViewSetViewSet(ViewSet):", result)
        self.assertIn("ViewSet for managing user operations.", result)
        self.assertIn("from users.models import User", result)
        self.assertIn("from users.serializers import UserSerializer", result)
        self.assertIn("from users.services.user_service import UserService", result)
        self.assertIn("permission_classes = [IsAdminUser]", result)
        self.assertIn("serializer_class = UserSerializer", result)

    def test_view_template_with_complex_name(self):
        """Test view template with complex names."""
        result = templates.ViewTemplates.view_template("ProductCategoryViewSet", "ProductCategory", "products")
        
        # Check that the template contains expected elements
        self.assertIn("class ProductCategoryViewSetViewSet(ViewSet):", result)
        self.assertIn("ViewSet for managing productcategory operations.", result)
        self.assertIn("from products.models import ProductCategory", result)
        self.assertIn("from products.serializers import ProductCategorySerializer", result)
        self.assertIn("from products.services.productcategory_service import ProductCategoryService", result)

    def test_view_template_methods(self):
        """Test that view methods are properly generated."""
        result = templates.ViewTemplates.view_template("OrderViewSet", "Order", "orders")
        
        # Check view methods
        self.assertIn("def list(self, request: Request) -> Response:", result)
        self.assertIn("def retrieve(self, request: Request, pk: str) -> Response:", result)
        self.assertIn("def create(self, request: Request) -> Response:", result)
        self.assertIn("def partial_update(self, request: Request, pk: str = None) -> Response:", result)
        self.assertIn("def destroy(self, request: Request, pk: str) -> Response:", result)

    def test_view_template_method_docstrings(self):
        """Test that view methods have proper docstrings."""
        result = templates.ViewTemplates.view_template("UserViewSet", "User", "users")
        
        # Check method docstrings
        self.assertIn('"""List active users."""', result)
        self.assertIn('"""Get a user by its ID."""', result)
        self.assertIn('"""Create a new user."""', result)
        self.assertIn('"""Update a user with the provided data."""', result)
        self.assertIn('"""Delete a user and all related data."""', result)

    def test_view_template_imports(self):
        """Test that view template includes necessary imports."""
        result = templates.ViewTemplates.view_template("UserViewSet", "User", "users")
        
        # Check imports
        self.assertIn("from http import HTTPStatus", result)
        self.assertIn("from rest_framework.permissions import IsAdminUser", result)
        self.assertIn("from rest_framework.request import Request", result)
        self.assertIn("from rest_framework.response import Response", result)
        self.assertIn("from rest_framework.viewsets import ViewSet", result)

    def test_view_template_service_import_path(self):
        """Test that service import path is correctly generated."""
        test_cases = [
            ("UserViewSet", "User", "users", "user_service"),
            ("ProductCategoryViewSet", "ProductCategory", "products", "productcategory_service"),
            ("OrderItemViewSet", "OrderItem", "orders", "orderitem_service")
        ]
        
        for view_name, model_name, app_name, expected_service_name in test_cases:
            with self.subTest(view_name=view_name):
                result = templates.ViewTemplates.view_template(view_name, model_name, app_name)
                self.assertIn(f"from {app_name}.services.{expected_service_name} import {model_name}Service", result)

    def test_view_test_template_basic(self):
        """Test basic view test template generation."""
        result = templates.ViewTemplates.view_test_template("UserViewSet", "User", "users")
        
        # Check that the template contains expected elements
        self.assertIn("class UserViewSetViewSetTest(TestCase):", result)
        self.assertIn("from users.factories import UserFactory", result)
        self.assertIn("from users.models import User", result)
        self.assertIn("def test_list_users_success(self):", result)
        self.assertIn("def test_retrieve_user_success(self):", result)
        self.assertIn("def test_retrieve_user_not_found(self):", result)
        self.assertIn("def test_create_user_success(self):", result)
        self.assertIn("def test_partial_update_user_success(self):", result)
        self.assertIn("def test_destroy_user_success(self):", result)

    def test_view_test_template_with_complex_name(self):
        """Test view test template with complex names."""
        result = templates.ViewTemplates.view_test_template("ProductCategoryViewSet", "ProductCategory", "products")
        
        # Check that the template contains expected elements
        self.assertIn("class ProductCategoryViewSetViewSetTest(TestCase):", result)
        self.assertIn("from products.factories import ProductCategoryFactory", result)
        self.assertIn("from products.models import ProductCategory", result)
        self.assertIn("def test_list_productcategorys_success(self):", result)
        self.assertIn("def test_retrieve_productcategory_success(self):", result)

    def test_view_test_template_method_names(self):
        """Test that test method names are properly generated."""
        test_cases = [
            ("UserViewSet", "User", "users", "user"),
            ("ProductCategoryViewSet", "ProductCategory", "products", "productcategory"),
            ("OrderItemViewSet", "OrderItem", "orders", "orderitem")
        ]
        
        for view_name, model_name, app_name, expected_lower_name in test_cases:
            with self.subTest(view_name=view_name):
                result = templates.ViewTemplates.view_test_template(view_name, model_name, app_name)
                self.assertIn(f"def test_list_{expected_lower_name}s_success(self):", result)
                self.assertIn(f"def test_retrieve_{expected_lower_name}_success(self):", result)
                self.assertIn(f"def test_retrieve_{expected_lower_name}_not_found(self):", result)
                self.assertIn(f"def test_create_{expected_lower_name}_success(self):", result)
                self.assertIn(f"def test_partial_update_{expected_lower_name}_success(self):", result)
                self.assertIn(f"def test_destroy_{expected_lower_name}_success(self):", result)

    def test_view_test_template_docstrings(self):
        """Test that view test methods have proper docstrings."""
        result = templates.ViewTemplates.view_test_template("UserViewSet", "User", "users")
        
        # Check test method docstrings
        self.assertIn('"""Test successful listing of users."""', result)
        self.assertIn('"""Test successful retrieval of a user."""', result)
        self.assertIn('"""Test retrieval of a non-existent user."""', result)
        self.assertIn('"""Test successful creation of a user."""', result)
        self.assertIn('"""Test successful partial update of a user."""', result)
        self.assertIn('"""Test successful deletion of a user."""', result)

    def test_view_test_template_imports(self):
        """Test that view test template includes necessary imports."""
        result = templates.ViewTemplates.view_test_template("UserViewSet", "User", "users")
        
        # Check imports
        self.assertIn("from http import HTTPStatus", result)
        self.assertIn("from unittest.mock import patch", result)
        self.assertIn("from django.urls import reverse", result)
        self.assertIn("from rest_framework import status", result)
        self.assertIn("from rest_framework.test import TestCase", result)

    def test_view_template_class_docstring(self):
        """Test that view template includes proper class docstring."""
        result = templates.ViewTemplates.view_template("UserViewSet", "User", "users")
        
        # Check class docstring
        self.assertIn('"""', result)
        self.assertIn("ViewSet for managing user operations.", result)

    def test_view_test_template_class_docstring(self):
        """Test that view test template includes proper class docstring."""
        result = templates.ViewTemplates.view_test_template("UserViewSet", "User", "users")
        
        # Check class docstring
        self.assertIn('"""', result)
        self.assertIn("Tests for the UserViewSetViewSet.", result)

    def test_view_template_setup_test_data(self):
        """Test that view test template includes setUpTestData method."""
        result = templates.ViewTemplates.view_test_template("UserViewSet", "User", "users")
        
        # Check setUpTestData method
        self.assertIn("@classmethod", result)
        self.assertIn("def setUpTestData(cls):", result)
        self.assertIn("Set up test data shared across all test methods.", result) 