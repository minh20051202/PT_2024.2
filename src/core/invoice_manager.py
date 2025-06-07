#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quản lý hóa đơn cho Hệ thống Quản lý Hóa đơn, sử dụng SQLite.
"""
from datetime import datetime
from typing import List, Optional, Dict, Any

from models import Invoice, InvoiceItem
from utils.db_utils import load_data, save_data, update_data, delete_data
from utils.validation import (
    validate_required_field,
    validate_date_format,
    validate_quantity
)
from utils.formatting import format_date, format_customer_name
from database.database import initialize_database
from .product_manager import ProductManager

class InvoiceManager:
    """
    Quản lý các thao tác với hóa đơn, kết nối trực tiếp với database SQLite.
    """
    
    def __init__(self, product_manager: ProductManager):
        """Khởi tạo và tải hóa đơn từ database."""
        self.product_manager = product_manager
        self.invoices: List[Invoice] = []
        # Khởi tạo database nếu chưa tồn tại
        initialize_database()
        self.load_invoices()

    def load_invoices(self) -> tuple[bool, str]:
        """Tải tất cả hóa đơn và các mục chi tiết từ database."""
        self.invoices = []

        # Load invoices
        invoice_rows, error = load_data("invoices")
        if error:
            return False, error
        if not invoice_rows:
            return True, "Đã tải 0 hóa đơn từ database."

        for inv_row in invoice_rows:
            invoice_id = inv_row['id']

            # Load invoice items
            item_rows, error = load_data("invoice_items", {"invoice_id": invoice_id})
            if error:
                return False, error

            items = [
                InvoiceItem(
                    product_id=row['product_id'],
                    quantity=row['quantity'],
                    unit_price=row['unit_price']
                )
                for row in item_rows
            ] if item_rows else []

            # Create Invoice object
            invoice = Invoice(
                invoice_id=str(invoice_id),
                customer_name=inv_row['customer_name'],
                date=inv_row['date'],
                items=items
            )
            self.invoices.append(invoice)

        return True, f"Đã tải {len(self.invoices)} hóa đơn từ database."

    def create_invoice(self, customer_name: str, items_data: List[Dict[str, Any]], date: Optional[str] = None) -> tuple[Optional[Invoice], str]:
        """
        Tạo một hóa đơn mới trong database.
        Lưu ý: invoice_id sẽ được database tự động tạo.

        Trả về:
            tuple[Optional[Invoice], str]: (Invoice object nếu thành công, thông báo lỗi nếu có)
        """
        # Validate input
        valid, error = validate_required_field(customer_name, "Tên khách hàng")
        if not valid:
            return None, error
        if not items_data:
            return None, "Hóa đơn phải có ít nhất một mặt hàng."

        # Validate date format
        invoice_date = date if date else datetime.now().strftime('%Y-%m-%d')
        valid, error = validate_date_format(invoice_date, "Ngày hóa đơn")
        if not valid:
            return None, error
            
        # Format input
        customer_name = format_customer_name(customer_name)
        
        # Validate items
        for item in items_data:
            valid, error = validate_quantity(item.get('quantity'))
            if not valid:
                return None, error
            if not self.product_manager.find_product(item.get('product_id')):
                return None, f"Sản phẩm với ID {item.get('product_id')} không tồn tại."
        
        # Insert invoice
        invoice_data = {
            "customer_name": customer_name,
            "date": invoice_date
        }
        
        success, error = save_data("invoices", invoice_data)
        if not success:
            return None, error

        # Get the new invoice ID
        new_invoice, error = load_data("invoices", {"customer_name": customer_name, "date": invoice_date})
        if error:
            return None, error
        if not new_invoice:
            return None, "Không thể tìm thấy hóa đơn vừa tạo."
            
        new_invoice_id = new_invoice[0]['id']
        
        # Insert items
        for item_data in items_data:
            product = self.product_manager.find_product(item_data['product_id'])
            item_data = {
                "invoice_id": new_invoice_id,
                "product_id": item_data['product_id'],
                "quantity": item_data['quantity'],
                "unit_price": product.unit_price
            }
            success, error = save_data("invoice_items", item_data)
            if not success:
                return None, error

        self.load_invoices()
        new_invoice = self.find_invoice(str(new_invoice_id))
        if new_invoice:
            return new_invoice, f"Đã tạo thành công hóa đơn #{new_invoice.invoice_id} cho khách hàng '{customer_name}'."
        return None, "Không thể tạo hóa đơn."

    def find_invoice(self, invoice_id: str) -> Optional[Invoice]:
        """Tìm một hóa đơn theo ID trong danh sách đã tải."""
        for invoice in self.invoices:
            if invoice.invoice_id == invoice_id:
                return invoice
        return None
    
    def view_invoice_detail(self, invoice_id: str) -> None:
        """Hiển thị chi tiết hóa đơn (dùng cho CLI)."""
        invoice = self.find_invoice(invoice_id)
        if not invoice:
            print(f"Không tìm thấy hóa đơn với Mã '{invoice_id}'.")
            return

        print("\n" + "="*80)
        print(f"CHI TIẾT HÓA ĐƠN #{invoice.invoice_id}")
        print(f"Khách hàng: {invoice.customer_name}")
        print(f"Ngày: {format_date(invoice.date)}")
        print("="*80)
        print(f"{'MÃ SP':<10} {'TÊN SẢN PHẨM':<30} {'SL':>5} {'ĐƠN GIÁ':>15} {'THÀNH TIỀN':>15}")
        print("-"*80)

        for item in invoice.items:
            product = self.product_manager.find_product(item.product_id)
            product_name = product.name if product else "[Sản phẩm đã bị xóa]"
            total_price = item.quantity * item.unit_price
            print(f"{item.product_id:<10} {product_name:<30} {item.quantity:>5} "
                  f"{item.unit_price:>15,.2f} {total_price:>15,.2f}")
        
        print("-"*80)
        print(f"{'TỔNG CỘNG:':<64} {invoice.total_amount:>15,.2f}")
        print("="*80)

    def list_invoices(self) -> None:
        """Hiển thị danh sách hóa đơn (dùng cho CLI)."""
        if not self.invoices:
            print("Danh sách hóa đơn trống!")
            return
        
        print("\n" + "="*80)
        print(f"{'MÃ HĐ':<10} {'KHÁCH HÀNG':<30} {'NGÀY':<15} {'SỐ MẶT HÀNG':>15} {'TỔNG TIỀN':>15}")
        print("-"*80)
        
        for invoice in self.invoices:
            print(f"#{invoice.invoice_id:<9} {invoice.customer_name:<30} {format_date(invoice.date):<15} "
                  f"{invoice.total_items:>15} {invoice.total_amount:>15,.2f}")
        
        print("="*80)
        print(f"Tổng số: {len(self.invoices)} hóa đơn")
        print("="*80) 