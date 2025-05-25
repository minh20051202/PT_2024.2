#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Các hàm tiện ích xử lý tệp tin cho Hệ thống Quản lý Hóa đơn.
"""

import os

def ensure_directory_exists(directory_path: str) -> None:
    """
    Đảm bảo một thư mục tồn tại, tạo nó nếu chưa có.
    
    Tham số:
        directory_path: Đường dẫn của thư mục cần kiểm tra/tạo
        
    Trả về:
        None
    """
    if not os.path.exists(directory_path):
        os.makedirs(directory_path) 