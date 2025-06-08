#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quản lý sản phẩm cho Hệ thống Quản lý Hóa đơn, sử dụng SQLite.

Module này cung cấp lớp ProductManager để thực hiện các thao tác
CRUD (Create, Read, Update, Delete) với sản phẩm trong database.
Tất cả dữ liệu được lưu trữ và truy xuất từ SQLite database.
"""
from typing import List, Optional

from models import Product
from utils.db_utils import load_data, save_data, update_data, delete_data
from utils.validation import (
    validate_required_field,
    validate_positive_number,
    validate_product_id,
    validate_string_length
)
from utils.formatting import format_product_id
from database.database import initialize_database

class ProductManager:
    """
    Quản lý các thao tác với sản phẩm, kết nối trực tiếp với database SQLite.
    """
    
    def __init__(self):
        """Khởi tạo và tải danh sách sản phẩm từ database."""
        self.products: List[Product] = []
        # Khởi tạo database nếu chưa tồn tại
        initialize_database()
        self.load_products()
    
    def load_products(self) -> tuple[bool, str]:
        """Tải tất cả sản phẩm từ database vào danh sách self.products."""
        self.products = []
        rows, error = load_data("products")
        if error:
            return False, error
        if rows:
            self.products = [Product(**row) for row in rows]
        return True, f"Đã tải {len(self.products)} sản phẩm từ database."

    def add_product(self, product_id: str, name: str, unit_price: float,
                   calculation_unit: str = "đơn vị", category: str = "Chung") -> tuple[bool, str]:
        """Thêm một sản phẩm mới vào database."""
        # Xác thực đầu vào
        valid, error = validate_product_id(product_id)
        if not valid:
            return False, error
        valid, error = validate_required_field(name, "Tên sản phẩm")
        if not valid:
            return False, error
        valid, error = validate_string_length(name, "Tên sản phẩm", 2, 50)
        if not valid:
            return False, error
        valid, error = validate_positive_number(unit_price, "Đơn giá")
        if not valid:
            return False, error
        if self.find_product(product_id):
            return False, f"Sản phẩm với Mã '{product_id}' đã tồn tại!"

        # Định dạng đầu vào
        product_id = format_product_id(product_id)
        
        # Thêm vào database
        success, error = save_data("products", {
            "product_id": product_id,
            "name": name,
            "unit_price": unit_price,
            "calculation_unit": calculation_unit,
            "category": category
        })

        if success:
            self.load_products()
            return True, f"Đã thêm sản phẩm '{name}' thành công!"
        return False, error
    
    def find_product(self, product_id: str) -> Optional[Product]:
        """Tìm kiếm sản phẩm theo ID trong danh sách đã tải."""
        product_id = format_product_id(product_id)
        for product in self.products:
            if product.product_id == product_id:
                return product
        return None
    
    def update_product(self, product_id: str, name: Optional[str] = None,
                      unit_price: Optional[float] = None, calculation_unit: Optional[str] = None,
                      category: Optional[str] = None) -> tuple[bool, str]:
        """Cập nhật thông tin sản phẩm trong database."""
        product_id = format_product_id(product_id)
        if not self.find_product(product_id):
            return False, f"Không tìm thấy sản phẩm với Mã '{product_id}'!"

        # Xác thực cập nhật
        if name is not None:
            valid, error = validate_string_length(name, "Tên sản phẩm", 2, 50)
            if not valid:
                return False, error
        if unit_price is not None:
            valid, error = validate_positive_number(unit_price, "Đơn giá")
            if not valid:
                return False, error
        
        # Xây dựng dữ liệu cập nhật
        update_data_dict = {}
        if name is not None:
            update_data_dict["name"] = name
        if unit_price is not None:
            update_data_dict["unit_price"] = unit_price
        if calculation_unit is not None:
            update_data_dict["calculation_unit"] = calculation_unit
        if category is not None:
            update_data_dict["category"] = category

        if not update_data_dict:
            return True, "Không có thông tin nào được cung cấp để cập nhật."

        success, error = update_data(
            "products",
            update_data_dict,
            {"product_id": product_id}
        )

        if success:
            self.load_products()
            return True, f"Đã cập nhật sản phẩm '{product_id}' thành công!"
        return False, error

    def delete_product(self, product_id: str) -> tuple[bool, str]:
        """Xóa sản phẩm khỏi database."""
        product_id = format_product_id(product_id)
        if not self.find_product(product_id):
            return False, f"Không tìm thấy sản phẩm với Mã '{product_id}'!"

        success, error = delete_data("products", {"product_id": product_id})

        if success:
            self.load_products()
            return True, f"Đã xóa sản phẩm '{product_id}' thành công!"
        return False, error
    
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