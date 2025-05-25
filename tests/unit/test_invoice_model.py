#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests cho mô hình Invoice và InvoiceItem.
"""

import unittest
import sys
import os
import datetime

# Thêm thư mục gốc vào đường dẫn để import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.invoicemanager.models.invoice import Invoice, InvoiceItem

class TestInvoiceItemModel(unittest.TestCase):
    """Kiểm thử cho mô hình InvoiceItem."""
    
    def test_invoice_item_creation(self):
        """Kiểm tra tạo InvoiceItem với dữ liệu hợp lệ."""
        # Tạo một mặt hàng hóa đơn
        item = InvoiceItem(
            product_id="P001",
            quantity=5,
            unit_price=100.0
        )
        
        # Kiểm tra các thuộc tính
        self.assertEqual(item.product_id, "P001")
        self.assertEqual(item.quantity, 5)
        self.assertEqual(item.unit_price, 100.0)
    
    def test_invoice_item_total_price(self):
        """Kiểm tra tính toán tổng giá trị của một mặt hàng."""
        # Tạo một mặt hàng hóa đơn
        item = InvoiceItem(
            product_id="P001",
            quantity=5,
            unit_price=100.0
        )
        
        # Kiểm tra tổng giá trị = quantity * unit_price
        self.assertEqual(item.total_price, 500.0)
        
        # Kiểm tra với giá trị khác
        item2 = InvoiceItem(
            product_id="P002",
            quantity=2,
            unit_price=50.0
        )
        self.assertEqual(item2.total_price, 100.0)


class TestInvoiceModel(unittest.TestCase):
    """Kiểm thử cho mô hình Invoice."""
    
    def test_invoice_creation_valid(self):
        """Kiểm tra tạo Invoice với dữ liệu hợp lệ."""
        # Tạo các mặt hàng cho hóa đơn
        item1 = InvoiceItem("P001", 2, 100.0)
        item2 = InvoiceItem("P002", 3, 50.0)
        
        # Tạo hóa đơn với dữ liệu hợp lệ
        invoice = Invoice(
            invoice_id="INV001",
            customer_name="Nguyễn Văn A",
            items=[item1, item2],
            date="2023-11-01"
        )
        
        # Kiểm tra các thuộc tính
        self.assertEqual(invoice.invoice_id, "INV001")
        self.assertEqual(invoice.customer_name, "Nguyễn Văn A")
        self.assertEqual(invoice.date, "2023-11-01")
        self.assertEqual(len(invoice.items), 2)
        self.assertEqual(invoice.items[0].product_id, "P001")
        self.assertEqual(invoice.items[1].product_id, "P002")
    
    def test_invoice_creation_with_defaults(self):
        """Kiểm tra tạo Invoice với giá trị mặc định."""
        # Tạo hóa đơn với danh sách mặt hàng rỗng
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        invoice = Invoice(
            invoice_id="INV002",
            customer_name="Nguyễn Văn B"
        )
        
        # Kiểm tra các thuộc tính mặc định
        self.assertEqual(invoice.invoice_id, "INV002")
        self.assertEqual(invoice.customer_name, "Nguyễn Văn B")
        self.assertEqual(invoice.date, today)  # Mặc định là ngày hôm nay
        self.assertEqual(len(invoice.items), 0)  # Danh sách rỗng
    
    def test_invoice_total_amount(self):
        """Kiểm tra tính toán tổng giá trị của hóa đơn."""
        # Tạo các mặt hàng cho hóa đơn
        item1 = InvoiceItem("P001", 2, 100.0)  # 200.0
        item2 = InvoiceItem("P002", 3, 50.0)   # 150.0
        
        # Tạo hóa đơn
        invoice = Invoice(
            invoice_id="INV003",
            customer_name="Nguyễn Văn C",
            items=[item1, item2]
        )
        
        # Kiểm tra tổng giá trị hóa đơn = tổng của các mặt hàng
        self.assertEqual(invoice.total_amount, 350.0)
        
        # Thử với hóa đơn không có mặt hàng
        empty_invoice = Invoice(
            invoice_id="INV004",
            customer_name="Nguyễn Văn D"
        )
        self.assertEqual(empty_invoice.total_amount, 0.0)
    
    def test_invoice_total_items(self):
        """Kiểm tra tính toán tổng số lượng mặt hàng của hóa đơn."""
        # Tạo các mặt hàng cho hóa đơn
        item1 = InvoiceItem("P001", 2, 100.0)
        item2 = InvoiceItem("P002", 3, 50.0)
        
        # Tạo hóa đơn
        invoice = Invoice(
            invoice_id="INV005",
            customer_name="Nguyễn Văn E",
            items=[item1, item2]
        )
        
        # Kiểm tra tổng số lượng mặt hàng = tổng quantity của các mặt hàng
        self.assertEqual(invoice.total_items, 5)
        
        # Thử với hóa đơn không có mặt hàng
        empty_invoice = Invoice(
            invoice_id="INV006",
            customer_name="Nguyễn Văn F"
        )
        self.assertEqual(empty_invoice.total_items, 0)


if __name__ == "__main__":
    unittest.main() 