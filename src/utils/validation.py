#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Các hàm tiện ích kiểm tra dữ liệu cho Hệ thống Quản lý Hóa đơn.
"""

from typing import Any

def validate_positive_number(value: float, field_name: str) -> bool:
    """
    Kiểm tra một số là số dương.
    
    Tham số:
        value: Giá trị số cần kiểm tra
        field_name: Tên trường để hiển thị thông báo lỗi
        
    Trả về:
        True nếu hợp lệ, False nếu không
    """
    if value < 0:
        print(f"Lỗi: {field_name} không được âm.")
        return False
    return True

def validate_required_field(value: Any, field_name: str) -> bool:
    """
    Kiểm tra một trường không được để trống.
    
    Tham số:
        value: Giá trị cần kiểm tra
        field_name: Tên trường để hiển thị thông báo lỗi
        
    Trả về:
        True nếu hợp lệ, False nếu không
    """
    if not value:
        print(f"Lỗi: {field_name} là bắt buộc.")
        return False
    return True 