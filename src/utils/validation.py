#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Các hàm tiện ích kiểm tra dữ liệu cho Hệ thống Quản lý Hóa đơn.
"""

from typing import Any, Union, List
import re
from datetime import datetime

def validate_positive_number(value: Union[int, float], field_name: str) -> bool:
    """
    Kiểm tra một số là số dương.
    
    Tham số:
        value: Giá trị số cần kiểm tra
        field_name: Tên trường để hiển thị thông báo lỗi
        
    Trả về:
        True nếu hợp lệ, False nếu không
    """
    try:
        num_value = float(value)
        if num_value <= 0:
            print(f"Lỗi: {field_name} phải lớn hơn 0.")
            return False
        return True
    except (ValueError, TypeError):
        print(f"Lỗi: {field_name} phải là một số.")
        return False

def validate_required_field(value: Any, field_name: str) -> bool:
    """
    Kiểm tra một trường không được để trống.
    
    Tham số:
        value: Giá trị cần kiểm tra
        field_name: Tên trường để hiển thị thông báo lỗi
        
    Trả về:
        True nếu hợp lệ, False nếu không
    """
    if value is None or (isinstance(value, str) and not value.strip()):
        print(f"Lỗi: {field_name} là bắt buộc.")
        return False
    return True

def validate_string_length(value: str, field_name: str, min_length: int = 0, max_length: int = None) -> bool:
    """
    Kiểm tra độ dài của chuỗi.
    
    Tham số:
        value: Chuỗi cần kiểm tra
        field_name: Tên trường để hiển thị thông báo lỗi
        min_length: Độ dài tối thiểu
        max_length: Độ dài tối đa
        
    Trả về:
        True nếu hợp lệ, False nếu không
    """
    if not isinstance(value, str):
        print(f"Lỗi: {field_name} phải là chuỗi.")
        return False
        
    length = len(value.strip())
    if length < min_length:
        print(f"Lỗi: {field_name} phải có ít nhất {min_length} ký tự.")
        return False
    if max_length and length > max_length:
        print(f"Lỗi: {field_name} không được vượt quá {max_length} ký tự.")
        return False
    return True

def validate_date_format(date_str: str, field_name: str, format: str = "%Y-%m-%d") -> bool:
    """
    Kiểm tra định dạng ngày tháng.
    
    Tham số:
        date_str: Chuỗi ngày tháng cần kiểm tra
        field_name: Tên trường để hiển thị thông báo lỗi
        format: Định dạng ngày tháng (mặc định: YYYY-MM-DD)
        
    Trả về:
        True nếu hợp lệ, False nếu không
    """
    try:
        datetime.strptime(date_str, format)
        return True
    except ValueError:
        print(f"Lỗi: {field_name} phải có định dạng {format}.")
        return False

def validate_email(email: str) -> bool:
    """
    Kiểm tra định dạng email.
    
    Tham số:
        email: Email cần kiểm tra
        
    Trả về:
        True nếu hợp lệ, False nếu không
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        print("Lỗi: Email không hợp lệ.")
        return False
    return True

def validate_phone_number(phone: str) -> bool:
    """
    Kiểm tra định dạng số điện thoại Việt Nam.
    
    Tham số:
        phone: Số điện thoại cần kiểm tra
        
    Trả về:
        True nếu hợp lệ, False nếu không
    """
    pattern = r'^(0[3|5|7|8|9])+([0-9]{8})$'
    if not re.match(pattern, phone):
        print("Lỗi: Số điện thoại không hợp lệ.")
        return False
    return True

def validate_product_id(product_id: str) -> bool:
    """
    Kiểm tra định dạng mã sản phẩm.
    
    Tham số:
        product_id: Mã sản phẩm cần kiểm tra
        
    Trả về:
        True nếu hợp lệ, False nếu không
    """
    if not validate_required_field(product_id, "Mã sản phẩm"):
        return False
    if not validate_string_length(product_id, "Mã sản phẩm", 3, 10):
        return False
    if not re.match(r'^[A-Z0-9]+$', product_id):
        print("Lỗi: Mã sản phẩm chỉ được chứa chữ in hoa và số.")
        return False
    return True

def validate_quantity(quantity: Union[int, str]) -> bool:
    """
    Kiểm tra số lượng sản phẩm.
    
    Tham số:
        quantity: Số lượng cần kiểm tra
        
    Trả về:
        True nếu hợp lệ, False nếu không
    """
    try:
        qty = int(quantity)
        if qty <= 0:
            print("Lỗi: Số lượng phải lớn hơn 0.")
            return False
        if qty > 1000:
            print("Lỗi: Số lượng không được vượt quá 1000.")
            return False
        return True
    except (ValueError, TypeError):
        print("Lỗi: Số lượng phải là số nguyên.")
        return False 