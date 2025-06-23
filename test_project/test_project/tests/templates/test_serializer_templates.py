from django.test import TestCase

from smartcli import templates


class SerializerTemplatesTest(TestCase):
    """Test SerializerTemplates class."""

    def test_serializer_template_basic(self):
        """Test basic serializer template generation."""
        result = templates.SerializerTemplates.serializer_template("UserSerializer", "User", "users")
        
        # Check that the template contains expected elements
        self.assertIn("class UserSerializerSerializer(serializers.ModelSerializer):", result)
        self.assertIn("from users.models import User", result)
        self.assertIn("model = User", result)
        self.assertIn('fields = [', result)
        self.assertIn('"id"', result)
        self.assertIn('"created_at"', result)
        self.assertIn('"deleted_at"', result)
        self.assertIn('read_only_fields = [', result)
        self.assertIn('"id"', result)
        self.assertIn('"created_at"', result)

    def test_serializer_template_with_complex_name(self):
        """Test serializer template with complex names."""
        result = templates.SerializerTemplates.serializer_template("ProductCategorySerializer", "ProductCategory", "products")
        
        # Check that the template contains expected elements
        self.assertIn("class ProductCategorySerializerSerializer(serializers.ModelSerializer):", result)
        self.assertIn("from products.models import ProductCategory", result)
        self.assertIn("model = ProductCategory", result)

    def test_serializer_template_fields_structure(self):
        """Test that serializer fields are properly structured."""
        result = templates.SerializerTemplates.serializer_template("OrderSerializer", "Order", "orders")
        
        # Check fields structure
        self.assertIn('fields = [', result)
        self.assertIn('"id",', result)
        self.assertIn('"created_at",', result)
        self.assertIn('"deleted_at",', result)
        
        # Check read_only_fields structure
        self.assertIn('read_only_fields = [', result)
        self.assertIn('"id",', result)
        self.assertIn('"created_at",', result)

    def test_serializer_test_template_basic(self):
        """Test basic serializer test template generation."""
        result = templates.SerializerTemplates.serializer_test_template("UserSerializer", "User", "users")
        
        # Check that the template contains expected elements
        self.assertIn("class UserSerializerSerializerTest(TestCase):", result)
        self.assertIn("from users.factories import UserFactory", result)
        self.assertIn("from users.models import User", result)
        self.assertIn("from users.serializers import UserSerializerSerializer", result)
        self.assertIn("cls.user = UserFactory()", result)
        self.assertIn("def test_serializer_contains_expected_fields(self):", result)
        self.assertIn("def test_serializer_read_only_fields(self):", result)
        self.assertIn("def test_serializer_model_class(self):", result)

    def test_serializer_test_template_with_complex_name(self):
        """Test serializer test template with complex names."""
        result = templates.SerializerTemplates.serializer_test_template("ProductCategorySerializer", "ProductCategory", "products")
        
        # Check that the template contains expected elements
        self.assertIn("class ProductCategorySerializerSerializerTest(TestCase):", result)
        self.assertIn("from products.factories import ProductCategoryFactory", result)
        self.assertIn("from products.models import ProductCategory", result)
        self.assertIn("from products.serializers import ProductCategorySerializerSerializer", result)
        self.assertIn("cls.productcategory = ProductCategoryFactory()", result)

    def test_serializer_test_template_test_methods(self):
        """Test that serializer test methods are properly generated."""
        result = templates.SerializerTemplates.serializer_test_template("OrderSerializer", "Order", "orders")
        
        # Check test method content
        self.assertIn("def test_serializer_contains_expected_fields(self):", result)
        self.assertIn("expected_fields = [\"id\", \"created_at\", \"deleted_at\"]", result)
        self.assertIn("def test_serializer_read_only_fields(self):", result)
        self.assertIn("expected_read_only = [\"id\", \"created_at\"]", result)
        self.assertIn("def test_serializer_model_class(self):", result)
        self.assertIn("self.assertEqual(self.serializer.Meta.model, Order)", result)

    def test_serializer_template_docstring(self):
        """Test that serializer template includes proper docstring."""
        result = templates.SerializerTemplates.serializer_template("UserSerializer", "User", "users")
        
        # Check docstring
        self.assertIn('"""', result)
        self.assertIn("Serializer for User model.", result)

    def test_serializer_test_template_docstring(self):
        """Test that serializer test template includes proper docstring."""
        result = templates.SerializerTemplates.serializer_test_template("UserSerializer", "User", "users")
        
        # Check docstring
        self.assertIn('"""', result)
        self.assertIn("Tests for the UserSerializerSerializer.", result) 