#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Điểm vào chính cho Hệ thống Quản lý Hóa đơn.
"""
import argparse
from ui.gui.app_gui import start_gui
from ui.cli.app_cli import start_cli

def show_usage():
    """Hiển thị thông tin sử dụng."""
    print("Cách sử dụng: python src/main.py [TÙY CHỌN]")
    print("Tùy chọn:")
    print("  --cli      Chạy ở chế độ giao diện dòng lệnh")
    print("  --gui      Chạy ở chế độ giao diện đồ họa (mặc định)")
    print("  --help     Hiển thị thông báo trợ giúp này")

def main():
    """Hàm chính quyết định chạy chế độ CLI hay GUI."""
    # Xử lý đối số dòng lệnh
    parser = argparse.ArgumentParser(description="Hệ thống Quản lý Hóa đơn")
    parser.add_argument('--cli', action='store_true', help='Chạy ở chế độ giao diện dòng lệnh')
    parser.add_argument('--gui', action='store_true', help='Chạy ở chế độ giao diện đồ họa (mặc định)')
    
    args = parser.parse_args()
    print("Đang khởi động Hệ thống Quản lý Hóa đơn...")
    # Nếu có cờ --cli, chạy chế độ CLI
    if args.cli:
        start_cli()
        return
            
    # Mặc định hoặc có cờ --gui, chạy chế độ GUI
    start_gui()
    return

if __name__ == "__main__":
    main() 