#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Các hàm tiện ích xử lý tệp tin cho Hệ thống Quản lý Hóa đơn.
"""

import os
import json
import shutil
from typing import Any, Dict, List, Optional
from datetime import datetime

def ensure_directory_exists(directory_path: str) -> bool:
    """
    Đảm bảo một thư mục tồn tại, tạo nó nếu chưa có.
    
    Tham số:
        directory_path: Đường dẫn của thư mục cần kiểm tra/tạo
        
    Trả về:
        True nếu thành công, False nếu thất bại
    """
    try:
        os.makedirs(directory_path, exist_ok=True)
        return True
    except (OSError, IOError) as e:
        print(f"Lỗi khi tạo thư mục {directory_path}: {e}")
        return False

def safe_write_json(data: Any, file_path: str, backup: bool = True) -> bool:
    """
    Ghi dữ liệu JSON vào file một cách an toàn.
    
    Tham số:
        data: Dữ liệu cần ghi
        file_path: Đường dẫn file
        backup: Có tạo bản sao lưu không
        
    Trả về:
        True nếu thành công, False nếu thất bại
    """
    try:
        # Tạo bản sao lưu nếu cần
        if backup and os.path.exists(file_path):
            backup_path = f"{file_path}.{datetime.now().strftime('%Y%m%d_%H%M%S')}.bak"
            shutil.copy2(file_path, backup_path)
        
        # Đảm bảo thư mục tồn tại
        ensure_directory_exists(os.path.dirname(file_path))
        
        # Ghi file tạm
        temp_path = f"{file_path}.tmp"
        with open(temp_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        # Di chuyển file tạm vào vị trí cuối cùng
        shutil.move(temp_path, file_path)
        return True
    except (OSError, IOError, json.JSONDecodeError) as e:
        print(f"Lỗi khi ghi file {file_path}: {e}")
        # Xóa file tạm nếu có
        if os.path.exists(temp_path):
            os.remove(temp_path)
        return False

def safe_read_json(file_path: str, default: Any = None) -> Any:
    """
    Đọc dữ liệu JSON từ file một cách an toàn.
    
    Tham số:
        file_path: Đường dẫn file
        default: Giá trị mặc định nếu đọc thất bại
        
    Trả về:
        Dữ liệu đọc được hoặc giá trị mặc định
    """
    try:
        if not os.path.exists(file_path):
            return default
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (OSError, IOError, json.JSONDecodeError) as e:
        print(f"Lỗi khi đọc file {file_path}: {e}")
        return default

def get_file_size(file_path: str) -> Optional[int]:
    """
    Lấy kích thước file.
    
    Tham số:
        file_path: Đường dẫn file
        
    Trả về:
        Kích thước file (bytes) hoặc None nếu lỗi
    """
    try:
        return os.path.getsize(file_path)
    except (OSError, IOError) as e:
        print(f"Lỗi khi lấy kích thước file {file_path}: {e}")
        return None

def is_file_readable(file_path: str) -> bool:
    """
    Kiểm tra file có thể đọc được không.
    
    Tham số:
        file_path: Đường dẫn file
        
    Trả về:
        True nếu có thể đọc, False nếu không
    """
    return os.path.isfile(file_path) and os.access(file_path, os.R_OK)

def is_file_writable(file_path: str) -> bool:
    """
    Kiểm tra file có thể ghi được không.
    
    Tham số:
        file_path: Đường dẫn file
        
    Trả về:
        True nếu có thể ghi, False nếu không
    """
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        return os.access(os.path.dirname(directory), os.W_OK)
    return os.access(directory, os.W_OK) 