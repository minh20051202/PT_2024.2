#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quản lý hóa đơn cho Hệ thống Quản lý Hóa đơn, sử dụng SQLite.
"""
import sqlite3
from datetime import datetime
from typing import List, Optional, Dict, Any

from models import Invoice, InvoiceItem
from database.database import DATABASE_PATH
from .product_manager import ProductManager

class InvoiceManager:
    """
    Quản lý các thao tác với hóa đơn, kết nối trực tiếp với database SQLite.
    """
    
    def __init__(self, product_manager: ProductManager):
        """Khởi tạo và tải hóa đơn từ database."""
        self.db_path = DATABASE_PATH
        self.product_manager = product_manager
        self.invoices: List[Invoice] = []
        self.load_invoices()
        
    def _get_connection(self):
        """Tạo và trả về một kết nối đến database."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def load_invoices(self) -> None:
        """Tải tất cả hóa đơn và các mục chi tiết từ database."""
        self.invoices = []
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                # Lấy tất cả hóa đơn
                cursor.execute("SELECT id, customer_name, date FROM invoices ORDER BY id;")
                invoice_rows = cursor.fetchall()

                for inv_row in invoice_rows:
                    invoice_id = inv_row['id']
                    
                    # Lấy tất cả các mục cho hóa đơn hiện tại
                    cursor.execute("""
                        SELECT product_id, quantity, unit_price
                        FROM invoice_items
                        WHERE invoice_id = ?
                    """, (invoice_id,))
                    item_rows = cursor.fetchall()
                    
                    items = [InvoiceItem(**dict(row)) for row in item_rows]
                    
                    # Tạo đối tượng Invoice
                    # Chuyển đổi invoice_id (int) sang str để phù hợp với model
                    invoice = Invoice(
                        invoice_id=str(invoice_id), 
                        customer_name=inv_row['customer_name'],
                        date=inv_row['date'],
                        items=items
                    )
                    self.invoices.append(invoice)
            print(f"Đã tải {len(self.invoices)} hóa đơn từ database.")
        except sqlite3.Error as e:
            print(f"Lỗi khi tải hóa đơn từ database: {e}")

    def create_invoice(self, customer_name: str, items_data: List[Dict[str, Any]], date: Optional[str] = None) -> Optional[Invoice]:
        """
        Tạo một hóa đơn mới trong database.
        Lưu ý: invoice_id sẽ được database tự động tạo.
        """
        if not customer_name:
            print("Lỗi: Tên khách hàng là bắt buộc.")
            return None
        if not items_data:
            print("Lỗi: Hóa đơn phải có ít nhất một mặt hàng.")
            return None
        
        invoice_date = date if date else datetime.now().strftime('%Y-%m-%d')
        
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                # Bắt đầu một transaction
                cursor.execute("BEGIN TRANSACTION;")
                
                # 1. Thêm vào bảng invoices
                cursor.execute(
                    "INSERT INTO invoices (customer_name, date) VALUES (?, ?)",
                    (customer_name, invoice_date)
                )
                new_invoice_id = cursor.lastrowid  # Lấy ID tự động tăng

                # 2. Thêm các mục vào bảng invoice_items
                for item_data in items_data:
                    product = self.product_manager.find_product(item_data['product_id'])
                    if not product:
                        # Nếu một sản phẩm không tồn tại, hủy toàn bộ transaction
                        raise ValueError(f"Sản phẩm với ID {item_data['product_id']} không tồn tại.")
                    
                    cursor.execute(
                        """
                        INSERT INTO invoice_items (invoice_id, product_id, quantity, unit_price)
                        VALUES (?, ?, ?, ?)
                        """,
                        (new_invoice_id, item_data['product_id'], item_data['quantity'], product.unit_price)
                    )
                
                # Hoàn tất transaction
                conn.commit()

                # Tải lại danh sách để cập nhật
                self.load_invoices()
                
                new_invoice = self.find_invoice(str(new_invoice_id))
                if new_invoice:
                    print(f"Đã tạo thành công hóa đơn #{new_invoice.invoice_id} cho khách hàng '{customer_name}'.")
                    return new_invoice
                return None

        except (sqlite3.Error, ValueError) as e:
            print(f"Lỗi database khi tạo hóa đơn: {e}")
            # Hủy transaction nếu có lỗi
            if conn:
                conn.rollback()
            return None

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
        print(f"Ngày: {invoice.date}")
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
            print(f"#{invoice.invoice_id:<9} {invoice.customer_name:<30} {invoice.date:<15} "
                  f"{invoice.total_items:>15} {invoice.total_amount:>15,.2f}")
        
        print("="*80)
        print(f"Tổng số: {len(self.invoices)} hóa đơn")
        print("="*80) 