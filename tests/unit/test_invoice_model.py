#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comprehensive tests for Invoice and InvoiceItem models.
"""

import pytest
import sys
import os
from datetime import datetime

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from models import Invoice, InvoiceItem

class TestInvoiceItemModel:
    """Tests for InvoiceItem model."""

    def test_invoice_item_creation(self):
        """Test creating InvoiceItem with valid data."""
        item = InvoiceItem(
            product_id="P001",
            quantity=5,
            unit_price=100.0
        )

        assert item.product_id == "P001"
        assert item.quantity == 5
        assert item.unit_price == 100.0

    def test_invoice_item_total_price(self):
        """Test calculating total price of an invoice item."""
        item = InvoiceItem(
            product_id="P001",
            quantity=5,
            unit_price=100.0
        )

        assert item.total_price == 500.0

        item2 = InvoiceItem(
            product_id="P002",
            quantity=2,
            unit_price=50.0
        )
        assert item2.total_price == 100.0


class TestInvoiceModel:
    """Tests for Invoice model."""

    def test_invoice_creation_valid(self):
        """Test creating Invoice with valid data."""
        item1 = InvoiceItem("P001", 2, 100.0)
        item2 = InvoiceItem("P002", 3, 50.0)

        invoice = Invoice(
            invoice_id="INV001",
            customer_name="Nguyễn Văn A",
            items=[item1, item2],
            date="2023-11-01"
        )

        assert invoice.invoice_id == "INV001"
        assert invoice.customer_name == "Nguyễn Văn A"
        assert invoice.date == "2023-11-01"
        assert len(invoice.items) == 2
        assert invoice.items[0].product_id == "P001"
        assert invoice.items[1].product_id == "P002"
    
    def test_invoice_creation_with_defaults(self):
        """Kiểm tra tạo Invoice với giá trị mặc định."""
        # Tạo hóa đơn với danh sách mặt hàng rỗng
        today = datetime.now().strftime('%Y-%m-%d')
        invoice = Invoice(
            invoice_id="INV002",
            customer_name="Nguyễn Văn B"
        )
        
        # Check default attributes
        assert invoice.invoice_id == "INV002"
        assert invoice.customer_name == "Nguyễn Văn B"
        assert invoice.date == today  # Default is today
        assert len(invoice.items) == 0  # Empty list
    
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
        
        # Check total amount = sum of all items
        assert invoice.total_amount == 350.0
        
        # Thử với hóa đơn không có mặt hàng
        empty_invoice = Invoice(
            invoice_id="INV004",
            customer_name="Nguyễn Văn D"
        )
        assert empty_invoice.total_amount == 0.0
    
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
        
        # Check total items = sum of all quantities
        assert invoice.total_items == 5
        
        # Thử với hóa đơn không có mặt hàng
        empty_invoice = Invoice(
            invoice_id="INV006",
            customer_name="Nguyễn Văn F"
        )
        assert empty_invoice.total_items == 0


if __name__ == "__main__":
    unittest.main() 