#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests cho ProductManager.
"""

import unittest
import sys
import os
import io
from unittest.mock import patch, MagicMock

# Thêm thư mục gốc vào đường dẫn để import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.invoicemanager.core.product_manager import ProductManager
from src.invoicemanager.models.product import Product

class TestProductManager(unittest.TestCase):
    """Kiểm thử cho ProductManager."""
    
    def setUp(self):
        """Thiết lập cho mỗi bài kiểm tra."""
        # Tạo một mock cho FileManager
        self.file_manager_patcher = patch('src.invoicemanager.core.product_manager.FileManager')
        self.mock_file_manager = self.file_manager_patcher.start().return_value
        
        # Đặt giá trị trả về cho phương thức load_products
        self.mock_file_manager.load_products.return_value = []
        
        # Khởi tạo ProductManager với mock file manager
        self.product_manager = ProductManager()
    
    def tearDown(self):
        """Dọn dẹp sau mỗi bài kiểm tra."""
        self.file_manager_patcher.stop()
    
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_add_product_valid(self, mock_stdout):
        """Kiểm tra thêm sản phẩm hợp lệ."""
        # Thêm sản phẩm hợp lệ
        result = self.product_manager.add_product(
            product_id="P001",
            name="Sản phẩm thử nghiệm",
            unit_price=100.0,
            calculation_unit="đơn vị",
            category="Kiểm thử"
        )
        
        # Kiểm tra kết quả
        self.assertTrue(result)
        self.assertEqual(len(self.product_manager.products), 1)
        self.assertEqual(self.product_manager.products[0].product_id, "P001")
        self.assertEqual(self.product_manager.products[0].name, "Sản phẩm thử nghiệm")
        
        # Kiểm tra thông báo
        self.assertIn("Đã thêm sản phẩm 'Sản phẩm thử nghiệm' thành công!", mock_stdout.getvalue())
        
        # Kiểm tra gọi save_products
        self.mock_file_manager.save_products.assert_called_once()
    
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_add_product_empty_id(self, mock_stdout):
        """Kiểm tra thêm sản phẩm với ID rỗng."""
        # Thêm sản phẩm với ID rỗng
        result = self.product_manager.add_product(
            product_id="",  # ID rỗng
            name="Sản phẩm lỗi",
            unit_price=100.0
        )
        
        # Kiểm tra kết quả
        self.assertFalse(result)
        self.assertEqual(len(self.product_manager.products), 0)
        
        # Kiểm tra thông báo
        self.assertIn("Lỗi: Mã sản phẩm là bắt buộc", mock_stdout.getvalue())
        
        # Kiểm tra không gọi save_products
        self.mock_file_manager.save_products.assert_not_called()
    
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_add_product_empty_name(self, mock_stdout):
        """Kiểm tra thêm sản phẩm với tên rỗng."""
        # Thêm sản phẩm với tên rỗng
        result = self.product_manager.add_product(
            product_id="P002",
            name="",  # Tên rỗng
            unit_price=100.0
        )
        
        # Kiểm tra kết quả
        self.assertFalse(result)
        self.assertEqual(len(self.product_manager.products), 0)
        
        # Kiểm tra thông báo
        self.assertIn("Lỗi: Tên sản phẩm là bắt buộc", mock_stdout.getvalue())
        
        # Kiểm tra không gọi save_products
        self.mock_file_manager.save_products.assert_not_called()
    
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_add_product_negative_price(self, mock_stdout):
        """Kiểm tra thêm sản phẩm với giá âm."""
        # Thêm sản phẩm với giá âm
        result = self.product_manager.add_product(
            product_id="P003",
            name="Sản phẩm giá âm",
            unit_price=-50.0  # Giá âm
        )
        
        # Kiểm tra kết quả
        self.assertFalse(result)
        self.assertEqual(len(self.product_manager.products), 0)
        
        # Kiểm tra thông báo
        self.assertIn("Lỗi: Đơn giá không được âm", mock_stdout.getvalue())
        
        # Kiểm tra không gọi save_products
        self.mock_file_manager.save_products.assert_not_called()
    
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_add_product_duplicate_id(self, mock_stdout):
        """Kiểm tra thêm sản phẩm với ID trùng lặp."""
        # Thêm sản phẩm đầu tiên
        self.product_manager.products = [
            Product(product_id="P001", name="Sản phẩm hiện có", unit_price=100.0)
        ]
        
        # Thêm sản phẩm với ID trùng lặp
        result = self.product_manager.add_product(
            product_id="P001",  # ID trùng lặp
            name="Sản phẩm mới",
            unit_price=200.0
        )
        
        # Kiểm tra kết quả
        self.assertFalse(result)
        self.assertEqual(len(self.product_manager.products), 1)
        self.assertEqual(self.product_manager.products[0].name, "Sản phẩm hiện có")
        
        # Kiểm tra thông báo
        self.assertIn("Sản phẩm với Mã 'P001' đã tồn tại!", mock_stdout.getvalue())
        
        # Kiểm tra không gọi save_products
        self.mock_file_manager.save_products.assert_not_called()
    
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_update_product_valid(self, mock_stdout):
        """Kiểm tra cập nhật sản phẩm hợp lệ."""
        # Tạo sản phẩm hiện có
        self.product_manager.products = [
            Product(product_id="P001", name="Sản phẩm cũ", unit_price=100.0)
        ]
        
        # Cập nhật sản phẩm
        result = self.product_manager.update_product(
            product_id="P001",
            name="Sản phẩm mới",
            unit_price=200.0,
            calculation_unit="cái",
            category="Danh mục mới"
        )
        
        # Kiểm tra kết quả
        self.assertTrue(result)
        self.assertEqual(self.product_manager.products[0].name, "Sản phẩm mới")
        self.assertEqual(self.product_manager.products[0].unit_price, 200.0)
        self.assertEqual(self.product_manager.products[0].calculation_unit, "cái")
        self.assertEqual(self.product_manager.products[0].category, "Danh mục mới")
        
        # Kiểm tra thông báo
        self.assertIn("Đã cập nhật sản phẩm 'P001' thành công!", mock_stdout.getvalue())
        
        # Kiểm tra gọi save_products
        self.mock_file_manager.save_products.assert_called_once()
    
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_update_product_not_found(self, mock_stdout):
        """Kiểm tra cập nhật sản phẩm không tồn tại."""
        # Không có sản phẩm nào
        self.product_manager.products = []
        
        # Cập nhật sản phẩm không tồn tại
        result = self.product_manager.update_product(
            product_id="P001",
            name="Sản phẩm mới"
        )
        
        # Kiểm tra kết quả
        self.assertFalse(result)
        
        # Kiểm tra thông báo
        self.assertIn("Không tìm thấy sản phẩm với Mã 'P001'!", mock_stdout.getvalue())
        
        # Kiểm tra không gọi save_products
        self.mock_file_manager.save_products.assert_not_called()
    
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_update_product_negative_price(self, mock_stdout):
        """Kiểm tra cập nhật sản phẩm với giá âm."""
        # Tạo sản phẩm hiện có
        self.product_manager.products = [
            Product(product_id="P001", name="Sản phẩm cũ", unit_price=100.0)
        ]
        
        # Cập nhật sản phẩm với giá âm
        result = self.product_manager.update_product(
            product_id="P001",
            unit_price=-50.0  # Giá âm
        )
        
        # Kiểm tra kết quả
        self.assertFalse(result)
        self.assertEqual(self.product_manager.products[0].unit_price, 100.0)  # Giá không thay đổi
        
        # Kiểm tra thông báo
        self.assertIn("Lỗi: Đơn giá không được âm", mock_stdout.getvalue())
        
        # Kiểm tra không gọi save_products
        self.mock_file_manager.save_products.assert_not_called()
    
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_delete_product_valid(self, mock_stdout):
        """Kiểm tra xóa sản phẩm hợp lệ."""
        # Tạo sản phẩm hiện có
        self.product_manager.products = [
            Product(product_id="P001", name="Sản phẩm 1", unit_price=100.0),
            Product(product_id="P002", name="Sản phẩm 2", unit_price=200.0)
        ]
        
        # Xóa sản phẩm
        result = self.product_manager.delete_product("P001")
        
        # Kiểm tra kết quả
        self.assertTrue(result)
        self.assertEqual(len(self.product_manager.products), 1)
        self.assertEqual(self.product_manager.products[0].product_id, "P002")
        
        # Kiểm tra thông báo
        self.assertIn("Đã xóa sản phẩm 'P001' thành công!", mock_stdout.getvalue())
        
        # Kiểm tra gọi save_products
        self.mock_file_manager.save_products.assert_called_once()
    
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_delete_product_not_found(self, mock_stdout):
        """Kiểm tra xóa sản phẩm không tồn tại."""
        # Không có sản phẩm nào
        self.product_manager.products = []
        
        # Xóa sản phẩm không tồn tại
        result = self.product_manager.delete_product("P001")
        
        # Kiểm tra kết quả
        self.assertFalse(result)
        
        # Kiểm tra thông báo
        self.assertIn("Không tìm thấy sản phẩm với Mã 'P001'!", mock_stdout.getvalue())
        
        # Kiểm tra không gọi save_products
        self.mock_file_manager.save_products.assert_not_called()
    
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_find_product(self, mock_stdout):
        """Kiểm tra tìm sản phẩm."""
        # Tạo sản phẩm hiện có
        product1 = Product(product_id="P001", name="Sản phẩm 1", unit_price=100.0)
        product2 = Product(product_id="P002", name="Sản phẩm 2", unit_price=200.0)
        self.product_manager.products = [product1, product2]
        
        # Tìm sản phẩm tồn tại
        found_product = self.product_manager.find_product("P001")
        
        # Kiểm tra kết quả
        self.assertEqual(found_product, product1)
        
        # Tìm sản phẩm không tồn tại
        not_found_product = self.product_manager.find_product("P003")
        
        # Kiểm tra kết quả
        self.assertIsNone(not_found_product)


if __name__ == "__main__":
    unittest.main() 