#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quản lý sản phẩm cho Hệ thống Quản lý Hóa đơn.
"""

from typing import List, Optional
from models import Product
from .file_manager import FileManager
from utils import validate_positive_number, validate_required_field

class ProductManager:
    """
    Quản lý các thao tác với sản phẩm trong Hệ thống Quản lý Hóa đơn.
    
    Lớp này xử lý các thao tác như thêm, cập nhật, xóa và liệt kê sản phẩm.
    Sử dụng FileManager để lưu trữ dữ liệu.
    """
    
    def __init__(self):
        """Khởi tạo với danh sách sản phẩm trống và tải sản phẩm từ bộ nhớ."""
        self.file_manager = FileManager()
        self.products: List[Product] = []
        self.load_products()
    
    def load_products(self) -> None:
        """Tải sản phẩm từ bộ nhớ."""
        self.products = self.file_manager.load_products()
    
    def save_products(self) -> None:
        """Lưu sản phẩm vào bộ nhớ."""
        self.file_manager.save_products(self.products)
    
    def add_product(self, product_id: str, name: str, unit_price: float, 
                   category: str = "General", calculation_unit: str = "đơn vị") -> bool:
        """
        Thêm một sản phẩm mới.
        
        Tham số:
            product_id: Mã định danh duy nhất cho sản phẩm
            name: Tên sản phẩm
            unit_price: Đơn giá
            category: Danh mục sản phẩm (mặc định: "General")
            calculation_unit: Đơn vị tính (mặc định: "đơn vị")
            
        Trả về:
            True nếu thành công, False nếu không
        """
        # Validate inputs
        if not validate_required_field(product_id, "Mã sản phẩm"):
            return False
        if not validate_required_field(name, "Tên sản phẩm"):
            return False
        if not validate_positive_number(unit_price, "Đơn giá"):
            return False
        
        # Check if product with this ID already exists
        if any(product.product_id == product_id for product in self.products):
            print(f"Sản phẩm với Mã '{product_id}' đã tồn tại!")
            return False
        
        # Create and add the product
        product = Product(
            product_id=product_id,
            name=name,
            unit_price=unit_price,
            category=category,
            calculation_unit=calculation_unit
        )
        
        self.products.append(product)
        self.save_products()
        print(f"Đã thêm sản phẩm '{name}' thành công!")
        return True
    
    def find_product(self, product_id: str) -> Optional[Product]:
        """
        Tìm kiếm sản phẩm theo ID.
        
        Tham số:
            product_id: Mã sản phẩm cần tìm
            
        Trả về:
            Đối tượng sản phẩm nếu tìm thấy, None nếu không
        """
        for product in self.products:
            if product.product_id == product_id:
                return product
        return None
    
    def update_product(self, product_id: str, name: Optional[str] = None, 
                      unit_price: Optional[float] = None, category: Optional[str] = None, 
                      calculation_unit: Optional[str] = None) -> bool:
        """
        Cập nhật thông tin sản phẩm.
        
        Tham số:
            product_id: Mã sản phẩm cần cập nhật
            name: Tên sản phẩm mới (hoặc None để giữ nguyên)
            unit_price: Đơn giá mới (hoặc None để giữ nguyên)
            category: Danh mục mới (hoặc None để giữ nguyên)
            calculation_unit: Đơn vị tính mới (hoặc None để giữ nguyên)
            
        Trả về:
            True nếu thành công, False nếu không
        """
        product = self.find_product(product_id)
        if not product:
            print(f"Không tìm thấy sản phẩm với Mã '{product_id}'!")
            return False
        
        # Update fields if provided
        if name is not None:
            product.name = name
        if unit_price is not None:
            if not validate_positive_number(unit_price, "Đơn giá"):
                return False
            product.unit_price = unit_price
        if category is not None:
            product.category = category
        if calculation_unit is not None:
            product.calculation_unit = calculation_unit
        
        self.save_products()
        print(f"Đã cập nhật sản phẩm '{product_id}' thành công!")
        return True
    
    def delete_product(self, product_id: str) -> bool:
        """
        Xóa sản phẩm theo ID.
        
        Tham số:
            product_id: Mã sản phẩm cần xóa
            
        Trả về:
            True nếu thành công, False nếu không
        """
        product = self.find_product(product_id)
        if not product:
            print(f"Không tìm thấy sản phẩm với Mã '{product_id}'!")
            return False
        
        self.products.remove(product)
        self.save_products()
        print(f"Đã xóa sản phẩm '{product_id}' thành công!")
        return True
    
    def list_products(self) -> None:
        """Hiển thị danh sách sản phẩm."""
        if not self.products:
            print("Danh sách sản phẩm trống!")
            return
        
        print("\n" + "="*80)
        print(f"{'MÃ SP':<10} {'TÊN SẢN PHẨM':<30} {'DANH MỤC':<15} {'ĐƠN VỊ':<10} {'ĐƠN GIÁ':>10}")
        print("-"*80)
        
        for product in self.products:
            print(f"{product.product_id:<10} {product.name:<30} {product.category:<15} "
                  f"{product.calculation_unit:<10} {product.unit_price:>10,.2f}")
        
        print("="*80)
        print(f"Tổng số: {len(self.products)} sản phẩm")
        print("="*80) 