#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quản lý sản phẩm cho Hệ thống Quản lý Hóa đơn, sử dụng SQLite.
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

class ProductManager:
    """
    Quản lý các thao tác với sản phẩm, kết nối trực tiếp với database SQLite.
    """
    
    def __init__(self):
        """Khởi tạo và tải danh sách sản phẩm từ database."""
        self.products: List[Product] = []
        self.load_products()
    
    def load_products(self) -> None:
        """Tải tất cả sản phẩm từ database vào danh sách self.products."""
        self.products = []
        rows = load_data("products")
        if rows:
            self.products = [Product(**row) for row in rows]
            print(f"Đã tải {len(self.products)} sản phẩm từ database.")

    def add_product(self, product_id: str, name: str, unit_price: float, 
                   calculation_unit: str = "đơn vị", category: str = "General") -> bool:
        """Thêm một sản phẩm mới vào database."""
        # Validate input
        if not validate_product_id(product_id):
            return False
        if not validate_required_field(name, "Tên sản phẩm"):
            return False
        if not validate_string_length(name, "Tên sản phẩm", 2, 50):
            return False
        if not validate_positive_number(unit_price, "Đơn giá"):
            return False
        if self.find_product(product_id):
            print(f"Sản phẩm với Mã '{product_id}' đã tồn tại!")
            return False

        # Format input
        product_id = format_product_id(product_id)
        
        # Add to database
        success = save_data("products", {
            "product_id": product_id,
            "name": name,
            "unit_price": unit_price,
            "calculation_unit": calculation_unit,
            "category": category
        })
        
        if success:
            self.load_products()
            print(f"Đã thêm sản phẩm '{name}' thành công!")
            return True
        return False
    
    def find_product(self, product_id: str) -> Optional[Product]:
        """Tìm kiếm sản phẩm theo ID trong danh sách đã tải."""
        product_id = format_product_id(product_id)
        for product in self.products:
            if product.product_id == product_id:
                return product
        return None
    
    def update_product(self, product_id: str, name: Optional[str] = None, 
                      unit_price: Optional[float] = None, calculation_unit: Optional[str] = None, 
                      category: Optional[str] = None) -> bool:
        """Cập nhật thông tin sản phẩm trong database."""
        product_id = format_product_id(product_id)
        if not self.find_product(product_id):
            print(f"Không tìm thấy sản phẩm với Mã '{product_id}'!")
            return False
        
        # Validate updates
        if name is not None and not validate_string_length(name, "Tên sản phẩm", 2, 50):
            return False
        if unit_price is not None and not validate_positive_number(unit_price, "Đơn giá"):
            return False
        
        # Build update data
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
            print("Không có thông tin nào được cung cấp để cập nhật.")
            return True

        success = update_data(
            "products",
            update_data_dict,
            {"product_id": product_id}
        )
        
        if success:
            self.load_products()
            print(f"Đã cập nhật sản phẩm '{product_id}' thành công!")
            return True
        return False

    def delete_product(self, product_id: str) -> bool:
        """Xóa sản phẩm khỏi database."""
        product_id = format_product_id(product_id)
        if not self.find_product(product_id):
            print(f"Không tìm thấy sản phẩm với Mã '{product_id}'!")
            return False
        
        success = delete_data("products", {"product_id": product_id})
        
        if success:
            self.load_products()
            print(f"Đã xóa sản phẩm '{product_id}' thành công!")
            return True
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