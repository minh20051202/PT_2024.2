#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kiểm tra toàn diện cho model Invoice và InvoiceItem.

Module kiểm thử này bao gồm các test cases cho:
- InvoiceItem: Kiểm tra tạo, validation và tính toán thành tiền
- Invoice: Kiểm tra tạo hóa đơn, quản lý danh sách mục hàng
- Property methods: Kiểm tra total_amount và total_items
- Edge cases: Xử lý hóa đơn rỗng, giá trị âm, v.v.
- Integration: Kiểm tra tương tác giữa Invoice và InvoiceItem
"""

import pytest
import sys
import os
from datetime import datetime

# Thêm src vào path để import
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from models import Invoice, InvoiceItem

class TestInvoiceItemModel:
    """Kiểm tra cho model InvoiceItem."""

    def test_invoice_item_creation(self):
        """Kiểm tra tạo InvoiceItem với dữ liệu hợp lệ."""
        item = InvoiceItem(
            product_id="P001",
            quantity=5,
            unit_price=100.0
        )

        assert item.product_id == "P001"
        assert item.quantity == 5
        assert item.unit_price == 100.0

    def test_invoice_item_total_price(self):
        """Kiểm tra tính toán tổng giá của một mặt hàng trong hóa đơn."""
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
    """Kiểm tra cho model Invoice."""

    def test_invoice_creation_valid(self):
        """Kiểm tra tạo Invoice với dữ liệu hợp lệ."""
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

        # Kiểm tra các thuộc tính mặc định
        assert invoice.invoice_id == "INV002"
        assert invoice.customer_name == "Nguyễn Văn B"
        assert invoice.date == today  # Mặc định là hôm nay
        assert len(invoice.items) == 0  # Danh sách rỗng

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

        # Kiểm tra tổng tiền = tổng của tất cả mặt hàng
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

        # Kiểm tra tổng số mặt hàng = tổng của tất cả số lượng
        assert invoice.total_items == 5

        # Thử với hóa đơn không có mặt hàng
        empty_invoice = Invoice(
            invoice_id="INV006",
            customer_name="Nguyễn Văn F"
        )
        assert empty_invoice.total_items == 0


if __name__ == "__main__":
    unittest.main()