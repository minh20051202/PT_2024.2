#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Giao diện dòng lệnh (CLI) cho Hệ thống Quản lý Hóa đơn.
"""

from typing import List, Dict, Any

from models import MenuOption
from core.product_manager import ProductManager
from core.invoice_manager import InvoiceManager
from core.statistics_manager import StatisticsManager

class InvoiceManagementSystem:
    """Lớp ứng dụng chính - Kỹ thuật: Mẫu thiết kế Facade & Kiểm soát luồng chương trình"""
    
    def __init__(self):
        self.product_manager = ProductManager()
        self.invoice_manager = InvoiceManager(self.product_manager)
        self.statistics_manager = StatisticsManager(self.invoice_manager, self.product_manager)
    
    def display_main_menu(self):
        """Hiển thị menu chính - Kỹ thuật: Giao diện điều khiển bằng menu"""
        print("\n" + "="*60)
        print("      HỆ THỐNG QUẢN LÝ HÓA ĐƠN (CLI)") # Đã làm rõ CLI
        print("="*60)
        print(f"{MenuOption.PRODUCT_MANAGEMENT.value}. Quản lý sản phẩm")
        print(f"{MenuOption.INVOICE_MANAGEMENT.value}. Quản lý hóa đơn")
        print(f"{MenuOption.STATISTICS.value}. Thống kê")
        print(f"{MenuOption.EXIT.value}. Thoát")
        print("="*60)
    
    def display_product_menu(self):
        """Hiển thị menu quản lý sản phẩm"""
        print("\n" + "="*50)
        print("      QUẢN LÝ SẢN PHẨM")
        print("="*50)
        print("1. Thêm sản phẩm")
        print("2. Cập nhật sản phẩm")
        print("3. Xóa sản phẩm")
        print("4. Danh sách sản phẩm")
        print("0. Quay lại Menu chính")
        print("="*50)
    
    def display_invoice_menu(self):
        """Hiển thị menu quản lý hóa đơn"""
        print("\n" + "="*50)
        print("      QUẢN LÝ HÓA ĐƠN")
        print("="*50)
        print("1. Tạo hóa đơn")
        print("2. Xem chi tiết hóa đơn")
        print("3. Danh sách hóa đơn")
        print("0. Quay lại Menu chính")
        print("="*50)
    
    def display_statistics_menu(self):
        """Hiển thị menu thống kê"""
        print("\n" + "="*50)
        print("      THỐNG KÊ")
        print("="*50)
        print("1. Doanh thu theo ngày")
        print("2. Doanh thu theo sản phẩm")
        print("3. Khách hàng tiềm năng")
        print("0. Quay lại Menu chính")
        print("="*50)
    
    def get_input(self, prompt: str, input_type: Any = str, required: bool = True) -> Any:
        """Lấy và xác thực đầu vào từ người dùng - Kỹ thuật: Xác thực đầu vào"""
        while True:
            try:
                value = input(prompt).strip()
                if required and not value:
                    print("Trường này là bắt buộc!")
                    continue
                
                if not value and not required: # Nếu không bắt buộc và rỗng, trả về None hoặc giá trị mặc định cho kiểu
                    return None if input_type != str else ""
                
                if input_type == int:
                    return int(value)
                elif input_type == float:
                    return float(value)
                else: # str hoặc kiểu khác
                    return value
            except ValueError:
                type_name = "số" if input_type in [int, float] else "văn bản hợp lệ"
                print(f"Đầu vào không hợp lệ! Vui lòng nhập {type_name} hợp lệ.")
    
    def handle_product_management(self):
        """Xử lý các thao tác quản lý sản phẩm"""
        while True:
            self.display_product_menu()
            choice_input = self.get_input("Nhập lựa chọn của bạn: ", input_type=int, required=True)
            if choice_input is None: continue
            choice = choice_input

            if choice == 1:  # Thêm sản phẩm
                print("\n--- THÊM SẢN PHẨM MỚI ---")
                product_id = self.get_input("Mã sản phẩm: ")
                name = self.get_input("Tên sản phẩm: ")
                while True:
                    unit_price = self.get_input("Đơn giá: ", float)
                    if unit_price is not None and unit_price < 0:
                        print("Đơn giá không được âm. Vui lòng nhập lại.")
                        continue
                    break
                category_input = self.get_input("Danh mục (tùy chọn, mặc định: General): ", required=False)
                category = category_input if category_input else "General"
                calculation_unit_input = self.get_input("Đơn vị tính (tùy chọn, mặc định: đơn vị): ", required=False)
                calculation_unit = calculation_unit_input if calculation_unit_input else "đơn vị"
                self.product_manager.add_product(product_id, name, unit_price, category, calculation_unit)
            
            elif choice == 2:  # Cập nhật sản phẩm
                print("\n--- CẬP NHẬT SẢN PHẨM ---")
                product_id = self.get_input("Nhập Mã sản phẩm cần cập nhật: ")
                if not self.product_manager.find_product(product_id):
                    print(f"Không tìm thấy sản phẩm với Mã '{product_id}'.")
                    continue
                print("Để trống nếu không muốn thay đổi giá trị:")
                name = self.get_input("Tên sản phẩm mới: ", required=False) or None
                
                unit_price = None
                while True:
                    price_input = self.get_input("Đơn giá mới: ", required=False)
                    if price_input == "":
                        break # Keep current value
                    try:
                        unit_price_candidate = float(price_input)
                        if unit_price_candidate < 0:
                            print("Đơn giá không được âm. Vui lòng nhập lại.")
                            continue
                        unit_price = unit_price_candidate
                        break
                    except ValueError:
                        print("Đầu vào không hợp lệ! Vui lòng nhập một số hợp lệ.")
                        continue

                category = self.get_input("Danh mục mới: ", required=False) or None
                calculation_unit = self.get_input("Đơn vị tính mới: ", required=False) or None
                self.product_manager.update_product(product_id, name, unit_price, category, calculation_unit)
            
            elif choice == 3:  # Xóa sản phẩm
                print("\n--- XÓA SẢN PHẨM ---")
                product_id = self.get_input("Nhập Mã sản phẩm cần xóa: ")
                if not self.product_manager.find_product(product_id):
                    print(f"Không tìm thấy sản phẩm với Mã '{product_id}'.")
                    continue
                confirm = self.get_input(f"Bạn có chắc chắn muốn xóa sản phẩm '{product_id}'? (y/N): ", required=False)
                if confirm and confirm.lower() == 'y':
                    self.product_manager.delete_product(product_id)
                else:
                    print("Đã hủy thao tác xóa.")
            
            elif choice == 4:  # Danh sách sản phẩm
                self.product_manager.list_products()
            
            elif choice == 0:  # Quay lại menu chính
                break
            
            else:
                print("Lựa chọn không hợp lệ! Vui lòng thử lại.")
    
    def handle_invoice_management(self):
        """Xử lý các thao tác quản lý hóa đơn"""
        while True:
            self.display_invoice_menu()
            choice_input = self.get_input("Nhập lựa chọn của bạn: ", int, required=True)
            if choice_input is None: continue
            choice = choice_input
            
            if choice == 1:  # Tạo hóa đơn
                print("\n--- TẠO HÓA ĐƠN MỚI ---")
                invoice_id = self.get_input("Mã hóa đơn: ")
                customer_name = self.get_input("Tên khách hàng: ")
                
                items_data: List[Dict[str, Any]] = []
                print("\nThêm mặt hàng vào hóa đơn (nhập 'done' vào Mã sản phẩm để kết thúc):")
                while True:
                    product_id = self.get_input("Mã sản phẩm: ", required=False)
                    if not product_id: # Handle empty input
                         if not items_data:
                             print("Mã sản phẩm không được để trống khi thêm mặt hàng đầu tiên. Nhập 'done' để hủy tạo hóa đơn.")
                             continue
                         else:
                             print("Đã kết thúc thêm mặt hàng.")
                             break # Assume done if empty after adding items

                    if product_id.lower() == 'done':
                        break

                    product = self.product_manager.find_product(product_id)
                    if not product:
                        print(f"Không tìm thấy sản phẩm với Mã '{product_id}'!")
                        continue
                    
                    print(f"Sản phẩm: {product.name} - Giá: {product.unit_price:,.2f}")
                    while True:
                        quantity_input = self.get_input("Số lượng: ", int, required=True)
                        if quantity_input is not None and quantity_input <= 0:
                            print("Số lượng không hợp lệ. Phải là số nguyên dương.")
                            continue
                        break
                    quantity = quantity_input
                    
                    items_data.append({
                        'product_id': product_id,
                        'quantity': quantity
                    })
                
                if items_data:
                    self.invoice_manager.create_invoice(invoice_id, customer_name, items_data)
                else:
                    print("Không có mặt hàng nào được thêm vào hóa đơn! Hóa đơn chưa được tạo.")
            
            elif choice == 2:  # Xem chi tiết hóa đơn
                print("\n--- XEM CHI TIẾT HÓA ĐƠN ---")
                invoice_id = self.get_input("Nhập Mã hóa đơn: ")
                self.invoice_manager.view_invoice_detail(invoice_id)
            
            elif choice == 3:  # Danh sách hóa đơn
                self.invoice_manager.list_invoices()
            
            elif choice == 0:  # Quay lại menu chính
                break
            
            else:
                print("Lựa chọn không hợp lệ! Vui lòng thử lại.")
    
    def handle_statistics(self):
        """Xử lý các thao tác thống kê"""
        while True:
            self.display_statistics_menu()
            choice_input = self.get_input("Nhập lựa chọn của bạn: ", int, required=True)
            if choice_input is None: continue
            choice = choice_input
            
            if choice == 1:  # Doanh thu theo ngày
                self.statistics_manager.revenue_by_date()
            
            elif choice == 2:  # Doanh thu theo sản phẩm
                self.statistics_manager.revenue_by_product()
            
            elif choice == 3:  # Khách hàng tiềm năng
                limit_str = self.get_input("Nhập số lượng khách hàng để hiển thị (mặc định: 5): ", required=False)
                limit = int(limit_str) if limit_str else 5
                self.statistics_manager.top_customers(limit)
            
            elif choice == 0:  # Quay lại menu chính
                break
            
            else:
                print("Lựa chọn không hợp lệ! Vui lòng thử lại.")
    
    def run(self):
        """Chạy ứng dụng - Kỹ thuật: Vòng lặp chính & Xử lý lệnh"""
        print("Chào mừng đến với Hệ thống Quản lý Hóa đơn!")
        while True:
            self.display_main_menu()
            try:
                choice = int(input("Nhập lựa chọn của bạn: ").strip())
                
                if choice == MenuOption.PRODUCT_MANAGEMENT.value:
                    self.handle_product_management()
                
                elif choice == MenuOption.INVOICE_MANAGEMENT.value:
                    self.handle_invoice_management()
                
                elif choice == MenuOption.STATISTICS.value:
                    self.handle_statistics()
                
                elif choice == MenuOption.EXIT.value:
                    print("Cảm ơn bạn đã sử dụng Hệ thống Quản lý Hóa đơn. Tạm biệt!")
                    break
                
                else:
                    print("Lựa chọn không hợp lệ! Vui lòng thử lại.")
            
            except ValueError:
                print("Đầu vào không hợp lệ! Vui lòng nhập một số.")
            except KeyboardInterrupt:
                print("\nĐã hủy thao tác. Quay lại menu chính.")
            except Exception as e:
                print(f"Đã xảy ra lỗi không mong muốn: {e}")
                print("Vui lòng thử lại sau.")


def start_cli():
    """Hàm để chạy ứng dụng CLI"""
    app = InvoiceManagementSystem()
    app.run()
