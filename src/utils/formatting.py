#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Các hàm tiện ích định dạng cho Hệ thống Quản lý Hóa đơn.
"""

def format_currency(amount: float) -> str:
    """
    Định dạng số tiền với dấu phân cách hàng nghìn và hai chữ số thập phân.
    
    Tham số:
        amount: Số tiền cần định dạng
        
    Trả về:
        Chuỗi định dạng của số tiền
    """
    return f"{amount:,.2f}" 