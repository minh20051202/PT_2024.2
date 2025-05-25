#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests cho mô hình Product.
"""

import unittest
import sys
import os

# Thêm thư mục gốc vào đường dẫn để import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.invoicemanager.models.product import Product

class TestProductModel(unittest.TestCase):
    """Kiểm thử cho mô hình Product."""
    
    def test_product_creation_valid(self):
        """Kiểm tra tạo Product với dữ liệu hợp lệ."""
        # Tạo sản phẩm với dữ liệu hợp lệ
        product = Product(
            product_id="P001",
            name="Sản phẩm thử nghiệm",
            unit_price=100.0,
            category="Kiểm thử",
            calculation_unit="đơn vị"
        )
        
        # Kiểm tra các thuộc tính
        self.assertEqual(product.product_id, "P001")
        self.assertEqual(product.name, "Sản phẩm thử nghiệm")
        self.assertEqual(product.unit_price, 100.0)
        self.assertEqual(product.category, "Kiểm thử")
        self.assertEqual(product.calculation_unit, "đơn vị")
    
    def test_product_creation_with_defaults(self):
        """Kiểm tra tạo Product với giá trị mặc định."""
        # Tạo sản phẩm với chỉ các trường bắt buộc
        product = Product(
            product_id="P002",
            name="Sản phẩm thử nghiệm 2",
            unit_price=200.0
        )
        
        # Kiểm tra các thuộc tính mặc định
        self.assertEqual(product.product_id, "P002")
        self.assertEqual(product.name, "Sản phẩm thử nghiệm 2")
        self.assertEqual(product.unit_price, 200.0)
        self.assertEqual(product.category, "General")  # Giá trị mặc định
        self.assertEqual(product.calculation_unit, "đơn vị")  # Giá trị mặc định
    
    def test_product_empty_id(self):
        """Kiểm tra validation khi product_id rỗng."""
        # Sản phẩm với ID rỗng phải gây ra lỗi
        with self.assertRaises(ValueError) as context:
            Product(
                product_id="",  # ID rỗng
                name="Sản phẩm lỗi",
                unit_price=100.0
            )
        self.assertIn("Mã sản phẩm và tên không được để trống", str(context.exception))
    
    def test_product_empty_name(self):
        """Kiểm tra validation khi name rỗng."""
        # Sản phẩm với tên rỗng phải gây ra lỗi
        with self.assertRaises(ValueError) as context:
            Product(
                product_id="P003",
                name="",  # Tên rỗng
                unit_price=100.0
            )
        self.assertIn("Mã sản phẩm và tên không được để trống", str(context.exception))
    
    def test_product_negative_price(self):
        """Kiểm tra validation khi unit_price âm."""
        # Sản phẩm với đơn giá âm phải gây ra lỗi
        with self.assertRaises(ValueError) as context:
            Product(
                product_id="P004",
                name="Sản phẩm giá âm",
                unit_price=-50.0  # Đơn giá âm
            )
        self.assertIn("Đơn giá không được âm", str(context.exception))


if __name__ == "__main__":
    unittest.main() 