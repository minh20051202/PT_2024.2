#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gói ứng dụng chính cho Hệ thống Quản lý Hóa đơn.
"""

# Đảm bảo các submodule có thể được truy cập
from . import ui
from . import core
from . import models
from . import utils
from . import data

# Định nghĩa các module sẽ được import khi dùng "from invoicemanager import *"
__all__ = ['ui', 'core', 'models', 'utils', 'data']