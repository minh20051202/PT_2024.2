#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests tích hợp cho luồng làm việc chính của ứng dụng.
"""

import unittest
import sys
import os
import io
import tempfile
import json
from unittest.mock import patch

# Thêm thư mục gốc vào đường dẫn để import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.invoicemanager.core.file_manager import FileManager
from src.invoicemanager.core.product_manager import ProductManager
from src.invoicemanager.core.invoice_manager import InvoiceManager
from src.invoicemanager.core.statistics_manager import StatisticsManager

class TestMainWorkflow(unittest.TestCase):
    """Kiểm thử tích hợp cho luồng làm việc chính."""
    
    def setUp(self):
        """Thiết lập cho mỗi bài kiểm tra."""
        # Tạo thư mục tạm thời cho dữ liệu kiểm thử
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_data_dir = self.temp_dir.name
        
        # Chặn đường dẫn data_dir mặc định trong FileManager
        self.file_manager_patcher = patch('src.invoicemanager.core.file_manager.FileManager')
        self.mock_file_manager_class = self.file_manager_patcher.start()
        
        # Khởi tạo các file manager thật với đường dẫn thử nghiệm
        self.file_manager = FileManager()
        self.file_manager.data_dir = self.test_data_dir
        self.file_manager.products_file = os.path.join(self.test_data_dir, "products.json")
        self.file_manager.invoices_file = os.path.join(self.test_data_dir, "invoices.json")
        
        # Tạo các file dữ liệu trống
        for filename in [self.file_manager.products_file, self.file_manager.invoices_file]:
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump([], f)
        
        # Sử dụng instance file_manager thật thay vì mock
        self.mock_file_manager_class.return_value = self.file_manager
        
        # Khởi tạo các managers
        self.product_manager = ProductManager()
        self.invoice_manager = InvoiceManager(self.product_manager)
        self.statistics_manager = StatisticsManager(self.invoice_manager, self.product_manager)
    
    def tearDown(self):
        """Dọn dẹp sau mỗi bài kiểm tra."""
        # Dừng các patchers
        self.file_manager_patcher.stop()
        
        # Xóa thư mục tạm thời
        self.temp_dir.cleanup()
    
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_complete_workflow(self, mock_stdout):
        """Kiểm tra luồng làm việc hoàn chỉnh từ thêm sản phẩm đến xem thống kê."""
        # 1. Thêm các sản phẩm
        self.product_manager.add_product(
            product_id="P001",
            name="Laptop",
            unit_price=1000.0,
            category="Thiết bị điện tử",
            calculation_unit="chiếc"
        )
        
        self.product_manager.add_product(
            product_id="P002",
            name="Chuột không dây",
            unit_price=25.0,
            category="Phụ kiện",
            calculation_unit="cái"
        )
        
        # Kiểm tra số lượng sản phẩm đã thêm
        self.assertEqual(len(self.product_manager.products), 2)
        
        # 2. Tạo hóa đơn
        self.invoice_manager.create_invoice(
            invoice_id="INV001",
            customer_name="Nguyễn Văn A",
            items_data=[
                {"product_id": "P001", "quantity": 1},
                {"product_id": "P002", "quantity": 2}
            ]
        )
        
        self.invoice_manager.create_invoice(
            invoice_id="INV002",
            customer_name="Trần Thị B",
            items_data=[
                {"product_id": "P002", "quantity": 3}
            ]
        )
        
        # Kiểm tra số lượng hóa đơn đã tạo
        self.assertEqual(len(self.invoice_manager.invoices), 2)
        
        # 3. Kiểm tra thông tin hóa đơn
        invoice = self.invoice_manager.find_invoice("INV001")
        self.assertEqual(invoice.customer_name, "Nguyễn Văn A")
        self.assertEqual(len(invoice.items), 2)
        self.assertEqual(invoice.total_amount, 1000.0 + 2 * 25.0)  # 1050.0
        
        # 4. Cập nhật thông tin sản phẩm
        self.product_manager.update_product(
            product_id="P002",
            unit_price=30.0  # Tăng giá
        )
        
        # Kiểm tra giá đã cập nhật
        updated_product = self.product_manager.find_product("P002")
        self.assertEqual(updated_product.unit_price, 30.0)
        
        # 5. Kiểm tra tính toán thống kê
        # Các hóa đơn vẫn giữ giá cũ của sản phẩm khi tạo
        invoice1 = self.invoice_manager.find_invoice("INV001")
        self.assertEqual(invoice1.total_amount, 1050.0)  # Không đổi
        
        # 6. Thử xóa sản phẩm và kiểm tra
        self.product_manager.delete_product("P002")
        self.assertEqual(len(self.product_manager.products), 1)
        
        # 7. Kiểm tra lưu và tải dữ liệu
        # Tạo ProductManager mới để tải lại dữ liệu từ file
        # Lưu ý: Chúng ta không thể thực sự kiểm tra điều này với mock
        # Nhưng ít nhất chúng ta có thể kiểm tra rằng phương thức được gọi
        self.assertEqual(len(self.file_manager.load_products()), 1)
        
        # 8. Xem chi tiết hóa đơn và thống kê
        self.invoice_manager.view_invoice_detail("INV001")
        self.statistics_manager.revenue_by_product()
        
        # Kiểm tra thông báo có chứa thông tin chính xác
        stdout_content = mock_stdout.getvalue()
        self.assertIn("Nguyễn Văn A", stdout_content)
        self.assertIn("Laptop", stdout_content)
        self.assertIn("THỐNG KÊ DOANH THU THEO SẢN PHẨM", stdout_content)


# Bài kiểm tra thất bại tất cả các điều kiện xác thực
class TestAllValidationFailures(unittest.TestCase):
    """Kiểm thử tất cả các trường hợp xác thực thất bại."""
    
    def setUp(self):
        """Thiết lập cho mỗi bài kiểm tra."""
        # Tạo các mock cho các managers
        self.file_manager_patcher = patch('src.invoicemanager.core.product_manager.FileManager')
        self.product_manager_patcher = patch('src.invoicemanager.core.invoice_manager.ProductManager')
        
        self.mock_file_manager = self.file_manager_patcher.start().return_value
        self.mock_product_manager = self.product_manager_patcher.start()
        
        # Đặt giá trị trả về cho các phương thức load
        self.mock_file_manager.load_products.return_value = []
        self.mock_file_manager.load_invoices.return_value = []
        
        # Khởi tạo các managers
        self.product_manager = ProductManager()
        self.invoice_manager = InvoiceManager(self.mock_product_manager)
    
    def tearDown(self):
        """Dọn dẹp sau mỗi bài kiểm tra."""
        self.file_manager_patcher.stop()
        self.product_manager_patcher.stop()
    
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_all_validation_failures(self, mock_stdout):
        """Kiểm tra tất cả các trường hợp xác thực thất bại."""
        # Kiểm tra tất cả các trường hợp thất bại trong ProductManager
        
        # 1. ID sản phẩm rỗng
        result1 = self.product_manager.add_product("", "Sản phẩm test", 100.0)
        self.assertFalse(result1)
        
        # 2. Tên sản phẩm rỗng
        result2 = self.product_manager.add_product("P001", "", 100.0)
        self.assertFalse(result2)
        
        # 3. Đơn giá âm
        result3 = self.product_manager.add_product("P001", "Sản phẩm test", -10.0)
        self.assertFalse(result3)
        
        # 4. Cập nhật sản phẩm không tồn tại
        result4 = self.product_manager.update_product("P999", "Sản phẩm không tồn tại")
        self.assertFalse(result4)
        
        # 5. Xóa sản phẩm không tồn tại
        result5 = self.product_manager.delete_product("P999")
        self.assertFalse(result5)
        
        # Thiết lập mock cho product_manager.find_product
        self.mock_product_manager.find_product.return_value = None
        
        # Kiểm tra tất cả các trường hợp thất bại trong InvoiceManager
        
        # 6. ID hóa đơn rỗng
        result6 = self.invoice_manager.create_invoice("", "Khách hàng test", [{"product_id": "P001", "quantity": 1}])
        self.assertFalse(result6)
        
        # 7. Tên khách hàng rỗng
        result7 = self.invoice_manager.create_invoice("INV001", "", [{"product_id": "P001", "quantity": 1}])
        self.assertFalse(result7)
        
        # 8. Danh sách mặt hàng rỗng
        result8 = self.invoice_manager.create_invoice("INV001", "Khách hàng test", [])
        self.assertFalse(result8)
        
        # 9. Sản phẩm trong hóa đơn không tồn tại
        result9 = self.invoice_manager.create_invoice("INV001", "Khách hàng test", [{"product_id": "P999", "quantity": 1}])
        self.assertFalse(result9)
        
        # 10. Xem chi tiết hóa đơn không tồn tại
        result10 = self.invoice_manager.view_invoice_detail("INV999")
        self.assertFalse(result10)
        
        # Kiểm tra các thông báo lỗi
        output = mock_stdout.getvalue()
        self.assertIn("Lỗi: Mã sản phẩm là bắt buộc", output)
        self.assertIn("Lỗi: Tên sản phẩm là bắt buộc", output)
        self.assertIn("Lỗi: Đơn giá không được âm", output)
        self.assertIn("Không tìm thấy sản phẩm với Mã", output)
        self.assertIn("Lỗi: Mã hóa đơn là bắt buộc", output)
        self.assertIn("Lỗi: Tên khách hàng là bắt buộc", output)
        self.assertIn("Lỗi: Hóa đơn phải có ít nhất một mặt hàng", output)
        self.assertIn("Không tìm thấy hóa đơn với Mã", output)


if __name__ == "__main__":
    unittest.main() 