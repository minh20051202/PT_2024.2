#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mô hình Sản phẩm cho Hệ thống Quản lý Hóa đơn.
"""

from dataclasses import dataclass, field

@dataclass
class Product:
    """
    Mô hình dữ liệu Sản phẩm.
    
    Thuộc tính:
        product_id (str): Định danh duy nhất cho sản phẩm
        name (str): Tên sản phẩm
        unit_price (float): Giá mỗi đơn vị
        category (str): Danh mục sản phẩm (mặc định: "General")
        calculation_unit (str): Đơn vị tính (mặc định: "đơn vị")
    """
    product_id: str
    name: str
    unit_price: float
    calculation_unit: str = field(default="đơn vị")
    category: str = field(default="General")
    
    def __post_init__(self):
        """Xác thực dữ liệu sản phẩm."""
        if not self.product_id or not self.name:
            raise ValueError("Mã sản phẩm và tên không được để trống")
        if self.unit_price < 0:
            raise ValueError("Đơn giá không được âm")
        # Có thể thêm xác thực cho calculation_unit nếu cần 