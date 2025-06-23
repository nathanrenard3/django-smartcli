from django.test import TestCase

from smartcli import templates


class ModelTemplatesTest(TestCase):
    """Test ModelTemplates class."""

    def test_model_template_basic(self):
        """Test basic model template generation."""
        result = templates.ModelTemplates.model_template("User")
        
        # Check that the template contains expected elements
        self.assertIn("class User(models.Model):", result)
        self.assertIn("class UserManager(models.Manager):", result)
        self.assertIn("id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)", result)
        self.assertIn("created_at = models.DateTimeField(default=timezone.now)", result)
        self.assertIn("deleted_at = models.DateTimeField(null=True, blank=True)", result)
        self.assertIn("objects = UserManager()", result)

    def test_model_template_with_complex_name(self):
        """Test model template with complex model name."""
        result = templates.ModelTemplates.model_template("UserProfile")
        
        # Check that the template contains expected elements
        self.assertIn("class UserProfile(models.Model):", result)
        self.assertIn("class UserProfileManager(models.Manager):", result)
        self.assertIn("userprofile_id: str", result)  # Check parameter name
        self.assertIn("userprofile = self.get(id=userprofile_id)", result)  # Check variable name

    def test_model_template_manager_methods(self):
        """Test that manager methods are properly generated."""
        result = templates.ModelTemplates.model_template("Product")
        
        # Check manager methods
        self.assertIn("def get_active(self):", result)
        self.assertIn("def get_by_id(self, product_id: str):", result)
        self.assertIn("return self.filter(deleted_at__isnull=True)", result)
        self.assertIn("product = self.get(id=product_id)", result)

    def test_factory_template_basic(self):
        """Test basic factory template generation."""
        result = templates.ModelTemplates.factory_template("UserFactory", "User", "users")
        
        # Check that the template contains expected elements
        self.assertIn("class UserFactoryFactory(factory.django.DjangoModelFactory):", result)
        self.assertIn("class Meta:", result)
        self.assertIn("model = User", result)
        self.assertIn("from users.models import User", result)
        self.assertIn("created_at = factory.LazyFunction(timezone.now)", result)
        self.assertIn("deleted_at = None", result)

    def test_factory_template_with_complex_name(self):
        """Test factory template with complex names."""
        result = templates.ModelTemplates.factory_template("ProductCategoryFactory", "ProductCategory", "products")
        
        # Check that the template contains expected elements
        self.assertIn("class ProductCategoryFactoryFactory(factory.django.DjangoModelFactory):", result)
        self.assertIn("model = ProductCategory", result)
        self.assertIn("from products.models import ProductCategory", result)

    def test_model_test_template_basic(self):
        """Test basic model test template generation."""
        result = templates.ModelTemplates.model_test_template("User", "users")
        
        # Check that the template contains expected elements
        self.assertIn("class UserModelTest(TestCase):", result)
        self.assertIn("class UserManagerTest(TestCase):", result)
        self.assertIn("from users.models import User", result)
        self.assertIn("cls.user = User.objects.create()", result)
        self.assertIn("def test_user_creation(self):", result)
        self.assertIn("def test_user_str(self):", result)
        self.assertIn("def test_user_soft_delete(self):", result)

    def test_model_test_template_manager_tests(self):
        """Test that manager tests are properly generated."""
        result = templates.ModelTemplates.model_test_template("Product", "products")
        
        # Check manager test methods
        self.assertIn("def test_manager_get_active(self):", result)
        self.assertIn("def test_manager_get_by_id_success(self):", result)
        self.assertIn("def test_manager_get_by_id_not_found(self):", result)
        self.assertIn("active_products = Product.objects.get_active()", result)
        self.assertIn("retrieved_product = Product.objects.get_by_id(self.product.id)", result)

    def test_model_test_template_with_complex_name(self):
        """Test model test template with complex model name."""
        result = templates.ModelTemplates.model_test_template("OrderItem", "orders")
        
        # Check that the template contains expected elements
        self.assertIn("class OrderItemModelTest(TestCase):", result)
        self.assertIn("class OrderItemManagerTest(TestCase):", result)
        self.assertIn("cls.orderitem = OrderItem.objects.create()", result)
        self.assertIn("def test_orderitem_creation(self):", result) 