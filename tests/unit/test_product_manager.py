#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comprehensive tests for ProductManager.
"""

import pytest
import sys
import os
import io
from unittest.mock import patch

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from core.product_manager import ProductManager
from models import Product
from tests.test_helpers import TestAssertions

class TestProductManager:
    """Tests for ProductManager."""

    def test_add_product_valid(self, product_manager):
        """Test adding a valid product."""
        product_data = {
            'product_id': 'P001',
            'name': 'Test Product',
            'unit_price': 100.0,
            'calculation_unit': 'chiếc',
            'category': 'Test'
        }

        success, message = product_manager.add_product(**product_data)

        assert success
        assert "thành công" in message
        assert len(product_manager.products) == 1

        added_product = product_manager.find_product('P001')
        assert added_product is not None
        TestAssertions.assert_product_equal(added_product, product_data)
    
    def test_add_product_with_defaults(self, product_manager):
        """Test adding a product with default values."""
        success, message = product_manager.add_product(
            product_id='P002',
            name='Product with Defaults',
            unit_price=200.0
        )

        assert success
        assert "thành công" in message

        product = product_manager.find_product('P002')
        assert product.calculation_unit == 'đơn vị'
        assert product.category == 'General'

    def test_add_product_empty_id(self, product_manager):
        """Test adding product with empty ID."""
        success, message = product_manager.add_product(
            product_id='',
            name='Valid Name',
            unit_price=100.0
        )

        assert not success
        assert "Mã sản phẩm" in message
        assert len(product_manager.products) == 0
    
    def test_add_product_empty_name(self, product_manager):
        """Test adding product with empty name."""
        success, message = product_manager.add_product(
            product_id='P003',
            name='',
            unit_price=100.0
        )

        assert not success
        assert "Tên sản phẩm" in message
        assert len(product_manager.products) == 0

    def test_add_product_negative_price(self, product_manager):
        """Test adding product with negative price."""
        success, message = product_manager.add_product(
            product_id='P004',
            name='Negative Price Product',
            unit_price=-50.0
        )

        assert not success
        assert "Đơn giá" in message and "lớn hơn 0" in message
        assert len(product_manager.products) == 0

