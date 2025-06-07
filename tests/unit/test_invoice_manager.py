#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comprehensive tests for InvoiceManager.
"""

import pytest
import sys
import os
import io
from datetime import datetime
from unittest.mock import patch

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from core.invoice_manager import InvoiceManager
from core.product_manager import ProductManager
from models import Invoice, InvoiceItem
from tests.test_helpers import TestAssertions


class TestInvoiceManager:
    """Tests for InvoiceManager."""

    def test_create_invoice_valid(self, populated_product_manager, temp_db):
        """Test creating a valid invoice."""
        with patch('utils.db_utils.DATABASE_PATH', temp_db):
            with patch('database.database.DATABASE_PATH', temp_db):
                invoice_manager = InvoiceManager(populated_product_manager)

                items_data = [
                    {'product_id': 'P001', 'quantity': 2},
                    {'product_id': 'P002', 'quantity': 1}
                ]

                invoice, message = invoice_manager.create_invoice(
                    customer_name="Nguyễn Văn A",
                    items_data=items_data
                )

                assert invoice is not None
                assert "thành công" in message
                assert invoice.customer_name == "Nguyễn Văn A"
                assert len(invoice.items) == 2
                assert invoice.total_amount > 0

    def test_create_invoice_empty_customer_name(self, populated_product_manager, temp_db):
        """Test creating invoice with empty customer name."""
        with patch('utils.db_utils.DATABASE_PATH', temp_db):
            with patch('database.database.DATABASE_PATH', temp_db):
                invoice_manager = InvoiceManager(populated_product_manager)

                items_data = [{'product_id': 'P001', 'quantity': 1}]

                invoice, message = invoice_manager.create_invoice(
                    customer_name="",
                    items_data=items_data
                )

                assert invoice is None
                assert "bắt buộc" in message

    def test_create_invoice_empty_items(self, populated_product_manager, temp_db):
        """Test creating invoice with no items."""
        with patch('utils.db_utils.DATABASE_PATH', temp_db):
            with patch('database.database.DATABASE_PATH', temp_db):
                invoice_manager = InvoiceManager(populated_product_manager)

                invoice, message = invoice_manager.create_invoice(
                    customer_name="Nguyễn Văn A",
                    items_data=[]
                )

                assert invoice is None
                assert "ít nhất một mặt hàng" in message

    def test_create_invoice_invalid_product(self, populated_product_manager, temp_db):
        """Test creating invoice with non-existent product."""
        with patch('utils.db_utils.DATABASE_PATH', temp_db):
            with patch('database.database.DATABASE_PATH', temp_db):
                invoice_manager = InvoiceManager(populated_product_manager)

                items_data = [{'product_id': 'NONEXISTENT', 'quantity': 1}]

                invoice, message = invoice_manager.create_invoice(
                    customer_name="Nguyễn Văn A",
                    items_data=items_data
                )

                assert invoice is None
                assert "không tồn tại" in message