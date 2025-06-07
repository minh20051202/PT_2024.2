#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for database module.
"""

import pytest
import sys
import os
import sqlite3
import tempfile
from unittest.mock import patch, MagicMock

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from database.database import initialize_database, DATABASE_PATH


class TestDatabase:
    """Tests for database initialization."""

    def test_initialize_database_success(self, temp_db):
        """Test successful database initialization."""
        with patch('database.database.DATABASE_PATH', temp_db):
            success, message = initialize_database()
            
            assert success
            assert "thành công" in message
            assert os.path.exists(temp_db)
            
            # Verify tables were created
            conn = sqlite3.connect(temp_db)
            cursor = conn.cursor()
            
            # Check for products table
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='products';")
            assert cursor.fetchone() is not None
            
            # Check for invoices table
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='invoices';")
            assert cursor.fetchone() is not None
            
            # Check for invoice_items table
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='invoice_items';")
            assert cursor.fetchone() is not None
            
            conn.close()

    def test_initialize_database_sqlite_error(self, temp_db):
        """Test database initialization with SQLite error."""
        with patch('database.database.DATABASE_PATH', temp_db):
            with patch('sqlite3.connect') as mock_connect:
                mock_connect.side_effect = sqlite3.Error("Connection failed")
                
                success, message = initialize_database()
                
                assert not success
                assert "Lỗi khi khởi tạo database" in message
                assert "Connection failed" in message

    def test_initialize_database_connection_cleanup(self, temp_db):
        """Test that database connection is properly closed even on error."""
        with patch('database.database.DATABASE_PATH', temp_db):
            mock_conn = MagicMock()
            mock_cursor = MagicMock()
            mock_conn.cursor.return_value = mock_cursor
            
            # Make cursor.execute raise an error
            mock_cursor.execute.side_effect = sqlite3.Error("SQL error")
            
            with patch('sqlite3.connect', return_value=mock_conn):
                success, message = initialize_database()
                
                assert not success
                # Verify connection.close() was called
                mock_conn.close.assert_called_once()

    def test_main_execution(self, temp_db, capsys):
        """Test running the module as main script."""
        with patch('database.database.DATABASE_PATH', temp_db):
            # Import and run the main section
            import subprocess
            import sys
            result = subprocess.run(
                [sys.executable, '/home/0xKaBG/Project/ktlt/PT_2024.2/src/database/database.py'],
                capture_output=True,
                text=True,
                env={**os.environ, 'DATABASE_PATH': temp_db}
            )
            
            assert "Đang tiến hành khởi tạo database" in result.stdout
            assert "thành công" in result.stdout

