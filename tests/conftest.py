#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cấu hình Pytest và fixtures chia sẻ cho hệ thống quản lý hóa đơn.

File này cung cấp các pytest fixtures tự động có sẵn cho tất cả tests.
Fixtures xử lý thiết lập test, dỎn dẹp, và cung cấp các dependencies test chung như
database tạm thời và các instance manager đã được cấu hình sẵn.

Các fixtures chính:
- temp_db: Tạo database SQLite tạm thời cho testing
- product_manager: ProductManager instance với database test
- populated_product_manager: ProductManager với dữ liệu mẫu

Tất cả fixtures được tự động dỎn dẹp sau khi test hoàn thành.
"""

import pytest
import tempfile
import os
import sys
from unittest.mock import patch

# Thêm src vào path để import
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.product_manager import ProductManager
from core.invoice_manager import InvoiceManager
from database.database import initialize_database


@pytest.fixture
def temp_db():
    """Tạo database tạm thời để testing."""
    temp_db_fd, temp_db_path = tempfile.mkstemp(suffix='.db')
    os.close(temp_db_fd)

    # Khởi tạo test database
    with patch('database.database.DATABASE_PATH', temp_db_path):
        with patch('utils.db_utils.DATABASE_PATH', temp_db_path):
            success, message = initialize_database()
            assert success, f"Không thể khởi tạo test database: {message}"

            yield temp_db_path

    # Dọn dẹp
    if os.path.exists(temp_db_path):
        os.unlink(temp_db_path)


@pytest.fixture
def product_manager(temp_db):
    """Tạo instance ProductManager với database tạm thời."""
    with patch('database.database.DATABASE_PATH', temp_db):
        with patch('utils.db_utils.DATABASE_PATH', temp_db):
            return ProductManager()


@pytest.fixture
def populated_product_manager(product_manager):
    """ProductManager với các sản phẩm mẫu đã được thêm sẵn."""
    sample_products = [
        {
            'product_id': 'P001',
            'name': 'Laptop Dell XPS 13',
            'unit_price': 25000000.0,
            'calculation_unit': 'chiếc',
            'category': 'Electronics'
        },
        {
            'product_id': 'P002',
            'name': 'Chuột không dây Logitech',
            'unit_price': 500000.0,
            'calculation_unit': 'chiếc',
            'category': 'Electronics'
        }
    ]

    for product_data in sample_products:
        success, message = product_manager.add_product(**product_data)
        assert success, f"Không thể thêm sản phẩm: {message}"
    return product_manager
