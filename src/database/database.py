#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module để khởi tạo và quản lý database SQLite.

Module này chịu trách nhiệm thiết lập và quản lý cơ sở dữ liệu
SQLite cho hệ thống quản lý hóa đơn. Bao gồm:
- Khởi tạo database và các bảng cần thiết
- Định nghĩa schema cho products, invoices, invoice_items
- Thiết lập foreign key constraints
- Cấu hình đường dẫn database

Database được đặt trong cùng thư mục với module này.
"""
import sqlite3
import os

DATABASE_NAME = "invoicemanager.db"
# Đặt database trong thư mục database
DATABASE_PATH = os.path.join(os.path.dirname(__file__), DATABASE_NAME)

def initialize_database():
    """
    Khởi tạo database SQLite và tạo các bảng nếu chúng chưa tồn tại.

    Trả về:
        tuple[bool, str]: (True/False, thông báo)
    """
    # Đảm bảo thư mục tồn tại
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)

    conn = None
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        # Bảng sản phẩm (products)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            unit_price REAL NOT NULL,
            calculation_unit TEXT,
            category TEXT
        );
        """)

        # Bảng hóa đơn (invoices)
        # `id` sẽ là khóa chính tự động tăng
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS invoices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            date TEXT NOT NULL
        );
        """)

        # Bảng chi tiết hóa đơn (invoice_items)
        # Liên kết giữa hóa đơn và sản phẩm
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS invoice_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            invoice_id INTEGER NOT NULL,
            product_id TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL,
            FOREIGN KEY (invoice_id) REFERENCES invoices (id) ON DELETE CASCADE,
            FOREIGN KEY (product_id) REFERENCES products (product_id) ON DELETE CASCADE
        );
        """)

        conn.commit()
        return True, f"Database đã được khởi tạo thành công tại: {DATABASE_PATH}"

    except sqlite3.Error as e:
        return False, f"Lỗi khi khởi tạo database: {e}"
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    # Chạy file này trực tiếp để tạo database
    print("Đang tiến hành khởi tạo database...")
    success, message = initialize_database()
    print(message)