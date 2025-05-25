#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Định nghĩa tùy chọn menu cho Hệ thống Quản lý Hóa đơn.
"""

from enum import Enum

class MenuOption(Enum):
    """
    Enum cho các tùy chọn menu chính trong Hệ thống Quản lý Hóa đơn.
    
    Thuộc tính:
        PRODUCT_MANAGEMENT (int): Tùy chọn cho quản lý sản phẩm
        INVOICE_MANAGEMENT (int): Tùy chọn cho quản lý hóa đơn
        STATISTICS (int): Tùy chọn cho thống kê
        EXIT (int): Tùy chọn để thoát ứng dụng
    """
    PRODUCT_MANAGEMENT = 1
    INVOICE_MANAGEMENT = 2
    STATISTICS = 3
    EXIT = 0 