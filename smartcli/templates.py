"""
Templates for Django SmartCLI commands.

This module contains all the template strings used by the generator commands.
"""


class ModelTemplates:
    """Templates for model generation."""
    
    @staticmethod
    def model_template(model_name: str) -> str:
        """Generate model template."""
        return f'''import uuid

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils import timezone


class {model_name}Manager(models.Manager):
    """
    Custom manager for the {model_name} model.
    Contains specific query methods for the model.
    """

    def get_active(self):
        """
        Get all {model_name.lower()}s that are not deleted.
        """
        return self.filter(deleted_at__isnull=True)

    def get_by_id(self, {model_name.lower()}_id: str):
        """
        Get a {model_name.lower()} by its ID.

        Args:
            {model_name.lower()}_id: The ID of the {model_name.lower()} to get
        """
        try:
            {model_name.lower()} = self.get(id={model_name.lower()}_id)
        except self.model.DoesNotExist:
            raise ObjectDoesNotExist("{model_name} not found")
        return {model_name.lower()}


class {model_name}(models.Model):
    """
    {model_name} model description.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Timestamps
    created_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    objects = {model_name}Manager()
'''

    @staticmethod
    def factory_template(factory_name: str, model_name: str, app_name: str) -> str:
        """Generate factory template."""
        return f'''import factory
from django.utils import timezone

from {app_name}.models import {model_name}


class {factory_name}Factory(factory.django.DjangoModelFactory):
    """
    Factory for creating test instances of {model_name}.
    """
    class Meta:
        model = {model_name}

    created_at = factory.LazyFunction(timezone.now)
    deleted_at = None
''' 

    @staticmethod
    def model_test_template(model_name: str, app_name: str) -> str:
        """Generate model test template."""
        return f'''from django.db import models
from django.db.utils import IntegrityError
from django.utils import timezone

from {app_name}.models import {model_name}
from rest_framework.test import TestCase


class {model_name}ModelTest(TestCase):
    """Tests for the {model_name} model."""

    @classmethod
    def setUpTestData(cls):
        """Set up test data shared across all test methods."""
        super().setUpTestData()
        cls.{model_name.lower()} = {model_name}.objects.create()

    def test_{model_name.lower()}_creation(self):
        """Test that a {model_name.lower()} can be created with valid data."""
        self.assertIsInstance(self.{model_name.lower()}, {model_name})
        self.assertIsNotNone(self.{model_name.lower()}.id)
        self.assertIsNotNone(self.{model_name.lower()}.created_at)

    def test_{model_name.lower()}_str(self):
        """Test the string representation of a {model_name.lower()}."""
        expected_str = str(self.{model_name.lower()}.id)
        self.assertEqual(str(self.{model_name.lower()}), expected_str)

    def test_{model_name.lower()}_soft_delete(self):
        """Test soft deletion functionality."""
        self.assertIsNone(self.{model_name.lower()}.deleted_at)
        self.{model_name.lower()}.deleted_at = timezone.now()
        self.{model_name.lower()}.save()
        self.assertIsNotNone(self.{model_name.lower()}.deleted_at)

    def test_{model_name.lower()}_manager_get_active(self):
        """Test the get_active manager method."""
        # Create a deleted {model_name.lower()}
        deleted_{model_name.lower()} = {model_name}.objects.create()
        deleted_{model_name.lower()}.deleted_at = timezone.now()
        deleted_{model_name.lower()}.save()

        # Get active {model_name.lower()}s
        active_{model_name.lower()}s = {model_name}.objects.get_active()
        
        # Should include the original {model_name.lower()} but not the deleted one
        self.assertIn(self.{model_name.lower()}, active_{model_name.lower()}s)
        self.assertNotIn(deleted_{model_name.lower()}, active_{model_name.lower()}s)

    def test_{model_name.lower()}_manager_get_by_id(self):
        """Test the get_by_id manager method."""
        # Test getting existing {model_name.lower()}
        retrieved_{model_name.lower()} = {model_name}.objects.get_by_id(self.{model_name.lower()}.id)
        self.assertEqual(retrieved_{model_name.lower()}, self.{model_name.lower()})

        # Test getting non-existent {model_name.lower()}
        with self.assertRaises(Exception):
            {model_name}.objects.get_by_id("non-existent-id")


class {model_name}ManagerTest(TestCase):
    """Tests for the {model_name}Manager."""

    @classmethod
    def setUpTestData(cls):
        """Set up test data shared across all test methods."""
        super().setUpTestData()
        cls.{model_name.lower()} = {model_name}.objects.create()

    def test_manager_get_active(self):
        """Test the get_active method returns active {model_name.lower()}s."""
        active_{model_name.lower()}s = {model_name}.objects.get_active()
        self.assertIn(self.{model_name.lower()}, active_{model_name.lower()}s)

    def test_manager_get_by_id_success(self):
        """Test getting a {model_name.lower()} by ID successfully."""
        retrieved_{model_name.lower()} = {model_name}.objects.get_by_id(self.{model_name.lower()}.id)
        self.assertEqual(retrieved_{model_name.lower()}, self.{model_name.lower()})

    def test_manager_get_by_id_not_found(self):
        """Test getting a {model_name.lower()} by non-existent ID."""
        with self.assertRaises(Exception):
            {model_name}.objects.get_by_id("non-existent-id")
'''


class SerializerTemplates:
    """Templates for serializer generation."""
    
    @staticmethod
    def serializer_template(serializer_name: str, model_name: str, app_name: str) -> str:
        """Generate serializer template."""
        return f'''from rest_framework import serializers

from {app_name}.models import {model_name}


class {serializer_name}Serializer(serializers.ModelSerializer):
    """
    Serializer for {model_name} model.
    """
    
    class Meta:
        model = {model_name}
        fields = [
            "id",
            "created_at",
            "deleted_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
        ]
'''

    @staticmethod
    def serializer_test_template(serializer_name: str, model_name: str, app_name: str) -> str:
        """Generate serializer test template."""
        return f'''from {app_name}.factories import {model_name}Factory
from {app_name}.models import {model_name}
from {app_name}.serializers import {serializer_name}Serializer
from rest_framework.test import TestCase


class {serializer_name}SerializerTest(TestCase):
    """Tests for the {serializer_name}Serializer."""

    @classmethod
    def setUpTestData(cls):
        """Set up test data shared across all test methods."""
        super().setUpTestData()
        cls.{model_name.lower()} = {model_name}Factory()

    def test_serializer_contains_expected_fields(self):
        """Test that the serializer contains the expected fields."""
        data = self.serializer.data
        
        expected_fields = ["id", "created_at", "deleted_at"]
        for field in expected_fields:
            self.assertIn(field, data)

    def test_serializer_read_only_fields(self):
        """Test that read-only fields are properly set."""
        read_only_fields = self.serializer.Meta.read_only_fields
        expected_read_only = ["id", "created_at"]
        
        for field in expected_read_only:
            self.assertIn(field, read_only_fields)

    def test_serializer_model_class(self):
        """Test that the serializer uses the correct model."""
        self.assertEqual(self.serializer.Meta.model, {model_name})
'''


class ServiceTemplates:
    """Templates for service generation."""
    
    @staticmethod
    def service_template(service_name: str) -> str:
        """Generate service template."""
        import re
        method_name = re.sub(r"(?<!^)(?=[A-Z])", "_", service_name).lower()
        
        return f'''from django.db import transaction

class {service_name}Service:
    """
    Service for {service_name} operations.
    """
    
    @classmethod
    @transaction.atomic
    def create_{method_name}(cls):
        """
        Create a new {service_name.lower()}.
        
        Returns:
            The created {service_name.lower()}
        """
        pass
        
    @classmethod
    @transaction.atomic
    def update_{method_name}(cls):
        """
        Update a {service_name.lower()}.
        """
        pass
        
    @classmethod
    @transaction.atomic
    def delete_{method_name}(cls):
        """
        Delete a {service_name.lower()}.
        """
        pass
'''

    @staticmethod
    def service_test_template(service_name: str, app_name: str) -> str:
        """Generate service test template."""
        import re
        method_name = re.sub(r"(?<!^)(?=[A-Z])", "_", service_name).lower()
        
        return f'''from {app_name}.services import {service_name}Service
from rest_framework.test import TestCase


class {service_name}ServiceTest(TestCase):
    """Tests for the {service_name}Service."""

    def test_create_{method_name}_success(self):
        """Test successful creation of {service_name.lower()}."""
        pass

    def test_update_{method_name}_success(self):
        """Test successful update of {service_name.lower()}."""
        pass

    def test_delete_{method_name}_success(self):
        """Test successful deletion of {service_name.lower()}."""
        pass
'''

class ViewTemplates:
    """Templates for view generation."""
    
    @staticmethod
    def view_template(view_name: str, model_name: str, app_name: str) -> str:
        """Generate view template."""
        return f'''from http import HTTPStatus

from rest_framework.permissions import IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from {app_name}.models import {model_name}
from {app_name}.serializers import {model_name}Serializer
from {app_name}.services.{model_name.lower()}_service import {model_name}Service


class {view_name}ViewSet(ViewSet):
    """ViewSet for managing {model_name.lower()} operations."""

    permission_classes = [IsAdminUser]
    serializer_class = {model_name}Serializer

    def list(self, request: Request) -> Response:
        """List active {model_name.lower()}s."""
        pass

    def retrieve(self, request: Request, pk: str) -> Response:
        """Get a {model_name.lower()} by its ID."""
        pass

    def create(self, request: Request) -> Response:
        """Create a new {model_name.lower()}."""
        pass

    def partial_update(self, request: Request, pk: str = None) -> Response:
        """Update a {model_name.lower()} with the provided data."""
        pass

    def destroy(self, request: Request, pk: str) -> Response:
        """Delete a {model_name.lower()} and all related data."""
        pass
'''

    @staticmethod
    def view_test_template(view_name: str, model_name: str, app_name: str) -> str:
        """Generate view test template."""
        return f'''from http import HTTPStatus
from unittest.mock import patch

from django.urls import reverse
from rest_framework import status
from rest_framework.test import TestCase

from {app_name}.factories import {model_name}Factory
from {app_name}.models import {model_name}


class {view_name}ViewSetTest(TestCase):
    """Tests for the {view_name}ViewSet."""

    @classmethod
    def setUpTestData(cls):
        """Set up test data shared across all test methods."""
        super().setUpTestData()

    def test_list_{model_name.lower()}s_success(self):
        """Test successful listing of {model_name.lower()}s."""
        pass

    def test_retrieve_{model_name.lower()}_success(self):
        """Test successful retrieval of a {model_name.lower()}."""
        pass

    def test_retrieve_{model_name.lower()}_not_found(self):
        """Test retrieval of a non-existent {model_name.lower()}."""
        pass

    def test_create_{model_name.lower()}_success(self):
        """Test successful creation of a {model_name.lower()}."""
        pass

    def test_partial_update_{model_name.lower()}_success(self):
        """Test successful partial update of a {model_name.lower()}."""
        pass

    def test_destroy_{model_name.lower()}_success(self):
        """Test successful deletion of a {model_name.lower()}."""
        pass
'''