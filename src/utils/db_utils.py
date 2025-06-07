#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Các hàm tiện ích xử lý database cho Hệ thống Quản lý Hóa đơn.
"""

import sqlite3
import os
from typing import Any, List, Dict, Optional, Tuple
from database.database import DATABASE_PATH

def ensure_database_exists() -> Tuple[bool, str]:
    """
    Đảm bảo database file tồn tại và có thể truy cập.

    Trả về:
        Tuple[bool, str]: (True/False, thông báo lỗi nếu có)
    """
    try:
        # Kiểm tra thư mục chứa database
        db_dir = os.path.dirname(DATABASE_PATH)
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)
        return True, ""
    except (OSError, IOError) as e:
        return False, f"Lỗi khi kiểm tra database: {e}"

def save_data(table: str, data: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Lưu dữ liệu vào bảng.

    Tham số:
        table: Tên bảng
        data: Dữ liệu cần lưu (dạng dict)

    Trả về:
        Tuple[bool, str]: (True/False, thông báo lỗi nếu có)
    """
    db_ok, db_error = ensure_database_exists()
    if not db_ok:
        return False, db_error

    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        # Tạo câu lệnh INSERT
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in data])
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"

        cursor.execute(query, tuple(data.values()))
        conn.commit()
        conn.close()
        return True, ""
    except sqlite3.Error as e:
        return False, f"Lỗi khi lưu dữ liệu vào bảng {table}: {e}"

def load_data(table: str, conditions: Dict[str, Any] = None) -> Tuple[List[Dict[str, Any]], str]:
    """
    Tải dữ liệu từ bảng.

    Tham số:
        table: Tên bảng
        conditions: Điều kiện lọc (dạng dict)

    Trả về:
        Tuple[List[Dict], str]: (Danh sách bản ghi, thông báo lỗi nếu có)
    """
    db_ok, db_error = ensure_database_exists()
    if not db_ok:
        return [], db_error

    try:
        conn = sqlite3.connect(DATABASE_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Tạo câu lệnh SELECT
        query = f"SELECT * FROM {table}"
        params = []

        if conditions:
            where_clauses = []
            for key, value in conditions.items():
                where_clauses.append(f"{key} = ?")
                params.append(value)
            if where_clauses:
                query += " WHERE " + " AND ".join(where_clauses)

        cursor.execute(query, params)
        results = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return results, ""
    except sqlite3.Error as e:
        return [], f"Lỗi khi tải dữ liệu từ bảng {table}: {e}"

def update_data(table: str, data: Dict[str, Any], conditions: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Cập nhật dữ liệu trong bảng.

    Tham số:
        table: Tên bảng
        data: Dữ liệu cần cập nhật (dạng dict)
        conditions: Điều kiện cập nhật (dạng dict)

    Trả về:
        Tuple[bool, str]: (True/False, thông báo lỗi nếu có)
    """
    db_ok, db_error = ensure_database_exists()
    if not db_ok:
        return False, db_error

    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        # Tạo câu lệnh UPDATE
        set_clauses = [f"{key} = ?" for key in data.keys()]
        where_clauses = [f"{key} = ?" for key in conditions.keys()]

        query = f"UPDATE {table} SET {', '.join(set_clauses)} WHERE {' AND '.join(where_clauses)}"
        params = list(data.values()) + list(conditions.values())

        cursor.execute(query, params)
        conn.commit()
        conn.close()
        return True, ""
    except sqlite3.Error as e:
        return False, f"Lỗi khi cập nhật dữ liệu trong bảng {table}: {e}"

def delete_data(table: str, conditions: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Xóa dữ liệu từ bảng.

    Tham số:
        table: Tên bảng
        conditions: Điều kiện xóa (dạng dict)

    Trả về:
        Tuple[bool, str]: (True/False, thông báo lỗi nếu có)
    """
    db_ok, db_error = ensure_database_exists()
    if not db_ok:
        return False, db_error

    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        # Tạo câu lệnh DELETE
        where_clauses = [f"{key} = ?" for key in conditions.keys()]
        query = f"DELETE FROM {table} WHERE {' AND '.join(where_clauses)}"

        cursor.execute(query, list(conditions.values()))
        conn.commit()
        conn.close()
        return True, ""
    except sqlite3.Error as e:
        return False, f"Lỗi khi xóa dữ liệu từ bảng {table}: {e}"