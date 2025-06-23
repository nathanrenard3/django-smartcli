from django.test import TestCase

from smartcli import config


class TemplateConfigsTest(TestCase):
    """Test template configurations."""

    def test_template_configs_keys(self):
        """Test that TEMPLATE_CONFIGS contains all expected keys."""
        expected_keys = ["model", "serializer", "service", "factory"]
        
        for key in expected_keys:
            with self.subTest(key=key):
                self.assertIn(key, config.TEMPLATE_CONFIGS)

    def test_template_configs_are_dicts(self):
        """Test that all template configs are dictionaries."""
        for template_config in config.TEMPLATE_CONFIGS.values():
            with self.subTest(template_config=template_config):
                self.assertIsInstance(template_config, dict)

    def test_model_template_config(self):
        """Test model template configuration."""
        model_config = config.TEMPLATE_CONFIGS["model"]
        
        # Check expected keys
        self.assertIn("base_fields", model_config)
        self.assertIn("read_only_fields", model_config)
        self.assertIn("manager_methods", model_config)
        
        # Check values
        expected_base_fields = ["id", "created_at", "deleted_at"]
        expected_read_only_fields = ["id", "created_at"]
        expected_manager_methods = ["get_active", "get_by_id"]
        
        self.assertEqual(model_config["base_fields"], expected_base_fields)
        self.assertEqual(model_config["read_only_fields"], expected_read_only_fields)
        self.assertEqual(model_config["manager_methods"], expected_manager_methods)

    def test_serializer_template_config(self):
        """Test serializer template configuration."""
        serializer_config = config.TEMPLATE_CONFIGS["serializer"]
        
        # Check expected keys
        self.assertIn("base_fields", serializer_config)
        self.assertIn("read_only_fields", serializer_config)
        
        # Check values
        expected_base_fields = ["id", "created_at", "deleted_at"]
        expected_read_only_fields = ["id", "created_at"]
        
        self.assertEqual(serializer_config["base_fields"], expected_base_fields)
        self.assertEqual(serializer_config["read_only_fields"], expected_read_only_fields)

    def test_service_template_config(self):
        """Test service template configuration."""
        service_config = config.TEMPLATE_CONFIGS["service"]
        
        # Check expected keys
        self.assertIn("base_methods", service_config)
        self.assertIn("decorators", service_config)
        
        # Check values
        expected_base_methods = ["create"]
        expected_decorators = ["@classmethod", "@transaction.atomic"]
        
        self.assertEqual(service_config["base_methods"], expected_base_methods)
        self.assertEqual(service_config["decorators"], expected_decorators)

    def test_factory_template_config(self):
        """Test factory template configuration."""
        factory_config = config.TEMPLATE_CONFIGS["factory"]
        
        # Check expected keys
        self.assertIn("base_fields", factory_config)
        
        # Check values
        expected_base_fields = ["created_at", "deleted_at"]
        
        self.assertEqual(factory_config["base_fields"], expected_base_fields)

    def test_model_base_fields_are_strings(self):
        """Test that model base fields are strings."""
        model_config = config.TEMPLATE_CONFIGS["model"]
        for field in model_config["base_fields"]:
            with self.subTest(field=field):
                self.assertIsInstance(field, str)

    def test_model_read_only_fields_are_strings(self):
        """Test that model read-only fields are strings."""
        model_config = config.TEMPLATE_CONFIGS["model"]
        for field in model_config["read_only_fields"]:
            with self.subTest(field=field):
                self.assertIsInstance(field, str)

    def test_model_manager_methods_are_strings(self):
        """Test that model manager methods are strings."""
        model_config = config.TEMPLATE_CONFIGS["model"]
        for method in model_config["manager_methods"]:
            with self.subTest(method=method):
                self.assertIsInstance(method, str)

    def test_serializer_base_fields_are_strings(self):
        """Test that serializer base fields are strings."""
        serializer_config = config.TEMPLATE_CONFIGS["serializer"]
        for field in serializer_config["base_fields"]:
            with self.subTest(field=field):
                self.assertIsInstance(field, str)

    def test_serializer_read_only_fields_are_strings(self):
        """Test that serializer read-only fields are strings."""
        serializer_config = config.TEMPLATE_CONFIGS["serializer"]
        for field in serializer_config["read_only_fields"]:
            with self.subTest(field=field):
                self.assertIsInstance(field, str)

    def test_service_base_methods_are_strings(self):
        """Test that service base methods are strings."""
        service_config = config.TEMPLATE_CONFIGS["service"]
        for method in service_config["base_methods"]:
            with self.subTest(method=method):
                self.assertIsInstance(method, str)

    def test_service_decorators_are_strings(self):
        """Test that service decorators are strings."""
        service_config = config.TEMPLATE_CONFIGS["service"]
        for decorator in service_config["decorators"]:
            with self.subTest(decorator=decorator):
                self.assertIsInstance(decorator, str)

    def test_factory_base_fields_are_strings(self):
        """Test that factory base fields are strings."""
        factory_config = config.TEMPLATE_CONFIGS["factory"]
        for field in factory_config["base_fields"]:
            with self.subTest(field=field):
                self.assertIsInstance(field, str)

    def test_model_base_fields_no_duplicates(self):
        """Test that model base fields have no duplicates."""
        model_config = config.TEMPLATE_CONFIGS["model"]
        base_fields = model_config["base_fields"]
        self.assertEqual(len(base_fields), len(set(base_fields)))

    def test_model_read_only_fields_no_duplicates(self):
        """Test that model read-only fields have no duplicates."""
        model_config = config.TEMPLATE_CONFIGS["model"]
        read_only_fields = model_config["read_only_fields"]
        self.assertEqual(len(read_only_fields), len(set(read_only_fields)))

    def test_model_manager_methods_no_duplicates(self):
        """Test that model manager methods have no duplicates."""
        model_config = config.TEMPLATE_CONFIGS["model"]
        manager_methods = model_config["manager_methods"]
        self.assertEqual(len(manager_methods), len(set(manager_methods)))

    def test_serializer_base_fields_no_duplicates(self):
        """Test that serializer base fields have no duplicates."""
        serializer_config = config.TEMPLATE_CONFIGS["serializer"]
        base_fields = serializer_config["base_fields"]
        self.assertEqual(len(base_fields), len(set(base_fields)))

    def test_serializer_read_only_fields_no_duplicates(self):
        """Test that serializer read-only fields have no duplicates."""
        serializer_config = config.TEMPLATE_CONFIGS["serializer"]
        read_only_fields = serializer_config["read_only_fields"]
        self.assertEqual(len(read_only_fields), len(set(read_only_fields)))

    def test_service_base_methods_no_duplicates(self):
        """Test that service base methods have no duplicates."""
        service_config = config.TEMPLATE_CONFIGS["service"]
        base_methods = service_config["base_methods"]
        self.assertEqual(len(base_methods), len(set(base_methods)))

    def test_service_decorators_no_duplicates(self):
        """Test that service decorators have no duplicates."""
        service_config = config.TEMPLATE_CONFIGS["service"]
        decorators = service_config["decorators"]
        self.assertEqual(len(decorators), len(set(decorators)))

    def test_factory_base_fields_no_duplicates(self):
        """Test that factory base fields have no duplicates."""
        factory_config = config.TEMPLATE_CONFIGS["factory"]
        base_fields = factory_config["base_fields"]
        self.assertEqual(len(base_fields), len(set(base_fields)))

    def test_model_read_only_fields_subset_of_base_fields(self):
        """Test that model read-only fields are a subset of base fields."""
        model_config = config.TEMPLATE_CONFIGS["model"]
        base_fields = set(model_config["base_fields"])
        read_only_fields = set(model_config["read_only_fields"])
        self.assertTrue(read_only_fields.issubset(base_fields))

    def test_serializer_read_only_fields_subset_of_base_fields(self):
        """Test that serializer read-only fields are a subset of base fields."""
        serializer_config = config.TEMPLATE_CONFIGS["serializer"]
        base_fields = set(serializer_config["base_fields"])
        read_only_fields = set(serializer_config["read_only_fields"])
        self.assertTrue(read_only_fields.issubset(base_fields))

    def test_service_decorators_contain_at_symbol(self):
        """Test that service decorators contain @ symbol."""
        service_config = config.TEMPLATE_CONFIGS["service"]
        for decorator in service_config["decorators"]:
            with self.subTest(decorator=decorator):
                self.assertIn("@", decorator) 