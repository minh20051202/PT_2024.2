#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gói giao diện đồ họa (GUI) cho Hệ thống Quản lý Hóa đơn.
"""

# Đảm bảo import app_gui vào namespace hiện tại
from . import app_gui

# Xuất cụ thể hàm start_gui 
from .app_gui import start_gui

__all__ = ['app_gui', 'start_gui'] 