#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pytest configuration and shared fixtures for the invoice management system.

This file provides pytest fixtures that are automatically available to all tests.
Fixtures handle test setup, teardown, and provide common test dependencies like
temporary databases and pre-configured manager instances.
"""

import pytest
import tempfile
import os
import sys
from unittest.mock import patch

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.product_manager import ProductManager
from core.invoice_manager import InvoiceManager
from database.database import initialize_database


@pytest.fixture
def temp_db():
    """Create a temporary database for testing."""
    temp_db_fd, temp_db_path = tempfile.mkstemp(suffix='.db')
    os.close(temp_db_fd)

    # Initialize the test database
    with patch('database.database.DATABASE_PATH', temp_db_path):
        with patch('utils.db_utils.DATABASE_PATH', temp_db_path):
            success, message = initialize_database()
            assert success, f"Failed to initialize test database: {message}"

            yield temp_db_path

    # Clean up
    if os.path.exists(temp_db_path):
        os.unlink(temp_db_path)


@pytest.fixture
def product_manager(temp_db):
    """Create a ProductManager instance with temporary database."""
    with patch('database.database.DATABASE_PATH', temp_db):
        with patch('utils.db_utils.DATABASE_PATH', temp_db):
            return ProductManager()


@pytest.fixture
def populated_product_manager(product_manager):
    """ProductManager with sample products already added."""
    sample_products = [
        {
            'product_id': 'P001',
            'name': 'Laptop Dell XPS 13',
            'unit_price': 25000000.0,
            'calculation_unit': 'chiếc',
            'category': 'Electronics'
        },
        {
            'product_id': 'P002',
            'name': 'Chuột không dây Logitech',
            'unit_price': 500000.0,
            'calculation_unit': 'chiếc',
            'category': 'Electronics'
        }
    ]

    for product_data in sample_products:
        success, message = product_manager.add_product(**product_data)
        assert success, f"Failed to add product: {message}"
    return product_manager
