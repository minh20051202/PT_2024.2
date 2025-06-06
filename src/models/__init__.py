#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gói mô hình cho Hệ thống Quản lý Hóa đơn.
Chứa các mô hình dữ liệu cho sản phẩm, hóa đơn và tùy chọn menu.
"""

from .product import Product
from .invoice import Invoice, InvoiceItem

__all__ = ['Product', 'Invoice', 'InvoiceItem'] 