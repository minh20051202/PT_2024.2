#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kiểm tra toàn diện cho model Product.

Module kiểm thử này bao gồm các test cases cho dataclass Product:
- Kiểm tra tạo Product với dữ liệu hợp lệ
- Kiểm tra các giá trị mặc định
- Kiểm tra validation logic trong __post_init__
- Kiểm tra xử lý các giá trị biên và ngoại lệ
- Kiểm tra các thuộc tính và phương thức của Product
"""

import pytest
import sys
import os

# Thêm src vào path để import
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from models import Product


class TestProductModel:
    """Kiểm tra cho model Product."""

    def test_product_creation_valid(self):
        """Kiểm tra tạo Product với dữ liệu hợp lệ."""
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
        """Kiểm tra tạo Product với các giá trị mặc định."""
        product = Product(
            product_id="P002",
            name="Chuột không dây",
            unit_price=500000.0
        )

        assert product.product_id == "P002"
        assert product.name == "Chuột không dây"
        assert product.unit_price == 500000.0
        assert product.calculation_unit == "đơn vị"  # Giá trị mặc định
        assert product.category == "General"  # Giá trị mặc định

    def test_product_creation_minimal(self):
        """Kiểm tra tạo Product với dữ liệu tối thiểu cần thiết."""
        product = Product(
            product_id="P003",
            name="Test Product",
            unit_price=100.0
        )

        assert product.product_id == "P003"
        assert product.name == "Test Product"
        assert product.unit_price == 100.0

    def test_product_zero_price(self):
        """Kiểm tra tạo Product với giá bằng không (nên được cho phép)."""
        product = Product(
            product_id="P004",
            name="Free Product",
            unit_price=0.0
        )

        assert product.unit_price == 0.0

    def test_product_empty_id_validation(self):
        """Kiểm tra validation khi product_id rỗng."""
        with pytest.raises(ValueError, match="Mã sản phẩm và tên không được để trống"):
            Product(
                product_id="",
                name="Valid Name",
                unit_price=100.0
            )

    def test_product_none_id_validation(self):
        """Kiểm tra validation khi product_id là None."""
        with pytest.raises(ValueError, match="Mã sản phẩm và tên không được để trống"):
            Product(
                product_id=None,
                name="Valid Name",
                unit_price=100.0
            )

    def test_product_empty_name_validation(self):
        """Kiểm tra validation khi name rỗng."""
        with pytest.raises(ValueError, match="Mã sản phẩm và tên không được để trống"):
            Product(
                product_id="P005",
                name="",
                unit_price=100.0
            )

    def test_product_none_name_validation(self):
        """Kiểm tra validation khi name là None."""
        with pytest.raises(ValueError, match="Mã sản phẩm và tên không được để trống"):
            Product(
                product_id="P006",
                name=None,
                unit_price=100.0
            )

    def test_product_negative_price_validation(self):
        """Kiểm tra validation khi unit_price âm."""
        with pytest.raises(ValueError, match="Đơn giá không được âm"):
            Product(
                product_id="P007",
                name="Negative Price Product",
                unit_price=-50.0
            )