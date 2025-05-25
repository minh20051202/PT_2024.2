#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quản lý thống kê cho Hệ thống Quản lý Hóa đơn.
"""

from collections import defaultdict
from typing import Dict, List, Tuple
from .invoice_manager import InvoiceManager
from .product_manager import ProductManager

class StatisticsManager:
    """
    Quản lý các thao tác thống kê trong Hệ thống Quản lý Hóa đơn.
    
    Lớp này tạo ra các báo cáo thống kê khác nhau dựa trên dữ liệu hóa đơn và sản phẩm.
    """
    
    def __init__(self, invoice_manager: InvoiceManager, product_manager: ProductManager):
        """
        Khởi tạo với tham chiếu đến trình quản lý hóa đơn và sản phẩm.
        
        Tham số:
            invoice_manager: Một thực thể của InvoiceManager cho dữ liệu hóa đơn
            product_manager: Một thực thể của ProductManager cho dữ liệu sản phẩm
        """
        self.invoice_manager = invoice_manager
        self.product_manager = product_manager
    
    def revenue_by_date(self) -> None:
        """Hiển thị doanh thu theo từng ngày."""
        if not self.invoice_manager.invoices:
            print("Không có dữ liệu hóa đơn để thống kê!")
            return
        
        # Group revenue by date
        date_revenue: Dict[str, float] = defaultdict(float)
        for invoice in self.invoice_manager.invoices:
            date_revenue[invoice.date] += invoice.total_amount
        
        if not date_revenue:
            print("Không có dữ liệu doanh thu để hiển thị!")
            return
        
        # Sort by date (newest first)
        sorted_dates = sorted(date_revenue.items(), reverse=True)
        
        # Display report
        print("\n" + "="*60)
        print("THỐNG KÊ DOANH THU THEO NGÀY")
        print("="*60)
        print(f"{'NGÀY':<15} {'DOANH THU':<20} {'TỈ LỆ':<10}")
        print("-"*60)
        
        total_revenue = sum(date_revenue.values())
        for date, revenue in sorted_dates:
            percentage = (revenue / total_revenue) * 100 if total_revenue > 0 else 0
            print(f"{date:<15} {revenue:>20,.2f} {percentage:>9.2f}%")
        
        print("-"*60)
        print(f"{'TỔNG CỘNG:':<15} {total_revenue:>20,.2f}")
        print("="*60)
    
    def revenue_by_product(self) -> None:
        """Hiển thị doanh thu theo từng sản phẩm."""
        if not self.invoice_manager.invoices:
            print("Không có dữ liệu hóa đơn để thống kê!")
            return
        
        # Calculate revenue and quantity by product
        product_stats: Dict[str, Tuple[float, int]] = defaultdict(lambda: (0.0, 0))
        for invoice in self.invoice_manager.invoices:
            for item in invoice.items:
                current_revenue, current_quantity = product_stats[item.product_id]
                product_stats[item.product_id] = (
                    current_revenue + item.total_price,
                    current_quantity + item.quantity
                )
        
        if not product_stats:
            print("Không có dữ liệu doanh thu theo sản phẩm để hiển thị!")
            return
        
        # Sort by revenue (highest first)
        sorted_products = sorted(
            product_stats.items(), 
            key=lambda x: x[1][0], 
            reverse=True
        )
        
        # Display report
        print("\n" + "="*80)
        print("THỐNG KÊ DOANH THU THEO SẢN PHẨM")
        print("="*80)
        print(f"{'MÃ SP':<10} {'TÊN SẢN PHẨM':<30} {'SỐ LƯỢNG':<10} {'DOANH THU':<15} {'TỈ LỆ':<10}")
        print("-"*80)
        
        total_revenue = sum(revenue for revenue, _ in product_stats.values())
        for product_id, (revenue, quantity) in sorted_products:
            product = self.product_manager.find_product(product_id)
            product_name = product.name if product else "[Sản phẩm không tồn tại]"
            percentage = (revenue / total_revenue) * 100 if total_revenue > 0 else 0
            print(f"{product_id:<10} {product_name:<30} {quantity:>10} {revenue:>15,.2f} {percentage:>9.2f}%")
        
        print("-"*80)
        print(f"{'TỔNG CỘNG:':<50} {total_revenue:>15,.2f}")
        print("="*80)
    
    def top_customers(self, limit: int = 5) -> None:
        """
        Hiển thị danh sách khách hàng chi tiêu nhiều nhất.
        
        Tham số:
            limit: Số lượng khách hàng hàng đầu cần hiển thị (mặc định: 5)
        """
        if not self.invoice_manager.invoices:
            print("Không có dữ liệu hóa đơn để thống kê!")
            return
        
        # Calculate spending by customer
        customer_spending: Dict[str, float] = defaultdict(float)
        for invoice in self.invoice_manager.invoices:
            customer_spending[invoice.customer_name] += invoice.total_amount
        
        if not customer_spending:
            print("Không có dữ liệu khách hàng để hiển thị!")
            return
        
        # Sort by spending (highest first) and limit results
        sorted_customers = sorted(
            customer_spending.items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:limit]
        
        # Display report
        print("\n" + "="*60)
        print(f"TOP {limit} KHÁCH HÀNG TIỀM NĂNG")
        print("="*60)
        print(f"{'KHÁCH HÀNG':<30} {'TỔNG CHI TIÊU':<20} {'TỈ LỆ':<10}")
        print("-"*60)
        
        total_spending = sum(customer_spending.values())
        for customer_name, spending in sorted_customers:
            percentage = (spending / total_spending) * 100 if total_spending > 0 else 0
            print(f"{customer_name:<30} {spending:>20,.2f} {percentage:>9.2f}%")
        
        print("-"*60)
        print(f"{'TỔNG CỘNG:':<30} {total_spending:>20,.2f}")
        print("="*60) 