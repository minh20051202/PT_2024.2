#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quản lý hóa đơn cho Hệ thống Quản lý Hóa đơn.
"""

from typing import List, Dict, Any, Optional
from models import Invoice, InvoiceItem, Product
from .file_manager import FileManager
from .product_manager import ProductManager
from utils import validate_required_field

class InvoiceManager:
    """
    Quản lý các thao tác với hóa đơn trong Hệ thống Quản lý Hóa đơn.
    
    Lớp này xử lý các thao tác như tạo, xem và liệt kê hóa đơn.
    Sử dụng FileManager để lưu trữ dữ liệu và ProductManager để lấy thông tin sản phẩm.
    """
    
    def __init__(self, product_manager: ProductManager):
        """
        Khởi tạo với danh sách hóa đơn trống và tải hóa đơn từ bộ nhớ.
        
        Tham số:
            product_manager: Một thực thể của ProductManager để tra cứu sản phẩm
        """
        self.file_manager = FileManager()
        self.product_manager = product_manager
        self.invoices: List[Invoice] = []
        self.load_invoices()
    
    def load_invoices(self) -> None:
        """Tải hóa đơn từ bộ nhớ."""
        self.invoices = self.file_manager.load_invoices()
    
    def save_invoices(self) -> None:
        """Lưu hóa đơn vào bộ nhớ."""
        self.file_manager.save_invoices(self.invoices)
    
    def create_invoice(self, invoice_id: str, customer_name: str, items_data: List[Dict[str, Any]]) -> bool:
        """
        Tạo một hóa đơn mới.
        
        Tham số:
            invoice_id: Mã định danh duy nhất cho hóa đơn
            customer_name: Tên khách hàng
            items_data: Danh sách các từ điển với khóa 'product_id' và 'quantity'
            
        Trả về:
            True nếu thành công, False nếu không
        """
        # Validate inputs
        if not validate_required_field(invoice_id, "Mã hóa đơn"):
            return False
        if not validate_required_field(customer_name, "Tên khách hàng"):
            return False
        if not items_data:
            print("Lỗi: Hóa đơn phải có ít nhất một mặt hàng.")
            return False
        
        # Check if invoice with this ID already exists
        if any(invoice.invoice_id == invoice_id for invoice in self.invoices):
            print(f"Hóa đơn với Mã '{invoice_id}' đã tồn tại!")
            return False
        
        # Create invoice items
        invoice_items = []
        for item_data in items_data:
            product_id = item_data['product_id']
            quantity = item_data['quantity']
            
            # Find product to get unit price
            product = self.product_manager.find_product(product_id)
            if not product:
                print(f"Không tìm thấy sản phẩm với Mã '{product_id}'!")
                return False
            
            # Create invoice item
            invoice_item = InvoiceItem(
                product_id=product_id,
                quantity=quantity,
                unit_price=product.unit_price
            )
            invoice_items.append(invoice_item)
        
        # Create invoice
        invoice = Invoice(
            invoice_id=invoice_id,
            customer_name=customer_name,
            items=invoice_items
        )
        
        # Add to list and save
        self.invoices.append(invoice)
        self.save_invoices()
        print(f"Đã tạo hóa đơn '{invoice_id}' thành công!")
        return True
    
    def find_invoice(self, invoice_id: str) -> Optional[Invoice]:
        """
        Tìm kiếm hóa đơn theo ID.
        
        Tham số:
            invoice_id: Mã hóa đơn cần tìm
            
        Trả về:
            Đối tượng hóa đơn nếu tìm thấy, None nếu không
        """
        for invoice in self.invoices:
            if invoice.invoice_id == invoice_id:
                return invoice
        return None
    
    def view_invoice_detail(self, invoice_id: str) -> bool:
        """
        Hiển thị chi tiết của một hóa đơn.
        
        Tham số:
            invoice_id: Mã hóa đơn cần xem
            
        Trả về:
            True nếu hóa đơn được tìm thấy và hiển thị, False nếu không
        """
        invoice = self.find_invoice(invoice_id)
        if not invoice:
            print(f"Không tìm thấy hóa đơn với Mã '{invoice_id}'!")
            return False
        
        print("\n" + "="*80)
        print(f"CHI TIẾT HÓA ĐƠN - {invoice_id}")
        print("="*80)
        print(f"Mã hóa đơn:    {invoice.invoice_id}")
        print(f"Ngày:          {invoice.date}")
        print(f"Khách hàng:    {invoice.customer_name}")
        print("-"*80)
        
        print(f"{'STT':<5} {'MÃ SP':<10} {'TÊN SẢN PHẨM':<30} {'SỐ LƯỢNG':<10} {'ĐƠN GIÁ':<15} {'THÀNH TIỀN':<15}")
        print("-"*80)
        
        for idx, item in enumerate(invoice.items, 1):
            product = self.product_manager.find_product(item.product_id)
            product_name = product.name if product else "[Sản phẩm không tồn tại]"
            print(f"{idx:<5} {item.product_id:<10} {product_name:<30} {item.quantity:<10} "
                  f"{item.unit_price:>15,.2f} {item.total_price:>15,.2f}")
        
        print("-"*80)
        print(f"{'TỔNG CỘNG:':<60} {invoice.total_amount:>15,.2f}")
        print("="*80)
        return True
    
    def list_invoices(self) -> None:
        """Hiển thị danh sách hóa đơn."""
        if not self.invoices:
            print("Danh sách hóa đơn trống!")
            return
        
        print("\n" + "="*80)
        print(f"{'MÃ HĐ':<10} {'NGÀY':<12} {'KHÁCH HÀNG':<25} {'SỐ MẶT HÀNG':<15} {'TỔNG TIỀN':<15}")
        print("-"*80)
        
        for invoice in self.invoices:
            print(f"{invoice.invoice_id:<10} {invoice.date:<12} {invoice.customer_name:<25} "
                  f"{len(invoice.items):<15} {invoice.total_amount:>15,.2f}")
        
        print("="*80)
        print(f"Tổng số: {len(self.invoices)} hóa đơn")
        print("="*80) 