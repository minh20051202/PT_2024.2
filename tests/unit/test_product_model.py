#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comprehensive tests for Product model.
"""

import pytest
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from models import Product


class TestProductModel:
    """Tests for Product model."""

    def test_product_creation_valid(self):
        """Test creating Product with valid data."""
        product = Product(
            product_id="P001",
            name="Laptop Dell XPS 13",
            unit_price=25000000.0,
            calculation_unit="chiếc",
            category="Electronics"
        )

        assert product.product_id == "P001"
        assert product.name == "Laptop Dell XPS 13"
        assert product.unit_price == 25000000.0
        assert product.calculation_unit == "chiếc"
        assert product.category == "Electronics"

    def test_product_creation_with_defaults(self):
        """Test creating Product with default values."""
        product = Product(
            product_id="P002",
            name="Chuột không dây",
            unit_price=500000.0
        )

        assert product.product_id == "P002"
        assert product.name == "Chuột không dây"
        assert product.unit_price == 500000.0
        assert product.calculation_unit == "đơn vị"  # Default value
        assert product.category == "General"  # Default value

    def test_product_creation_minimal(self):
        """Test creating Product with minimal required data."""
        product = Product(
            product_id="P003",
            name="Test Product",
            unit_price=100.0
        )

        assert product.product_id == "P003"
        assert product.name == "Test Product"
        assert product.unit_price == 100.0

    def test_product_zero_price(self):
        """Test creating Product with zero price (should be allowed)."""
        product = Product(
            product_id="P004",
            name="Free Product",
            unit_price=0.0
        )

        assert product.unit_price == 0.0

    def test_product_empty_id_validation(self):
        """Test validation when product_id is empty."""
        with pytest.raises(ValueError, match="Mã sản phẩm và tên không được để trống"):
            Product(
                product_id="",
                name="Valid Name",
                unit_price=100.0
            )

    def test_product_none_id_validation(self):
        """Test validation when product_id is None."""
        with pytest.raises(ValueError, match="Mã sản phẩm và tên không được để trống"):
            Product(
                product_id=None,
                name="Valid Name",
                unit_price=100.0
            )

    def test_product_empty_name_validation(self):
        """Test validation when name is empty."""
        with pytest.raises(ValueError, match="Mã sản phẩm và tên không được để trống"):
            Product(
                product_id="P005",
                name="",
                unit_price=100.0
            )

    def test_product_none_name_validation(self):
        """Test validation when name is None."""
        with pytest.raises(ValueError, match="Mã sản phẩm và tên không được để trống"):
            Product(
                product_id="P006",
                name=None,
                unit_price=100.0
            )

    def test_product_negative_price_validation(self):
        """Test validation when unit_price is negative."""
        with pytest.raises(ValueError, match="Đơn giá không được âm"):
            Product(
                product_id="P007",
                name="Negative Price Product",
                unit_price=-50.0
            )