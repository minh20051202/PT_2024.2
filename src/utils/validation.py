#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Các hàm tiện ích kiểm tra dữ liệu cho Hệ thống Quản lý Hóa đơn.
"""

from typing import Any, Union, List, Tuple
import re
from datetime import datetime

def validate_positive_number(value: Union[int, float], field_name: str) -> Tuple[bool, str]:
    """
    Kiểm tra một số là số dương.

    Tham số:
        value: Giá trị số cần kiểm tra
        field_name: Tên trường để hiển thị thông báo lỗi

    Trả về:
        Tuple[bool, str]: (True/False, thông báo lỗi nếu có)
    """
    try:
        num_value = float(value)
        if num_value <= 0:
            return False, f"{field_name} phải lớn hơn 0."
        return True, ""
    except (ValueError, TypeError):
        return False, f"{field_name} phải là một số."

def validate_required_field(value: Any, field_name: str) -> Tuple[bool, str]:
    """
    Kiểm tra một trường không được để trống.

    Tham số:
        value: Giá trị cần kiểm tra
        field_name: Tên trường để hiển thị thông báo lỗi

    Trả về:
        Tuple[bool, str]: (True/False, thông báo lỗi nếu có)
    """
    if value is None or (isinstance(value, str) and not value.strip()):
        return False, f"{field_name} là bắt buộc."
    return True, ""

def validate_string_length(value: str, field_name: str, min_length: int = 0, max_length: int = None) -> Tuple[bool, str]:
    """
    Kiểm tra độ dài của chuỗi.

    Tham số:
        value: Chuỗi cần kiểm tra
        field_name: Tên trường để hiển thị thông báo lỗi
        min_length: Độ dài tối thiểu
        max_length: Độ dài tối đa

    Trả về:
        Tuple[bool, str]: (True/False, thông báo lỗi nếu có)
    """
    if not isinstance(value, str):
        return False, f"{field_name} phải là chuỗi."

    length = len(value.strip())
    if length < min_length:
        return False, f"{field_name} phải có ít nhất {min_length} ký tự."
    if max_length and length > max_length:
        return False, f"{field_name} không được vượt quá {max_length} ký tự."
    return True, ""

def validate_date_format(date_str: str, field_name: str, format: str = "%Y-%m-%d") -> Tuple[bool, str]:
    """
    Kiểm tra định dạng ngày tháng.

    Tham số:
        date_str: Chuỗi ngày tháng cần kiểm tra
        field_name: Tên trường để hiển thị thông báo lỗi
        format: Định dạng ngày tháng (mặc định: YYYY-MM-DD)

    Trả về:
        Tuple[bool, str]: (True/False, thông báo lỗi nếu có)
    """
    try:
        datetime.strptime(date_str, format)
        return True, ""
    except ValueError:
        return False, f"{field_name} phải có định dạng {format}."

def validate_email(email: str) -> Tuple[bool, str]:
    """
    Kiểm tra định dạng email.

    Tham số:
        email: Email cần kiểm tra

    Trả về:
        Tuple[bool, str]: (True/False, thông báo lỗi nếu có)
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        return False, "Email không hợp lệ."
    return True, ""

def validate_phone_number(phone: str) -> Tuple[bool, str]:
    """
    Kiểm tra định dạng số điện thoại Việt Nam.

    Tham số:
        phone: Số điện thoại cần kiểm tra

    Trả về:
        Tuple[bool, str]: (True/False, thông báo lỗi nếu có)
    """
    pattern = r'^(0[3|5|7|8|9])+([0-9]{8})$'
    if not re.match(pattern, phone):
        return False, "Số điện thoại không hợp lệ."
    return True, ""

def validate_product_id(product_id: str) -> Tuple[bool, str]:
    """
    Kiểm tra định dạng mã sản phẩm.

    Tham số:
        product_id: Mã sản phẩm cần kiểm tra

    Trả về:
        Tuple[bool, str]: (True/False, thông báo lỗi nếu có)
    """
    valid, error = validate_required_field(product_id, "Mã sản phẩm")
    if not valid:
        return False, error
    valid, error = validate_string_length(product_id, "Mã sản phẩm", 3, 10)
    if not valid:
        return False, error
    if not re.match(r'^[A-Z0-9]+$', product_id):
        return False, "Mã sản phẩm chỉ được chứa chữ in hoa và số."
    return True, ""

def validate_quantity(quantity: Union[int, str]) -> Tuple[bool, str]:
    """
    Kiểm tra số lượng sản phẩm.

    Tham số:
        quantity: Số lượng cần kiểm tra

    Trả về:
        Tuple[bool, str]: (True/False, thông báo lỗi nếu có)
    """
    try:
        qty = int(quantity)
        if qty <= 0:
            return False, "Số lượng phải lớn hơn 0."
        if qty > 1000:
            return False, "Số lượng không được vượt quá 1000."
        return True, ""
    except (ValueError, TypeError):
        return False, "Số lượng phải là số nguyên."