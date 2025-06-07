#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comprehensive integration tests for the main application workflow.
"""

import pytest
import sys
import os
import io
import tempfile
import unittest
from unittest.mock import patch

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from core.product_manager import ProductManager
from core.invoice_manager import InvoiceManager
from models import Product, Invoice
from tests.test_helpers import TestAssertions

class TestMainWorkflow:
    """Integration tests for main application workflow."""
    """Kiểm thử tích hợp cho luồng làm việc chính."""
    
    def test_complete_product_and_invoice_workflow(self, temp_db):
        """Test complete workflow from product creation to invoice generation."""
        with patch('utils.db_utils.DATABASE_PATH', temp_db):
            with patch('database.database.DATABASE_PATH', temp_db):
                # Initialize managers
                product_manager = ProductManager()
                invoice_manager = InvoiceManager(product_manager)

                # 1. Add products
                success, message = product_manager.add_product(
                    product_id="P001",
                    name="Laptop Dell",
                    unit_price=25000000.0,
                    category="Electronics",
                    calculation_unit="chiếc"
                )
                assert success, f"Failed to add product: {message}"

                success, message = product_manager.add_product(
                    product_id="P002",
                    name="Chuột không dây",
                    unit_price=500000.0,
                    category="Accessories",
                    calculation_unit="cái"
                )
                assert success, f"Failed to add second product: {message}"

                # Verify products were added
                assert len(product_manager.products) == 2

                # 2. Create invoice
                items_data = [
                    {"product_id": "P001", "quantity": 1},
                    {"product_id": "P002", "quantity": 2}
                ]

                invoice, message = invoice_manager.create_invoice(
                    customer_name="Nguyễn Văn A",
                    items_data=items_data
                )

                assert invoice is not None, f"Failed to create invoice: {message}"
                assert invoice.customer_name == "Nguyễn Văn A"
                assert len(invoice.items) == 2
                assert invoice.total_amount == 26000000.0  # 25000000 + 2*500000

                # 3. Verify invoice was saved and can be loaded
                success, message = invoice_manager.load_invoices()
                assert success, f"Failed to load invoices: {message}"
                assert len(invoice_manager.invoices) >= 1

    def test_error_handling_workflow(self, temp_db):
        """Test error handling in the workflow."""
        with patch('utils.db_utils.DATABASE_PATH', temp_db):
            with patch('database.database.DATABASE_PATH', temp_db):
                product_manager = ProductManager()
                invoice_manager = InvoiceManager(product_manager)

                # Test adding invalid product
                success, message = product_manager.add_product("", "Invalid Product", 100.0)
                assert not success
                assert "Mã sản phẩm" in message

                # Test creating invoice with no products
                invoice, message = invoice_manager.create_invoice(
                    customer_name="Test Customer",
                    items_data=[{"product_id": "NONEXISTENT", "quantity": 1}]
                )
                assert invoice is None
                assert "không tồn tại" in message