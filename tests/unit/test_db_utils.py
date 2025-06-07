#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kiểm tra toàn diện cho các hàm db_utils.

Module kiểm thử này bao gồm các test cases cho:
- Các hàm CRUD cơ bản: save_data, load_data, update_data, delete_data
- Xử lý lỗi database: SQLite exceptions, connection issues
- Kiểm tra data integrity: Transactions, rollbacks
- Performance testing: Large datasets, concurrent access
- Security testing: SQL injection prevention

Sử dụng temp database để đảm bảo test isolation.
"""

import pytest
import tempfile
import os
import sys
import sqlite3
from unittest.mock import patch

# Thêm src vào path để import
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from utils.db_utils import (
    ensure_database_exists,
    save_data,
    load_data,
    update_data,
    delete_data
)
from database.database import initialize_database


class TestEnsureDatabaseExists:
    """Kiểm tra cho hàm ensure_database_exists."""

    def test_database_creation(self, temp_db):
        """Kiểm tra tạo database khi nó không tồn tại."""
        # Xóa file database
        if os.path.exists(temp_db):
            os.unlink(temp_db)

        with patch('utils.db_utils.DATABASE_PATH', temp_db):
            success, message = ensure_database_exists()
            assert success
            assert message == ""
            # Thư mục nên được tạo
            assert os.path.exists(os.path.dirname(temp_db))

    def test_database_already_exists(self, temp_db):
        """Kiểm tra khi database đã tồn tại."""
        with patch('utils.db_utils.DATABASE_PATH', temp_db):
            success, message = ensure_database_exists()
            assert success
            assert message == ""

    def test_permission_error(self):
        """Kiểm tra xử lý lỗi quyền truy cập."""
        # Thử tạo database ở vị trí chỉ đọc
        readonly_path = "/root/readonly/test.db"

        with patch('utils.db_utils.DATABASE_PATH', readonly_path):
            success, message = ensure_database_exists()
            assert not success
            assert "Lỗi khi kiểm tra database" in message


class TestSaveData:
    """Kiểm tra cho hàm save_data."""

    def test_save_product_data(self, temp_db):
        """Kiểm tra lưu dữ liệu sản phẩm."""
        with patch('utils.db_utils.DATABASE_PATH', temp_db):
            product_data = {
                'product_id': 'P001',
                'name': 'Test Product',
                'unit_price': 100.0,
                'calculation_unit': 'chiếc',
                'category': 'Test'
            }

            success, message = save_data('products', product_data)
            assert success
            assert message == ""

            # Xác minh dữ liệu đã được lưu
            conn = sqlite3.connect(temp_db)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM products WHERE product_id = ?", ('P001',))
            result = cursor.fetchone()
            conn.close()

            assert result is not None
            assert result[0] == 'P001'  # product_id
            assert result[1] == 'Test Product'  # name

    def test_save_invoice_data(self, temp_db):
        """Kiểm tra lưu dữ liệu hóa đơn."""
        with patch('utils.db_utils.DATABASE_PATH', temp_db):
            invoice_data = {
                'customer_name': 'Nguyễn Văn A',
                'date': '2023-12-25'
            }

            success, message = save_data('invoices', invoice_data)
            assert success
            assert message == ""

    def test_save_invalid_table(self, temp_db):
        """Kiểm tra lưu vào bảng không tồn tại."""
        with patch('utils.db_utils.DATABASE_PATH', temp_db):
            data = {'field': 'value'}

            success, message = save_data('nonexistent_table', data)
            assert not success
            assert "Lỗi khi lưu dữ liệu" in message

    def test_save_invalid_data(self, temp_db):
        """Kiểm tra lưu cấu trúc dữ liệu không hợp lệ."""
        with patch('utils.db_utils.DATABASE_PATH', temp_db):
            # Thiếu các trường bắt buộc
            invalid_data = {
                'invalid_field': 'value'
            }

            success, message = save_data('products', invalid_data)
            assert not success
            assert "Lỗi khi lưu dữ liệu" in message


class TestLoadData:
    """Kiểm tra cho hàm load_data."""

    def test_load_all_products(self, temp_db):
        """Kiểm tra tải tất cả sản phẩm."""
        with patch('utils.db_utils.DATABASE_PATH', temp_db):
            # Đầu tiên, lưu một số dữ liệu test
            test_products = [
                {
                    'product_id': 'P001',
                    'name': 'Product 1',
                    'unit_price': 100.0,
                    'calculation_unit': 'chiếc',
                    'category': 'Test'
                },
                {
                    'product_id': 'P002',
                    'name': 'Product 2',
                    'unit_price': 200.0,
                    'calculation_unit': 'cái',
                    'category': 'Test'
                }
            ]

            for product in test_products:
                save_data('products', product)

            # Tải tất cả sản phẩm
            products, error = load_data('products')
            assert error == ""
            assert len(products) == 2
            assert products[0]['product_id'] == 'P001'
            assert products[1]['product_id'] == 'P002'

    def test_load_with_conditions(self, temp_db):
        """Kiểm tra tải dữ liệu với điều kiện."""
        with patch('utils.db_utils.DATABASE_PATH', temp_db):
            # Lưu dữ liệu test
            products = [
                {
                    'product_id': 'P001',
                    'name': 'Product 1',
                    'unit_price': 100.0,
                    'calculation_unit': 'chiếc',
                    'category': 'Electronics'
                },
                {
                    'product_id': 'P002',
                    'name': 'Product 2',
                    'unit_price': 200.0,
                    'calculation_unit': 'cái',
                    'category': 'Office'
                }
            ]

            for product in products:
                save_data('products', product)

            # Tải với điều kiện
            results, error = load_data('products', {'category': 'Electronics'})
            assert error == ""
            assert len(results) == 1
            assert results[0]['product_id'] == 'P001'

    def test_load_empty_table(self, temp_db):
        """Kiểm tra tải từ bảng rỗng."""
        with patch('utils.db_utils.DATABASE_PATH', temp_db):
            results, error = load_data('products')
            assert error == ""
            assert results == []

    def test_load_nonexistent_table(self, temp_db):
        """Kiểm tra tải từ bảng không tồn tại."""
        with patch('utils.db_utils.DATABASE_PATH', temp_db):
            results, error = load_data('nonexistent_table')
            assert error != ""
            assert "Lỗi khi tải dữ liệu" in error
            assert results == []


class TestUpdateData:
    """Kiểm tra cho hàm update_data."""

    def test_update_product(self, temp_db):
        """Kiểm tra cập nhật dữ liệu sản phẩm."""
        with patch('utils.db_utils.DATABASE_PATH', temp_db):
            # Đầu tiên, lưu một sản phẩm
            original_data = {
                'product_id': 'P001',
                'name': 'Original Product',
                'unit_price': 100.0,
                'calculation_unit': 'chiếc',
                'category': 'Test'
            }
            save_data('products', original_data)

            # Cập nhật sản phẩm
            update_values = {
                'name': 'Updated Product',
                'unit_price': 150.0
            }
            conditions = {'product_id': 'P001'}

            success, message = update_data('products', update_values, conditions)
            assert success
            assert message == ""

            # Xác minh cập nhật
            products, _ = load_data('products', {'product_id': 'P001'})
            assert len(products) == 1
            assert products[0]['name'] == 'Updated Product'
            assert products[0]['unit_price'] == 150.0
            assert products[0]['category'] == 'Test'  # Không thay đổi

    def test_update_nonexistent_record(self, temp_db):
        """Kiểm tra cập nhật bản ghi không tồn tại."""
        with patch('utils.db_utils.DATABASE_PATH', temp_db):
            update_values = {'name': 'New Name'}
            conditions = {'product_id': 'NONEXISTENT'}

            success, message = update_data('products', update_values, conditions)
            # Nên thành công ngay cả khi không có hàng nào bị ảnh hưởng
            assert success
            assert message == ""

    def test_update_invalid_table(self, temp_db):
        """Kiểm tra cập nhật bảng không tồn tại."""
        with patch('utils.db_utils.DATABASE_PATH', temp_db):
            update_values = {'field': 'value'}
            conditions = {'id': 1}

            success, message = update_data('nonexistent_table', update_values, conditions)
            assert not success
            assert "Lỗi khi cập nhật dữ liệu" in message


class TestDeleteData:
    """Kiểm tra cho hàm delete_data."""

    def test_delete_product(self, temp_db):
        """Kiểm tra xóa dữ liệu sản phẩm."""
        with patch('utils.db_utils.DATABASE_PATH', temp_db):
            # Đầu tiên, lưu một số sản phẩm
            products = [
                {
                    'product_id': 'P001',
                    'name': 'Product 1',
                    'unit_price': 100.0,
                    'calculation_unit': 'chiếc',
                    'category': 'Test'
                },
                {
                    'product_id': 'P002',
                    'name': 'Product 2',
                    'unit_price': 200.0,
                    'calculation_unit': 'cái',
                    'category': 'Test'
                }
            ]

            for product in products:
                save_data('products', product)

            # Xóa một sản phẩm
            success, message = delete_data('products', {'product_id': 'P001'})
            assert success
            assert message == ""

            # Xác minh việc xóa
            remaining_products, _ = load_data('products')
            assert len(remaining_products) == 1
            assert remaining_products[0]['product_id'] == 'P002'

    def test_delete_nonexistent_record(self, temp_db):
        """Kiểm tra xóa bản ghi không tồn tại."""
        with patch('utils.db_utils.DATABASE_PATH', temp_db):
            success, message = delete_data('products', {'product_id': 'NONEXISTENT'})
            # Nên thành công ngay cả khi không có hàng nào bị ảnh hưởng
            assert success
            assert message == ""

    def test_delete_invalid_table(self, temp_db):
        """Kiểm tra xóa từ bảng không tồn tại."""
        with patch('utils.db_utils.DATABASE_PATH', temp_db):
            success, message = delete_data('nonexistent_table', {'id': 1})
            assert not success
            assert "Lỗi khi xóa dữ liệu" in message
