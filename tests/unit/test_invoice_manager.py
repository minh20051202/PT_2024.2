#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests cho InvoiceManager.
"""

import unittest
import sys
import os
import io
from unittest.mock import patch, MagicMock

# Thêm thư mục gốc vào đường dẫn để import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.invoicemanager.core.invoice_manager import InvoiceManager
from src.invoicemanager.models.invoice import Invoice, InvoiceItem
from src.invoicemanager.models.product import Product

class TestInvoiceManager(unittest.TestCase):
    """Kiểm thử cho InvoiceManager."""
    
    def setUp(self):
        """Thiết lập cho mỗi bài kiểm tra."""
        # Tạo một mock cho FileManager và ProductManager
        self.file_manager_patcher = patch('src.invoicemanager.core.invoice_manager.FileManager')
        self.product_manager_patcher = patch('src.invoicemanager.core.invoice_manager.ProductManager')
        
        self.mock_file_manager = self.file_manager_patcher.start().return_value
        self.mock_product_manager = self.product_manager_patcher.start()
        
        # Đặt giá trị trả về cho phương thức load_invoices
        self.mock_file_manager.load_invoices.return_value = []
        
        # Khởi tạo InvoiceManager với mock managers
        self.invoice_manager = InvoiceManager(self.mock_product_manager)
    
    def tearDown(self):
        """Dọn dẹp sau mỗi bài kiểm tra."""
        self.file_manager_patcher.stop()
        self.product_manager_patcher.stop()
    
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_create_invoice_valid(self, mock_stdout):
        """Kiểm tra tạo hóa đơn hợp lệ."""
        # Thiết lập mock product_manager.find_product để trả về sản phẩm giả
        self.mock_product_manager.find_product.return_value = Product(
            product_id="P001", name="Sản phẩm thử nghiệm", unit_price=100.0
        )
        
        # Tạo hóa đơn hợp lệ
        result = self.invoice_manager.create_invoice(
            invoice_id="INV001",
            customer_name="Nguyễn Văn A",
            items_data=[
                {"product_id": "P001", "quantity": 2}
            ]
        )
        
        # Kiểm tra kết quả
        self.assertTrue(result)
        self.assertEqual(len(self.invoice_manager.invoices), 1)
        self.assertEqual(self.invoice_manager.invoices[0].invoice_id, "INV001")
        self.assertEqual(self.invoice_manager.invoices[0].customer_name, "Nguyễn Văn A")
        self.assertEqual(len(self.invoice_manager.invoices[0].items), 1)
        
        # Kiểm tra thông báo
        self.assertIn("Đã tạo hóa đơn 'INV001' thành công!", mock_stdout.getvalue())
        
        # Kiểm tra gọi save_invoices
        self.mock_file_manager.save_invoices.assert_called_once()
    
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_create_invoice_empty_id(self, mock_stdout):
        """Kiểm tra tạo hóa đơn với ID rỗng."""
        # Tạo hóa đơn với ID rỗng
        result = self.invoice_manager.create_invoice(
            invoice_id="",  # ID rỗng
            customer_name="Nguyễn Văn A",
            items_data=[
                {"product_id": "P001", "quantity": 2}
            ]
        )
        
        # Kiểm tra kết quả
        self.assertFalse(result)
        self.assertEqual(len(self.invoice_manager.invoices), 0)
        
        # Kiểm tra thông báo
        self.assertIn("Lỗi: Mã hóa đơn là bắt buộc", mock_stdout.getvalue())
        
        # Kiểm tra không gọi save_invoices
        self.mock_file_manager.save_invoices.assert_not_called()
    
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_create_invoice_empty_customer_name(self, mock_stdout):
        """Kiểm tra tạo hóa đơn với tên khách hàng rỗng."""
        # Tạo hóa đơn với tên khách hàng rỗng
        result = self.invoice_manager.create_invoice(
            invoice_id="INV001",
            customer_name="",  # Tên khách hàng rỗng
            items_data=[
                {"product_id": "P001", "quantity": 2}
            ]
        )
        
        # Kiểm tra kết quả
        self.assertFalse(result)
        self.assertEqual(len(self.invoice_manager.invoices), 0)
        
        # Kiểm tra thông báo
        self.assertIn("Lỗi: Tên khách hàng là bắt buộc", mock_stdout.getvalue())
        
        # Kiểm tra không gọi save_invoices
        self.mock_file_manager.save_invoices.assert_not_called()
    
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_create_invoice_empty_items(self, mock_stdout):
        """Kiểm tra tạo hóa đơn với danh sách mặt hàng rỗng."""
        # Tạo hóa đơn với danh sách mặt hàng rỗng
        result = self.invoice_manager.create_invoice(
            invoice_id="INV001",
            customer_name="Nguyễn Văn A",
            items_data=[]  # Danh sách mặt hàng rỗng
        )
        
        # Kiểm tra kết quả
        self.assertFalse(result)
        self.assertEqual(len(self.invoice_manager.invoices), 0)
        
        # Kiểm tra thông báo
        self.assertIn("Lỗi: Hóa đơn phải có ít nhất một mặt hàng", mock_stdout.getvalue())
        
        # Kiểm tra không gọi save_invoices
        self.mock_file_manager.save_invoices.assert_not_called()
    
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_create_invoice_duplicate_id(self, mock_stdout):
        """Kiểm tra tạo hóa đơn với ID trùng lặp."""
        # Thêm hóa đơn đầu tiên
        self.invoice_manager.invoices = [
            Invoice(invoice_id="INV001", customer_name="Khách hàng hiện có")
        ]
        
        # Tạo hóa đơn với ID trùng lặp
        result = self.invoice_manager.create_invoice(
            invoice_id="INV001",  # ID trùng lặp
            customer_name="Nguyễn Văn A",
            items_data=[
                {"product_id": "P001", "quantity": 2}
            ]
        )
        
        # Kiểm tra kết quả
        self.assertFalse(result)
        self.assertEqual(len(self.invoice_manager.invoices), 1)
        self.assertEqual(self.invoice_manager.invoices[0].customer_name, "Khách hàng hiện có")
        
        # Kiểm tra thông báo
        self.assertIn("Hóa đơn với Mã 'INV001' đã tồn tại!", mock_stdout.getvalue())
        
        # Kiểm tra không gọi save_invoices
        self.mock_file_manager.save_invoices.assert_not_called()
    
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_create_invoice_product_not_found(self, mock_stdout):
        """Kiểm tra tạo hóa đơn với sản phẩm không tồn tại."""
        # Thiết lập mock product_manager.find_product để trả về None
        self.mock_product_manager.find_product.return_value = None
        
        # Tạo hóa đơn với sản phẩm không tồn tại
        result = self.invoice_manager.create_invoice(
            invoice_id="INV001",
            customer_name="Nguyễn Văn A",
            items_data=[
                {"product_id": "P999", "quantity": 2}  # Sản phẩm không tồn tại
            ]
        )
        
        # Kiểm tra kết quả
        self.assertFalse(result)
        self.assertEqual(len(self.invoice_manager.invoices), 0)
        
        # Kiểm tra thông báo
        self.assertIn("Không tìm thấy sản phẩm với Mã 'P999'!", mock_stdout.getvalue())
        
        # Kiểm tra không gọi save_invoices
        self.mock_file_manager.save_invoices.assert_not_called()
    
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_find_invoice(self, mock_stdout):
        """Kiểm tra tìm hóa đơn."""
        # Tạo hóa đơn hiện có
        invoice1 = Invoice(invoice_id="INV001", customer_name="Nguyễn Văn A")
        invoice2 = Invoice(invoice_id="INV002", customer_name="Nguyễn Văn B")
        self.invoice_manager.invoices = [invoice1, invoice2]
        
        # Tìm hóa đơn tồn tại
        found_invoice = self.invoice_manager.find_invoice("INV001")
        
        # Kiểm tra kết quả
        self.assertEqual(found_invoice, invoice1)
        
        # Tìm hóa đơn không tồn tại
        not_found_invoice = self.invoice_manager.find_invoice("INV999")
        
        # Kiểm tra kết quả
        self.assertIsNone(not_found_invoice)
    
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_view_invoice_detail_valid(self, mock_stdout):
        """Kiểm tra xem chi tiết hóa đơn hợp lệ."""
        # Thiết lập mock product_manager.find_product để trả về sản phẩm giả
        self.mock_product_manager.find_product.return_value = Product(
            product_id="P001", name="Sản phẩm thử nghiệm", unit_price=100.0
        )
        
        # Tạo hóa đơn hiện có
        item = InvoiceItem(product_id="P001", quantity=2, unit_price=100.0)
        invoice = Invoice(invoice_id="INV001", customer_name="Nguyễn Văn A", items=[item])
        self.invoice_manager.invoices = [invoice]
        
        # Xem chi tiết hóa đơn
        result = self.invoice_manager.view_invoice_detail("INV001")
        
        # Kiểm tra kết quả
        self.assertTrue(result)
        
        # Kiểm tra thông báo
        self.assertIn("CHI TIẾT HÓA ĐƠN - INV001", mock_stdout.getvalue())
        self.assertIn("Nguyễn Văn A", mock_stdout.getvalue())
        self.assertIn("Sản phẩm thử nghiệm", mock_stdout.getvalue())
    
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_view_invoice_detail_not_found(self, mock_stdout):
        """Kiểm tra xem chi tiết hóa đơn không tồn tại."""
        # Không có hóa đơn nào
        self.invoice_manager.invoices = []
        
        # Xem chi tiết hóa đơn không tồn tại
        result = self.invoice_manager.view_invoice_detail("INV001")
        
        # Kiểm tra kết quả
        self.assertFalse(result)
        
        # Kiểm tra thông báo
        self.assertIn("Không tìm thấy hóa đơn với Mã 'INV001'!", mock_stdout.getvalue())


if __name__ == "__main__":
    unittest.main() 