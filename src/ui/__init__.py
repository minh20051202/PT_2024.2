#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gói giao diện người dùng cho Hệ thống Quản lý Hóa đơn.
"""

# Đảm bảo các submodule có thể được truy cập
from . import gui
from . import cli

# Định nghĩa các module sẽ được import khi dùng "from invoicemanager.ui import *"
__all__ = ['gui', 'cli'] 