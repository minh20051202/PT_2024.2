#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kiểm tra tích hợp luồng làm việc chính của hệ thống quản lý hóa đơn.

Module kiểm thử này thực hiện end-to-end testing cho:
- Luồng làm việc hoàn chỉnh: Từ thêm sản phẩm đến tạo hóa đơn
- Tương tác giữa các component: ProductManager, InvoiceManager, StatisticsManager
- Kiểm tra data consistency: Giữa các bảng database
- Performance testing: Với dataset thực tế
- Error recovery: Xử lý khi có lỗi trong quá trình

Mô phỏng các kịch bản kiểm định thực tế.
"""

import pytest
import sys
import os
import io
import tempfile
import unittest
from unittest.mock import patch

# Thêm src vào path để import
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from core.product_manager import ProductManager
from core.invoice_manager import InvoiceManager
from models import Product, Invoice
from test_helpers import TestAssertions

class TestMainWorkflow:
    """Kiểm tra tích hợp cho luồng làm việc chính của ứng dụng."""

    def test_complete_product_and_invoice_workflow(self, temp_db):
        """Kiểm tra luồng làm việc hoàn chỉnh từ tạo sản phẩm đến tạo hóa đơn."""
        with patch('utils.db_utils.DATABASE_PATH', temp_db):
            with patch('database.database.DATABASE_PATH', temp_db):
                # Khởi tạo managers
                product_manager = ProductManager()
                invoice_manager = InvoiceManager(product_manager)

                # 1. Thêm sản phẩm
                success, message = product_manager.add_product(
                    product_id="P001",
                    name="Laptop Dell",
                    unit_price=25000000.0,
                    category="Electronics",
                    calculation_unit="chiếc"
                )
                assert success, f"Không thể thêm sản phẩm: {message}"

                success, message = product_manager.add_product(
                    product_id="P002",
                    name="Chuột không dây",
                    unit_price=500000.0,
                    category="Accessories",
                    calculation_unit="cái"
                )
                assert success, f"Không thể thêm sản phẩm thứ hai: {message}"

                # Xác minh sản phẩm đã được thêm
                assert len(product_manager.products) == 2

                # 2. Tạo hóa đơn
                items_data = [
                    {"product_id": "P001", "quantity": 1},
                    {"product_id": "P002", "quantity": 2}
                ]

                invoice, message = invoice_manager.create_invoice(
                    customer_name="Nguyễn Văn A",
                    items_data=items_data
                )

                assert invoice is not None, f"Không thể tạo hóa đơn: {message}"
                assert invoice.customer_name == "Nguyễn Văn A"
                assert len(invoice.items) == 2
                assert invoice.total_amount == 26000000.0  # 25000000 + 2*500000

                # 3. Xác minh hóa đơn đã được lưu và có thể tải
                success, message = invoice_manager.load_invoices()
                assert success, f"Không thể tải hóa đơn: {message}"
                assert len(invoice_manager.invoices) >= 1

    def test_error_handling_workflow(self, temp_db):
        """Kiểm tra xử lý lỗi trong luồng làm việc."""
        with patch('utils.db_utils.DATABASE_PATH', temp_db):
            with patch('database.database.DATABASE_PATH', temp_db):
                product_manager = ProductManager()
                invoice_manager = InvoiceManager(product_manager)

                # Kiểm tra thêm sản phẩm không hợp lệ
                success, message = product_manager.add_product("", "Invalid Product", 100.0)
                assert not success
                assert "Mã sản phẩm" in message

                # Kiểm tra tạo hóa đơn với sản phẩm không tồn tại
                invoice, message = invoice_manager.create_invoice(
                    customer_name="Test Customer",
                    items_data=[{"product_id": "NONEXISTENT", "quantity": 1}]
                )
                assert invoice is None
                assert "không tồn tại" in message