#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quản lý sản phẩm cho Hệ thống Quản lý Hóa đơn, sử dụng SQLite.
"""
import sqlite3
from typing import List, Optional

from models import Product
from database.database import DATABASE_PATH

class ProductManager:
    """
    Quản lý các thao tác với sản phẩm, kết nối trực tiếp với database SQLite.
    """
    
    def __init__(self):
        """Khởi tạo và tải danh sách sản phẩm từ database."""
        self.db_path = DATABASE_PATH
        self.products: List[Product] = []
        self.load_products()
    
    def _get_connection(self):
        """Tạo và trả về một kết nối đến database."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Trả về kết quả dạng dict-like
        return conn

    def load_products(self) -> None:
        """Tải tất cả sản phẩm từ database vào danh sách self.products."""
        self.products = []
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM products ORDER BY name;")
                rows = cursor.fetchall()
                for row in rows:
                    self.products.append(Product(**dict(row)))
            print(f"Đã tải {len(self.products)} sản phẩm từ database.")
        except sqlite3.Error as e:
            print(f"Lỗi khi tải sản phẩm từ database: {e}")

    def add_product(self, product_id: str, name: str, unit_price: float, 
                   calculation_unit: str = "đơn vị", category: str = "General") -> bool:
        """Thêm một sản phẩm mới vào database."""
        if not product_id or not name:
            print("Lỗi: Mã sản phẩm và tên là bắt buộc.")
            return False
        if unit_price < 0:
            print("Lỗi: Đơn giá không được âm.")
            return False
        if self.find_product(product_id):
            print(f"Sản phẩm với Mã '{product_id}' đã tồn tại!")
            return False

        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO products (product_id, name, unit_price, calculation_unit, category)
                    VALUES (?, ?, ?, ?, ?)
                """, (product_id, name, unit_price, calculation_unit, category))
                conn.commit()
            
            # Tải lại danh sách sau khi thêm
            self.load_products()
            print(f"Đã thêm sản phẩm '{name}' thành công!")
            return True
        except sqlite3.Error as e:
            print(f"Lỗi database khi thêm sản phẩm: {e}")
            return False
    
    def find_product(self, product_id: str) -> Optional[Product]:
        """Tìm kiếm sản phẩm theo ID trong danh sách đã tải."""
        for product in self.products:
            if product.product_id == product_id:
                return product
        return None
    
    def update_product(self, product_id: str, name: Optional[str] = None, 
                      unit_price: Optional[float] = None, calculation_unit: Optional[str] = None, 
                      category: Optional[str] = None) -> bool:
        """Cập nhật thông tin sản phẩm trong database."""
        product = self.find_product(product_id)
        if not product:
            print(f"Không tìm thấy sản phẩm với Mã '{product_id}'!")
            return False
        
        # Tạo câu lệnh UPDATE động
        fields_to_update = []
        params = []
        if name is not None:
            fields_to_update.append("name = ?")
            params.append(name)
        if unit_price is not None:
            if unit_price < 0:
                print("Lỗi: Đơn giá không được âm.")
                return False
            fields_to_update.append("unit_price = ?")
            params.append(unit_price)
        if calculation_unit is not None:
            fields_to_update.append("calculation_unit = ?")
            params.append(calculation_unit)
        if category is not None:
            fields_to_update.append("category = ?")
            params.append(category)

        if not fields_to_update:
            print("Không có thông tin nào được cung cấp để cập nhật.")
            return True

        # Thêm product_id vào cuối params cho mệnh đề WHERE
        params.append(product_id)
        
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                sql = f"UPDATE products SET {', '.join(fields_to_update)} WHERE product_id = ?"
                cursor.execute(sql, tuple(params))
                conn.commit()

            # Tải lại danh sách sau khi cập nhật
            self.load_products()
            print(f"Đã cập nhật sản phẩm '{product_id}' thành công!")
            return True
        except sqlite3.Error as e:
            print(f"Lỗi database khi cập nhật sản phẩm: {e}")
            return False

    def delete_product(self, product_id: str) -> bool:
        """Xóa sản phẩm khỏi database."""
        if not self.find_product(product_id):
            print(f"Không tìm thấy sản phẩm với Mã '{product_id}'!")
            return False
        
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM products WHERE product_id = ?", (product_id,))
                conn.commit()

            # Tải lại danh sách sau khi xóa
            self.load_products()
            print(f"Đã xóa sản phẩm '{product_id}' thành công!")
            return True
        except sqlite3.Error as e:
            print(f"Lỗi database khi xóa sản phẩm: {e}")
            return False
    
    def list_products(self) -> None:
        """Hiển thị danh sách sản phẩm (dùng cho CLI)."""
        if not self.products:
            print("Danh sách sản phẩm trống!")
            return
        
        print("\n" + "="*80)
        print(f"{'MÃ SP':<10} {'TÊN SẢN PHẨM':<30} {'ĐƠN VỊ':<10} {'DANH MỤC':<15} {'ĐƠN GIÁ':>10}")
        print("-"*80)
        
        for product in self.products:
            print(f"{product.product_id:<10} {product.name:<30} {product.calculation_unit:<10} "
                  f"{product.category:<15} {product.unit_price:>10,.2f}")
        
        print("="*80)
        print(f"Tổng số: {len(self.products)} sản phẩm")
        print("="*80) 