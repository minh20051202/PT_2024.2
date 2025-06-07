#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comprehensive tests for database utilities.
"""

import pytest
import tempfile
import os
import sys
import sqlite3
from unittest.mock import patch

# Add src to path for imports
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
    """Tests for ensure_database_exists function."""
    
    def test_database_creation(self, temp_db):
        """Test database creation when it doesn't exist."""
        # Remove the database file
        if os.path.exists(temp_db):
            os.unlink(temp_db)
        
        with patch('utils.db_utils.DATABASE_PATH', temp_db):
            success, message = ensure_database_exists()
            assert success
            assert message == ""
            # Directory should be created
            assert os.path.exists(os.path.dirname(temp_db))
    
    def test_database_already_exists(self, temp_db):
        """Test when database already exists."""
        with patch('utils.db_utils.DATABASE_PATH', temp_db):
            success, message = ensure_database_exists()
            assert success
            assert message == ""
    
    def test_permission_error(self):
        """Test handling of permission errors."""
        # Try to create database in a read-only location
        readonly_path = "/root/readonly/test.db"
        
        with patch('utils.db_utils.DATABASE_PATH', readonly_path):
            success, message = ensure_database_exists()
            assert not success
            assert "Lỗi khi kiểm tra database" in message


class TestSaveData:
    """Tests for save_data function."""
    
    def test_save_product_data(self, temp_db):
        """Test saving product data."""
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
            
            # Verify data was saved
            conn = sqlite3.connect(temp_db)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM products WHERE product_id = ?", ('P001',))
            result = cursor.fetchone()
            conn.close()
            
            assert result is not None
            assert result[0] == 'P001'  # product_id
            assert result[1] == 'Test Product'  # name
    
    def test_save_invoice_data(self, temp_db):
        """Test saving invoice data."""
        with patch('utils.db_utils.DATABASE_PATH', temp_db):
            invoice_data = {
                'customer_name': 'Nguyễn Văn A',
                'date': '2023-12-25'
            }
            
            success, message = save_data('invoices', invoice_data)
            assert success
            assert message == ""
    
    def test_save_invalid_table(self, temp_db):
        """Test saving to non-existent table."""
        with patch('utils.db_utils.DATABASE_PATH', temp_db):
            data = {'field': 'value'}
            
            success, message = save_data('nonexistent_table', data)
            assert not success
            assert "Lỗi khi lưu dữ liệu" in message
    
    def test_save_invalid_data(self, temp_db):
        """Test saving invalid data structure."""
        with patch('utils.db_utils.DATABASE_PATH', temp_db):
            # Missing required fields
            invalid_data = {
                'invalid_field': 'value'
            }
            
            success, message = save_data('products', invalid_data)
            assert not success
            assert "Lỗi khi lưu dữ liệu" in message


class TestLoadData:
    """Tests for load_data function."""
    
    def test_load_all_products(self, temp_db):
        """Test loading all products."""
        with patch('utils.db_utils.DATABASE_PATH', temp_db):
            # First, save some test data
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
            
            # Load all products
            products, error = load_data('products')
            assert error == ""
            assert len(products) == 2
            assert products[0]['product_id'] == 'P001'
            assert products[1]['product_id'] == 'P002'
    
    def test_load_with_conditions(self, temp_db):
        """Test loading data with conditions."""
        with patch('utils.db_utils.DATABASE_PATH', temp_db):
            # Save test data
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
            
            # Load with condition
            results, error = load_data('products', {'category': 'Electronics'})
            assert error == ""
            assert len(results) == 1
            assert results[0]['product_id'] == 'P001'
    
    def test_load_empty_table(self, temp_db):
        """Test loading from empty table."""
        with patch('utils.db_utils.DATABASE_PATH', temp_db):
            results, error = load_data('products')
            assert error == ""
            assert results == []
    
    def test_load_nonexistent_table(self, temp_db):
        """Test loading from non-existent table."""
        with patch('utils.db_utils.DATABASE_PATH', temp_db):
            results, error = load_data('nonexistent_table')
            assert error != ""
            assert "Lỗi khi tải dữ liệu" in error
            assert results == []


class TestUpdateData:
    """Tests for update_data function."""
    
    def test_update_product(self, temp_db):
        """Test updating product data."""
        with patch('utils.db_utils.DATABASE_PATH', temp_db):
            # First, save a product
            original_data = {
                'product_id': 'P001',
                'name': 'Original Product',
                'unit_price': 100.0,
                'calculation_unit': 'chiếc',
                'category': 'Test'
            }
            save_data('products', original_data)
            
            # Update the product
            update_values = {
                'name': 'Updated Product',
                'unit_price': 150.0
            }
            conditions = {'product_id': 'P001'}
            
            success, message = update_data('products', update_values, conditions)
            assert success
            assert message == ""
            
            # Verify update
            products, _ = load_data('products', {'product_id': 'P001'})
            assert len(products) == 1
            assert products[0]['name'] == 'Updated Product'
            assert products[0]['unit_price'] == 150.0
            assert products[0]['category'] == 'Test'  # Unchanged
    
    def test_update_nonexistent_record(self, temp_db):
        """Test updating non-existent record."""
        with patch('utils.db_utils.DATABASE_PATH', temp_db):
            update_values = {'name': 'New Name'}
            conditions = {'product_id': 'NONEXISTENT'}
            
            success, message = update_data('products', update_values, conditions)
            # Should succeed even if no rows affected
            assert success
            assert message == ""
    
    def test_update_invalid_table(self, temp_db):
        """Test updating non-existent table."""
        with patch('utils.db_utils.DATABASE_PATH', temp_db):
            update_values = {'field': 'value'}
            conditions = {'id': 1}
            
            success, message = update_data('nonexistent_table', update_values, conditions)
            assert not success
            assert "Lỗi khi cập nhật dữ liệu" in message


class TestDeleteData:
    """Tests for delete_data function."""
    
    def test_delete_product(self, temp_db):
        """Test deleting product data."""
        with patch('utils.db_utils.DATABASE_PATH', temp_db):
            # First, save some products
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
            
            # Delete one product
            success, message = delete_data('products', {'product_id': 'P001'})
            assert success
            assert message == ""
            
            # Verify deletion
            remaining_products, _ = load_data('products')
            assert len(remaining_products) == 1
            assert remaining_products[0]['product_id'] == 'P002'
    
    def test_delete_nonexistent_record(self, temp_db):
        """Test deleting non-existent record."""
        with patch('utils.db_utils.DATABASE_PATH', temp_db):
            success, message = delete_data('products', {'product_id': 'NONEXISTENT'})
            # Should succeed even if no rows affected
            assert success
            assert message == ""
    
    def test_delete_invalid_table(self, temp_db):
        """Test deleting from non-existent table."""
        with patch('utils.db_utils.DATABASE_PATH', temp_db):
            success, message = delete_data('nonexistent_table', {'id': 1})
            assert not success
            assert "Lỗi khi xóa dữ liệu" in message
