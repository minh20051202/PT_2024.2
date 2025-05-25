#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quản lý tệp tin cho Hệ thống Quản lý Hóa đơn.
Xử lý việc tải và lưu dữ liệu sản phẩm và hóa đơn.
"""

import os
import csv
import json
from typing import List, TYPE_CHECKING
from dataclasses import asdict

# Sử dụng TYPE_CHECKING để tránh import vòng tròn trong quá trình chạy
if TYPE_CHECKING:
    from .product_manager import ProductManager

from models import Product, Invoice, InvoiceItem
from utils import ensure_directory_exists

class FileManager:
    """Lớp quản lý file - Kỹ thuật: Mẫu thiết kế Singleton & Nhập/Xuất file"""
    _instance = None
    
    def __new__(cls):
        """Triển khai mẫu thiết kế Singleton"""
        if cls._instance is None:
            cls._instance = super(FileManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        # Thay đổi đường dẫn để sử dụng cấu trúc mới
        self.data_dir = os.path.join("src", "invoicemanager", "data")
        ensure_directory_exists(self.data_dir)
        self.products_file = os.path.join(self.data_dir, "products.json")
        self.invoices_file = os.path.join(self.data_dir, "invoices.json")
        # Đảm bảo các file dữ liệu tồn tại khi khởi tạo
        self._ensure_files_exist()
    
    def _ensure_files_exist(self):
        """Đảm bảo các file dữ liệu tồn tại - Kỹ thuật: Xử lý file"""
        for filename in [self.products_file, self.invoices_file]:
            # Kiểm tra nếu file không tồn tại
            if not os.path.exists(filename):
                try:
                    # Tạo file rỗng với định dạng JSON
                    with open(filename, 'w', encoding='utf-8') as f:
                        json.dump([], f, ensure_ascii=False, indent=2)
                    print(f"Đã tạo file dữ liệu '{filename}' rỗng.") # Thông báo khi tạo file
                except IOError as e:
                    print(f"Lỗi: Không thể tạo file dữ liệu '{filename}': {e}") # Xử lý lỗi khi tạo file
    
    def load_products(self) -> List[Product]:
        """Tải danh sách sản phẩm từ file - Kỹ thuật: Xử lý ngoại lệ & Phân tích cú pháp JSON"""
        try:
            # Mở file JSON để đọc
            with open(self.products_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Chuyển đổi dữ liệu JSON thành danh sách đối tượng Product
                return [Product(**item) for item in data]
        except FileNotFoundError:
            print(f"Lỗi: Không tìm thấy file sản phẩm '{self.products_file}'. Trả về danh sách rỗng.") # Thông báo khi không tìm thấy file
            return []
        except json.JSONDecodeError:
            print(f"Lỗi: File sản phẩm '{self.products_file}' có định dạng JSON không hợp lệ. Trả về danh sách rỗng.") # Thông báo khi lỗi định dạng JSON
            return []
        except Exception as e:
            print(f"Lỗi không mong muốn khi tải sản phẩm: {e}") # Xử lý các lỗi khác
            return []
    
    def save_products(self, products: List[Product]):
        """Lưu danh sách sản phẩm vào file - Kỹ thuật: Tuần tự hóa JSON"""
        try:
            # Mở file JSON để ghi (ghi đè)
            with open(self.products_file, 'w', encoding='utf-8') as f:
                # Chuyển đổi danh sách đối tượng Product thành định dạng JSON và ghi vào file
                json.dump([asdict(product) for product in products],
                         f, ensure_ascii=False, indent=2)
            # print(f"Đã lưu sản phẩm vào file '{self.products_file}' thành công.") # Có thể thêm thông báo thành công
        except IOError as e:
            print(f"Lỗi: Không thể lưu sản phẩm vào file '{self.products_file}': {e}") # Xử lý lỗi khi ghi file
        except Exception as e:
            print(f"Lỗi không mong muốn khi lưu sản phẩm: {e}") # Xử lý các lỗi khác
    
    def load_invoices(self) -> List[Invoice]:
        """Tải danh sách hóa đơn từ file"""
        try:
            # Mở file JSON để đọc
            with open(self.invoices_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                invoices = []
                # Duyệt qua dữ liệu hóa đơn và chuyển đổi thành đối tượng Invoice
                for invoice_data in data:
                    try:
                        # Chuyển đổi dữ liệu mặt hàng thành đối tượng InvoiceItem
                        items = [InvoiceItem(**item) for item in invoice_data.get('items', [])] # Sử dụng .get để tránh KeyError
                        # Tạo đối tượng Invoice
                        invoice = Invoice(
                            invoice_id=invoice_data.get('invoice_id'), # Sử dụng .get để tránh KeyError
                            date=invoice_data.get('date', ''), # Sử dụng .get để tránh KeyError, model sẽ xử lý ngày rỗng
                            customer_name=invoice_data.get('customer_name'), # Sử dụng .get để tránh KeyError
                            items=items
                        )
                        invoices.append(invoice)
                    except (TypeError, ValueError, KeyError) as e_item:
                        print(f"Cảnh báo: Bỏ qua dữ liệu hóa đơn không hợp lệ: {invoice_data} - Lỗi: {e_item}") # Thông báo khi bỏ qua dữ liệu hóa đơn lỗi
                return invoices
        except FileNotFoundError:
            print(f"Lỗi: Không tìm thấy file hóa đơn '{self.invoices_file}'. Trả về danh sách rỗng.") # Thông báo khi không tìm thấy file
            return []
        except json.JSONDecodeError:
            print(f"Lỗi: File hóa đơn '{self.invoices_file}' có định dạng JSON không hợp lệ. Trả về danh sách rỗng.") # Thông báo khi lỗi định dạng JSON
            return []
        except Exception as e:
            print(f"Lỗi không mong muốn khi tải hóa đơn: {e}") # Xử lý các lỗi khác
            return []
    
    def save_invoices(self, invoices: List[Invoice]):
        """Lưu danh sách hóa đơn vào file"""
        try:
            data = []
            # Chuyển đổi danh sách đối tượng Invoice thành định dạng dictionary
            for invoice in invoices:
                invoice_dict = asdict(invoice)
                # Đảm bảo các mặt hàng cũng là dictionary (đã được xử lý bởi asdict nếu InvoiceItem là dataclass)
                data.append(invoice_dict)
            
            # Mở file JSON để ghi (ghi đè)
            with open(self.invoices_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            # print(f"Đã lưu hóa đơn vào file '{self.invoices_file}' thành công.") # Có thể thêm thông báo thành công
        except IOError as e:
            print(f"Lỗi: Không thể lưu hóa đơn vào file '{self.invoices_file}': {e}") # Xử lý lỗi khi ghi file
        except Exception as e:
            print(f"Lỗi không mong muốn khi lưu hóa đơn: {e}") # Xử lý các lỗi khác
    
    def import_products_from_csv(self, filepath: str) -> List[Product]:
        """Nhập sản phẩm từ file CSV."""
        products = []
        try:
            # Mở file CSV để đọc
            with open(filepath, mode='r', encoding='utf-8', newline='') as file:
                reader = csv.DictReader(file)
                # Kiểm tra các cột bắt buộc trong header
                required_fields = ['product_id', 'name', 'unit_price']
                if not all(field in reader.fieldnames for field in required_fields):
                    print(f"Lỗi: File CSV thiếu các cột bắt buộc: {', '.join(required_fields)}")
                    return [] # Trả về danh sách rỗng nếu thiếu cột

                # Duyệt qua từng dòng trong file CSV
                for row in reader:
                    try:
                        # Tạo đối tượng Product từ dữ liệu dòng
                        product = Product(
                            product_id=row['product_id'],
                            name=row['name'],
                            unit_price=float(row['unit_price']),
                            category=row.get('category', 'General'), # Sử dụng .get cho trường tùy chọn
                            calculation_unit=row.get('calculation_unit', 'đơn vị') # Sử dụng .get cho trường tùy chọn
                        )
                        products.append(product)
                    except ValueError as ve:
                        print(f"Cảnh báo: Bỏ qua dòng do lỗi dữ liệu (chuyển đổi kiểu): {row} - Lỗi: {ve}") # Thông báo lỗi dữ liệu
                    except KeyError as ke:
                        print(f"Cảnh báo: Bỏ qua dòng do thiếu cột CSV: {row} - Lỗi: {ke}") # Thông báo lỗi thiếu cột
                    except Exception as e_row:
                        print(f"Cảnh báo: Bỏ qua dòng do lỗi không mong muốn: {row} - Lỗi: {e_row}") # Xử lý các lỗi khác trên từng dòng
        except FileNotFoundError:
            print(f"Lỗi: Không tìm thấy file tại đường dẫn '{filepath}'") # Thông báo khi không tìm thấy file
            return []
        except Exception as e:
            print(f"Đã xảy ra lỗi trong quá trình nhập CSV sản phẩm: {e}") # Xử lý các lỗi khác khi đọc file
            return []
        return products

    def export_products_to_csv(self, filepath: str, products: List[Product]):
        """Xuất sản phẩm ra file CSV."""
        try:
            # Mở file CSV để ghi (ghi đè)
            with open(filepath, mode='w', encoding='utf-8', newline='') as file:
                # Định nghĩa rõ ràng tên các cột
                fieldnames = ['product_id', 'name', 'unit_price', 'category', 'calculation_unit']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                
                # Ghi dòng tiêu đề
                writer.writeheader()
                
                # Ghi dữ liệu từng sản phẩm
                for product in products:
                    product_dict = asdict(product)
                    # Đảm bảo tất cả các cột đều có giá trị, cung cấp giá trị mặc định nếu thiếu
                    row_to_write = {field: product_dict.get(field, "") for field in fieldnames}
                    writer.writerow(row_to_write)
            print(f"Đã xuất sản phẩm thành công ra file '{filepath}'") # Thông báo thành công
        except IOError as e:
            print(f"Lỗi: Không thể xuất sản phẩm ra file '{filepath}': {e}") # Xử lý lỗi khi ghi file
        except Exception as e:
            print(f"Đã xảy ra lỗi trong quá trình xuất CSV sản phẩm: {e}") # Xử lý các lỗi khác

    def import_invoices_from_csv(self, filepath: str) -> List[Invoice]:
        """Nhập hóa đơn từ file CSV."""
        invoices = []
        try:
            # Mở file CSV để đọc
            with open(filepath, mode='r', encoding='utf-8', newline='') as file:
                reader = csv.DictReader(file)
                # Kiểm tra các cột bắt buộc trong header
                required_fields = ['invoice_id', 'date', 'customer_name', 'product_id', 'quantity', 'unit_price']
                if not all(field in reader.fieldnames for field in required_fields):
                    print(f"Lỗi: File CSV thiếu các cột bắt buộc: {', '.join(required_fields)}")
                    return [] # Trả về danh sách rỗng nếu thiếu cột

                # Duyệt qua từng dòng trong file CSV
                current_invoice = None
                invoice_items = []
                
                for row in reader:
                    try:
                        invoice_id = row['invoice_id']
                        date = row['date']
                        customer_name = row['customer_name']
                        
                        # Kiểm tra nếu là hóa đơn mới
                        if current_invoice is None or current_invoice.invoice_id != invoice_id:
                            # Lưu hóa đơn trước đó nếu có
                            if current_invoice is not None:
                                invoices.append(current_invoice)
                            
                            # Tạo hóa đơn mới
                            invoice_items = []
                            current_invoice = Invoice(
                                invoice_id=invoice_id,
                                date=date,
                                customer_name=customer_name,
                                items=invoice_items
                            )
                        
                        # Thêm mặt hàng vào hóa đơn
                        item = InvoiceItem(
                            product_id=row['product_id'],
                            quantity=int(row['quantity']),
                            unit_price=float(row['unit_price'])
                        )
                        invoice_items.append(item)
                    
                    except ValueError as ve:
                        print(f"Cảnh báo: Bỏ qua dòng do lỗi dữ liệu (chuyển đổi kiểu): {row} - Lỗi: {ve}") # Thông báo lỗi dữ liệu
                    except KeyError as ke:
                        print(f"Cảnh báo: Bỏ qua dòng do thiếu cột CSV: {row} - Lỗi: {ke}") # Thông báo lỗi thiếu cột
                    except Exception as e_row:
                        print(f"Cảnh báo: Bỏ qua dòng do lỗi không mong muốn: {row} - Lỗi: {e_row}") # Xử lý các lỗi khác trên từng dòng
                
                # Thêm hóa đơn cuối cùng nếu có
                if current_invoice is not None:
                    invoices.append(current_invoice)
                    
        except FileNotFoundError:
            print(f"Lỗi: Không tìm thấy file tại đường dẫn '{filepath}'") # Thông báo khi không tìm thấy file
            return []
        except Exception as e:
            print(f"Đã xảy ra lỗi trong quá trình nhập CSV hóa đơn: {e}") # Xử lý các lỗi khác khi đọc file
            return []
        return invoices

    def export_invoices_to_csv(self, filepath: str, invoices: List[Invoice]):
        """Xuất hóa đơn ra file CSV."""
        try:
            # Mở file CSV để ghi (ghi đè)
            with open(filepath, mode='w', encoding='utf-8', newline='') as file:
                # Định nghĩa rõ ràng tên các cột
                fieldnames = ['invoice_id', 'date', 'customer_name', 'product_id', 'quantity', 'unit_price', 'total_price']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                
                # Ghi dòng tiêu đề
                writer.writeheader()
                
                # Ghi dữ liệu từng hóa đơn và mặt hàng
                for invoice in invoices:
                    for item in invoice.items:
                        row = {
                            'invoice_id': invoice.invoice_id,
                            'date': invoice.date,
                            'customer_name': invoice.customer_name,
                            'product_id': item.product_id,
                            'quantity': item.quantity,
                            'unit_price': item.unit_price,
                            'total_price': item.total_price
                        }
                        writer.writerow(row)
            print(f"Đã xuất hóa đơn thành công ra file '{filepath}'") # Thông báo thành công
        except IOError as e:
            print(f"Lỗi: Không thể xuất hóa đơn ra file '{filepath}': {e}") # Xử lý lỗi khi ghi file
        except Exception as e:
            print(f"Đã xảy ra lỗi trong quá trình xuất CSV hóa đơn: {e}") # Xử lý các lỗi khác 