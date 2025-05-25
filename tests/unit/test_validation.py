#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests cho các hàm validation.
"""

import unittest
import sys
import os
import io
from unittest.mock import patch

# Thêm thư mục gốc vào đường dẫn để import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.invoicemanager.utils.validation import validate_positive_number, validate_required_field

class TestValidation(unittest.TestCase):
    """Kiểm thử cho các hàm validation."""
    
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_validate_positive_number_valid(self, mock_stdout):
        """Kiểm tra validate_positive_number với giá trị hợp lệ."""
        # Kiểm tra số dương - phải trả về True
        self.assertTrue(validate_positive_number(10.5, "Đơn giá"))
        self.assertTrue(validate_positive_number(0, "Đơn giá"))  # 0 là hợp lệ (không âm)
        self.assertEqual(mock_stdout.getvalue(), "")  # Không in ra lỗi
    
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_validate_positive_number_invalid(self, mock_stdout):
        """Kiểm tra validate_positive_number với giá trị không hợp lệ."""
        # Kiểm tra số âm - phải trả về False
        self.assertFalse(validate_positive_number(-10.5, "Đơn giá"))
        self.assertIn("Lỗi: Đơn giá không được âm", mock_stdout.getvalue())
    
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_validate_required_field_valid(self, mock_stdout):
        """Kiểm tra validate_required_field với giá trị hợp lệ."""
        # Kiểm tra các giá trị không rỗng - phải trả về True
        self.assertTrue(validate_required_field("Test", "Tên sản phẩm"))
        self.assertTrue(validate_required_field(123, "Mã sản phẩm"))
        self.assertTrue(validate_required_field([1, 2, 3], "Danh sách"))
        self.assertEqual(mock_stdout.getvalue(), "")  # Không in ra lỗi
    
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_validate_required_field_invalid(self, mock_stdout):
        """Kiểm tra validate_required_field với giá trị không hợp lệ."""
        # Kiểm tra các giá trị rỗng - phải trả về False
        self.assertFalse(validate_required_field("", "Tên sản phẩm"))
        self.assertFalse(validate_required_field(None, "Mã sản phẩm"))
        self.assertFalse(validate_required_field([], "Danh sách"))
        self.assertFalse(validate_required_field(0, "Số lượng"))  # 0 được coi là giá trị rỗng
        self.assertIn("Lỗi: Tên sản phẩm là bắt buộc", mock_stdout.getvalue())
        self.assertIn("Lỗi: Mã sản phẩm là bắt buộc", mock_stdout.getvalue())
        self.assertIn("Lỗi: Danh sách là bắt buộc", mock_stdout.getvalue())
        self.assertIn("Lỗi: Số lượng là bắt buộc", mock_stdout.getvalue())


if __name__ == "__main__":
    unittest.main() 