#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Giao diện đồ họa (GUI) cho Hệ thống Quản lý Hóa đơn.
"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import io
import sys  
from tkinter import simpledialog 
from collections import defaultdict

from core.product_manager import ProductManager
from core.invoice_manager import InvoiceManager
from core.statistics_manager import StatisticsManager

class InvoiceAppGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Hệ thống Quản lý Hóa đơn")
        self.root.geometry("900x700")  # Kích thước lớn hơn một chút để bố cục tốt hơn

        # Error handling for manager initialization
        try:
            # Khởi tạo các trình quản lý
            self.product_manager = ProductManager()
            self.invoice_manager = InvoiceManager(self.product_manager)
            self.statistics_manager = StatisticsManager(self.invoice_manager, self.product_manager)
        except Exception as e:
            messagebox.showerror("Lỗi khởi tạo", f"Không thể khởi tạo trình quản lý: {str(e)}")
            # Create empty managers for UI to render without crashing
            self.product_manager = None
            self.invoice_manager = None
            self.statistics_manager = None

        # Tạo Notebook (giao diện tab)
        self.notebook = ttk.Notebook(root)

        # Tạo các frame cho mỗi tab
        self.product_tab = ttk.Frame(self.notebook)
        self.invoice_tab = ttk.Frame(self.notebook)
        self.statistics_tab = ttk.Frame(self.notebook)

        # Thêm các tab vào notebook
        self.notebook.add(self.product_tab, text='Quản lý Sản phẩm')
        self.notebook.add(self.invoice_tab, text='Quản lý Hóa đơn')
        self.notebook.add(self.statistics_tab, text='Thống kê')

        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)

        # Điền nội dung cho mỗi tab
        self._create_product_tab()
        self._create_invoice_tab()
        self._create_statistics_tab()

    def _create_product_tab(self):
        # Tạo frame chứa danh sách sản phẩm
        list_frame = ttk.LabelFrame(self.product_tab, text="Danh sách sản phẩm")
        list_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Tạo Treeview để hiển thị sản phẩm
        columns = ("ID", "Tên", "Đơn giá", "Danh mục", "Đơn vị tính")
        self.product_tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        
        # Đặt tiêu đề cho các cột
        for col in columns:
            self.product_tree.heading(col, text=col)
            self.product_tree.column(col, width=100)
        
        # Thêm scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.product_tree.yview)
        self.product_tree.configure(yscrollcommand=scrollbar.set)
        
        # Đặt vị trí
        self.product_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Buttons frame
        button_frame = ttk.Frame(self.product_tab)
        button_frame.pack(fill="x", padx=10, pady=5)
        
        # Nút tải danh sách sản phẩm
        refresh_button = ttk.Button(button_frame, text="Tải lại danh sách sản phẩm", 
                                  command=self.load_products)
        refresh_button.pack(side="left", padx=5)
        
        # Nút thêm sản phẩm mới
        add_button = ttk.Button(button_frame, text="Thêm sản phẩm", 
                              command=self.add_product_dialog)
        add_button.pack(side="left", padx=5)
        
        # Nút cập nhật sản phẩm
        update_button = ttk.Button(button_frame, text="Cập nhật sản phẩm", 
                                 command=self.update_product_dialog)
        update_button.pack(side="left", padx=5)
        
        # Nút xóa sản phẩm
        delete_button = ttk.Button(button_frame, text="Xóa sản phẩm", 
                                 command=self.delete_product)
        delete_button.pack(side="left", padx=5)
        
        # Frame chứa nút nhập/xuất CSV
        csv_frame = ttk.Frame(self.product_tab)
        csv_frame.pack(fill="x", padx=10, pady=5)
        
        # Nút nhập từ CSV
        import_csv_button = ttk.Button(csv_frame, text="Nhập từ CSV", 
                                     command=self.import_products_from_csv)
        import_csv_button.pack(side="left", padx=5)
        
        # Nút xuất ra CSV
        export_csv_button = ttk.Button(csv_frame, text="Xuất ra CSV", 
                                     command=self.export_products_to_csv)
        export_csv_button.pack(side="left", padx=5)
        
        # Tự động tải khi mở tab
        self.load_products()

    def load_products(self):
        try:
            # Xóa dữ liệu cũ
            for item in self.product_tree.get_children():
                self.product_tree.delete(item)
            
            # Kiểm tra xem trình quản lý đã được khởi tạo chưa
            if self.product_manager is None:
                messagebox.showwarning("Cảnh báo", "Trình quản lý sản phẩm chưa được khởi tạo")
                return
                
            # Tải sản phẩm từ product_manager
            for product in self.product_manager.products:
                self.product_tree.insert("", "end", values=(
                    product.product_id,
                    product.name,
                    f"{product.unit_price:,.0f}",
                    product.category,
                    product.calculation_unit
                ))
                
            # Thông báo khi không có sản phẩm
            if len(self.product_manager.products) == 0:
                messagebox.showinfo("Thông báo", "Không có sản phẩm nào. Hãy thêm sản phẩm mới.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải danh sách sản phẩm: {str(e)}")

    def add_product_dialog(self):
        """Hiển thị hộp thoại để thêm sản phẩm mới."""
        if self.product_manager is None:
            messagebox.showwarning("Cảnh báo", "Trình quản lý sản phẩm chưa được khởi tạo")
            return
            
        # Tạo cửa sổ dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Thêm sản phẩm mới")
        dialog.geometry("400x300")
        dialog.transient(self.root)  # Làm cho cửa sổ này phụ thuộc vào cửa sổ chính
        dialog.grab_set()  # Ngăn người dùng tương tác với cửa sổ chính
        
        # Frame chứa các trường nhập liệu
        input_frame = ttk.Frame(dialog, padding=10)
        input_frame.pack(fill="both", expand=True)
        
        # Tạo các trường nhập liệu
        ttk.Label(input_frame, text="Mã sản phẩm:").grid(row=0, column=0, sticky="w", pady=5)
        product_id_entry = ttk.Entry(input_frame, width=30)
        product_id_entry.grid(row=0, column=1, pady=5)
        
        ttk.Label(input_frame, text="Tên sản phẩm:").grid(row=1, column=0, sticky="w", pady=5)
        name_entry = ttk.Entry(input_frame, width=30)
        name_entry.grid(row=1, column=1, pady=5)
        
        ttk.Label(input_frame, text="Đơn giá:").grid(row=2, column=0, sticky="w", pady=5)
        price_entry = ttk.Entry(input_frame, width=30)
        price_entry.grid(row=2, column=1, pady=5)
        
        ttk.Label(input_frame, text="Danh mục:").grid(row=3, column=0, sticky="w", pady=5)
        category_entry = ttk.Entry(input_frame, width=30)
        category_entry.grid(row=3, column=1, pady=5)
        category_entry.insert(0, "General")  # Giá trị mặc định
        
        ttk.Label(input_frame, text="Đơn vị tính:").grid(row=4, column=0, sticky="w", pady=5)
        unit_entry = ttk.Entry(input_frame, width=30)
        unit_entry.grid(row=4, column=1, pady=5)
        unit_entry.insert(0, "đơn vị")  # Giá trị mặc định
        
        # Frame chứa các nút
        button_frame = ttk.Frame(dialog, padding=10)
        button_frame.pack(fill="x")
        
        # Hàm xử lý khi nhấn nút Thêm
        def on_add():
            try:
                # Lấy giá trị từ các trường nhập liệu
                product_id = product_id_entry.get().strip()
                name = name_entry.get().strip()
                
                # Kiểm tra và chuyển đổi đơn giá
                try:
                    price = float(price_entry.get().strip())
                except ValueError:
                    messagebox.showerror("Lỗi", "Đơn giá phải là số")
                    return
                    
                category = category_entry.get().strip()
                unit = unit_entry.get().strip()
                
                # Gọi phương thức thêm sản phẩm
                result = self.product_manager.add_product(
                    product_id=product_id,
                    name=name,
                    unit_price=price,
                    category=category,
                    calculation_unit=unit
                )
                
                if result:
                    # Thêm trực tiếp vào TreeView thay vì tải lại toàn bộ danh sách
                    self.product_tree.insert("", "end", values=(
                        product_id,
                        name,
                        f"{price:,.0f}",
                        category,
                        unit
                    ))
                    dialog.destroy()  # Đóng hộp thoại
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể thêm sản phẩm: {str(e)}")
        
        # Nút Thêm và Hủy
        ttk.Button(button_frame, text="Thêm", command=on_add).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Hủy", command=dialog.destroy).pack(side="right", padx=5)

    def update_product_dialog(self):
        """Hiển thị hộp thoại để cập nhật sản phẩm."""
        # Kiểm tra sản phẩm được chọn
        selected = self.product_tree.selection()
        if not selected:
            messagebox.showinfo("Thông báo", "Vui lòng chọn một sản phẩm để cập nhật")
            return
            
        if self.product_manager is None:
            messagebox.showwarning("Cảnh báo", "Trình quản lý sản phẩm chưa được khởi tạo")
            return
        
        # Lấy ID sản phẩm
        product_id = self.product_tree.item(selected[0], "values")[0]
        product = self.product_manager.find_product(product_id)
        
        if not product:
            messagebox.showinfo("Thông báo", f"Không tìm thấy sản phẩm với mã {product_id}")
            return
        
        # Tạo cửa sổ dialog
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Cập nhật sản phẩm - {product_id}")
        dialog.geometry("400x300")
        dialog.transient(self.root)  # Làm cho cửa sổ này phụ thuộc vào cửa sổ chính
        dialog.grab_set()  # Ngăn người dùng tương tác với cửa sổ chính
        
        # Frame chứa các trường nhập liệu
        input_frame = ttk.Frame(dialog, padding=10)
        input_frame.pack(fill="both", expand=True)
        
        # Tạo các trường nhập liệu, điền giá trị hiện tại
        ttk.Label(input_frame, text="Mã sản phẩm:").grid(row=0, column=0, sticky="w", pady=5)
        product_id_entry = ttk.Entry(input_frame, width=30)
        product_id_entry.grid(row=0, column=1, pady=5)
        product_id_entry.insert(0, product_id)
        product_id_entry.config(state="disabled")  # Không cho phép thay đổi ID
        
        ttk.Label(input_frame, text="Tên sản phẩm:").grid(row=1, column=0, sticky="w", pady=5)
        name_entry = ttk.Entry(input_frame, width=30)
        name_entry.grid(row=1, column=1, pady=5)
        name_entry.insert(0, product.name)
        
        ttk.Label(input_frame, text="Đơn giá:").grid(row=2, column=0, sticky="w", pady=5)
        price_entry = ttk.Entry(input_frame, width=30)
        price_entry.grid(row=2, column=1, pady=5)
        price_entry.insert(0, str(product.unit_price))
        
        ttk.Label(input_frame, text="Danh mục:").grid(row=3, column=0, sticky="w", pady=5)
        category_entry = ttk.Entry(input_frame, width=30)
        category_entry.grid(row=3, column=1, pady=5)
        category_entry.insert(0, product.category)
        
        ttk.Label(input_frame, text="Đơn vị tính:").grid(row=4, column=0, sticky="w", pady=5)
        unit_entry = ttk.Entry(input_frame, width=30)
        unit_entry.grid(row=4, column=1, pady=5)
        unit_entry.insert(0, product.calculation_unit)
        
        # Frame chứa các nút
        button_frame = ttk.Frame(dialog, padding=10)
        button_frame.pack(fill="x")
        
        # Hàm xử lý khi nhấn nút Cập nhật
        def on_update():
            try:
                # Lấy giá trị từ các trường nhập liệu
                name = name_entry.get().strip()
                
                # Kiểm tra và chuyển đổi đơn giá
                try:
                    price = float(price_entry.get().strip())
                except ValueError:
                    messagebox.showerror("Lỗi", "Đơn giá phải là số")
                    return
                    
                category = category_entry.get().strip()
                unit = unit_entry.get().strip()
                
                # Gọi phương thức cập nhật sản phẩm
                result = self.product_manager.update_product(
                    product_id=product_id,
                    name=name,
                    unit_price=price,
                    category=category,
                    calculation_unit=unit
                )
                
                if result:
                    # Cập nhật trực tiếp vào TreeView thay vì tải lại toàn bộ danh sách
                    self.product_tree.item(selected[0], values=(
                        product_id,
                        name,
                        f"{price:,.0f}",
                        category,
                        unit
                    ))
                    dialog.destroy()  # Đóng hộp thoại
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể cập nhật sản phẩm: {str(e)}")
        
        # Nút Cập nhật và Hủy
        ttk.Button(button_frame, text="Cập nhật", command=on_update).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Hủy", command=dialog.destroy).pack(side="right", padx=5)

    def delete_product(self):
        """Xóa sản phẩm đã chọn."""
        # Kiểm tra sản phẩm được chọn
        selected = self.product_tree.selection()
        if not selected:
            messagebox.showinfo("Thông báo", "Vui lòng chọn một sản phẩm để xóa")
            return
            
        if self.product_manager is None:
            messagebox.showwarning("Cảnh báo", "Trình quản lý sản phẩm chưa được khởi tạo")
            return
        
        # Lấy ID sản phẩm
        product_id = self.product_tree.item(selected[0], "values")[0]
        
        # Xác nhận xóa
        if not messagebox.askyesno("Xác nhận", f"Bạn có chắc chắn muốn xóa sản phẩm {product_id}?"):
            return
        
        # Gọi phương thức xóa sản phẩm
        try:
            result = self.product_manager.delete_product(product_id)
            if result:
                # Xóa trực tiếp khỏi TreeView thay vì tải lại toàn bộ danh sách
                self.product_tree.delete(selected[0])
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xóa sản phẩm: {str(e)}")

    def import_products_from_csv(self):
        """Nhập sản phẩm từ file CSV."""
        if self.product_manager is None:
            messagebox.showwarning("Cảnh báo", "Trình quản lý sản phẩm chưa được khởi tạo")
            return
            
        # Mở hộp thoại chọn file
        filepath = filedialog.askopenfilename(
            title="Chọn file CSV sản phẩm",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if not filepath:  # Người dùng đã hủy
            return
            
        try:
            # Nhập sản phẩm từ CSV thông qua FileManager
            imported_products = self.product_manager.file_manager.import_products_from_csv(filepath)
            
            if not imported_products:
                messagebox.showinfo("Thông báo", "Không có sản phẩm nào được nhập từ file CSV.")
                return
                
            # Xác nhận số lượng sản phẩm sẽ nhập
            confirmed = messagebox.askyesno(
                "Xác nhận", 
                f"Đã tìm thấy {len(imported_products)} sản phẩm trong file CSV. Bạn muốn nhập vào hệ thống?"
            )
            
            if not confirmed:
                return
                
            # Thêm từng sản phẩm vào hệ thống
            products_added = 0
            products_skipped = 0
            
            # Với số lượng lớn (>10), dùng load_products() sẽ hiệu quả hơn
            large_import = len(imported_products) > 10
            
            for product in imported_products:
                # Kiểm tra xem sản phẩm đã tồn tại chưa
                existing_product = self.product_manager.find_product(product.product_id)
                
                if existing_product:
                    # Sản phẩm đã tồn tại, cập nhật nếu người dùng xác nhận
                    products_skipped += 1
                else:
                    # Thêm sản phẩm mới
                    result = self.product_manager.add_product(
                        product_id=product.product_id,
                        name=product.name,
                        unit_price=product.unit_price,
                        category=product.category,
                        calculation_unit=product.calculation_unit
                    )
                    
                    if result and not large_import:
                        # Thêm trực tiếp vào TreeView với số lượng nhỏ
                        self.product_tree.insert("", "end", values=(
                            product.product_id,
                            product.name,
                            f"{product.unit_price:,.0f}",
                            product.category,
                            product.calculation_unit
                        ))
                    
                    if result:
                        products_added += 1
            
            # Thông báo kết quả
            messagebox.showinfo(
                "Kết quả nhập CSV", 
                f"Đã nhập thành công {products_added} sản phẩm.\n"
                f"Bỏ qua {products_skipped} sản phẩm đã tồn tại."
            )
            
            # Chỉ tải lại danh sách nếu số lượng lớn
            if large_import and products_added > 0:
                self.load_products()
                
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể nhập sản phẩm từ CSV: {str(e)}")

    def export_products_to_csv(self):
        """Xuất sản phẩm ra file CSV."""
        if self.product_manager is None:
            messagebox.showwarning("Cảnh báo", "Trình quản lý sản phẩm chưa được khởi tạo")
            return
            
        if not self.product_manager.products:
            messagebox.showinfo("Thông báo", "Không có sản phẩm nào để xuất")
            return
            
        # Mở hộp thoại lưu file
        filepath = filedialog.asksaveasfilename(
            title="Lưu file CSV sản phẩm",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if not filepath:  # Người dùng đã hủy
            return
            
        try:
            # Xuất sản phẩm ra CSV thông qua FileManager
            self.product_manager.file_manager.export_products_to_csv(filepath, self.product_manager.products)
            
            # Thông báo kết quả
            messagebox.showinfo(
                "Thành công", 
                f"Đã xuất {len(self.product_manager.products)} sản phẩm ra file CSV."
            )
                
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xuất sản phẩm ra CSV: {str(e)}")

    def _create_invoice_tab(self):
        # Tạo frame chứa danh sách hóa đơn
        list_frame = ttk.LabelFrame(self.invoice_tab, text="Danh sách hóa đơn")
        list_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Tạo Treeview để hiển thị hóa đơn
        columns = ("ID", "Khách hàng", "Ngày", "Tổng tiền", "Số mặt hàng")
        self.invoice_tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        
        # Đặt tiêu đề cho các cột
        for col in columns:
            self.invoice_tree.heading(col, text=col)
            self.invoice_tree.column(col, width=100)
        
        # Thêm scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.invoice_tree.yview)
        self.invoice_tree.configure(yscrollcommand=scrollbar.set)
        
        # Đặt vị trí
        self.invoice_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Buttons frame
        button_frame = ttk.Frame(self.invoice_tab)
        button_frame.pack(fill="x", padx=10, pady=5)
        
        # Nút tải danh sách hóa đơn
        refresh_button = ttk.Button(button_frame, text="Tải danh sách hóa đơn", 
                                   command=self.load_invoices)
        refresh_button.pack(side="left", padx=5)
        
        # Nút xem chi tiết hóa đơn
        view_button = ttk.Button(button_frame, text="Xem chi tiết", 
                               command=self.view_invoice_details)
        view_button.pack(side="left", padx=5)
        
        # Nút tạo hóa đơn mới
        add_button = ttk.Button(button_frame, text="Tạo hóa đơn mới", 
                              command=self.create_new_invoice)
        add_button.pack(side="left", padx=5)
        
        # Frame chứa nút nhập/xuất CSV
        csv_frame = ttk.Frame(self.invoice_tab)
        csv_frame.pack(fill="x", padx=10, pady=5)
        
        # Nút nhập từ CSV
        import_csv_button = ttk.Button(csv_frame, text="Nhập từ CSV", 
                                     command=self.import_invoices_from_csv)
        import_csv_button.pack(side="left", padx=5)
        
        # Nút xuất ra CSV
        export_csv_button = ttk.Button(csv_frame, text="Xuất ra CSV", 
                                     command=self.export_invoices_to_csv)
        export_csv_button.pack(side="left", padx=5)
        
        # Tự động tải khi mở tab
        self.load_invoices()

    def load_invoices(self):
        try:
            # Xóa dữ liệu cũ
            for item in self.invoice_tree.get_children():
                self.invoice_tree.delete(item)
            
            # Kiểm tra xem trình quản lý đã được khởi tạo chưa
            if self.invoice_manager is None:
                messagebox.showwarning("Cảnh báo", "Trình quản lý hóa đơn chưa được khởi tạo")
                return
                
            # Tải hóa đơn từ invoice_manager
            for invoice in self.invoice_manager.invoices:
                self.invoice_tree.insert("", "end", values=(
                    invoice.invoice_id,
                    invoice.customer_name,
                    invoice.date,
                    f"{invoice.total_amount:,.0f}",
                    invoice.total_items
                ))
                
            # Thông báo khi không có hóa đơn
            if len(self.invoice_manager.invoices) == 0:
                messagebox.showinfo("Thông báo", "Không có hóa đơn nào. Hãy tạo hóa đơn mới.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải danh sách hóa đơn: {str(e)}")

    def view_invoice_details(self):
        """Hiển thị chi tiết hóa đơn trong một cửa sổ mới."""
        # Lấy hóa đơn được chọn
        selected = self.invoice_tree.selection()
        if not selected:
            messagebox.showinfo("Thông báo", "Vui lòng chọn một hóa đơn để xem chi tiết")
            return
        
        # Lấy ID hóa đơn
        invoice_id = self.invoice_tree.item(selected[0], "values")[0]
        
        try:
            # Tìm hóa đơn
            invoice = self.invoice_manager.find_invoice(invoice_id)
            if not invoice:
                messagebox.showinfo("Thông báo", f"Không tìm thấy chi tiết cho hóa đơn {invoice_id}")
                return
            
            # Tạo cửa sổ mới
            detail_window = tk.Toplevel(self.root)
            detail_window.title(f"Chi tiết hóa đơn - {invoice_id}")
            detail_window.geometry("800x600")
            detail_window.transient(self.root)  # Làm cho cửa sổ này phụ thuộc vào cửa sổ chính
            
            # Frame chứa thông tin chung
            info_frame = ttk.LabelFrame(detail_window, text="Thông tin hóa đơn")
            info_frame.pack(fill="x", padx=10, pady=5)
            
            # Hiển thị thông tin chung
            ttk.Label(info_frame, text=f"Mã hóa đơn: {invoice.invoice_id}", font=("Arial", 11)).grid(row=0, column=0, sticky="w", padx=10, pady=5)
            ttk.Label(info_frame, text=f"Ngày: {invoice.date}", font=("Arial", 11)).grid(row=0, column=1, sticky="w", padx=10, pady=5)
            ttk.Label(info_frame, text=f"Khách hàng: {invoice.customer_name}", font=("Arial", 11)).grid(row=1, column=0, columnspan=2, sticky="w", padx=10, pady=5)
            
            # Frame chứa danh sách mặt hàng
            items_frame = ttk.LabelFrame(detail_window, text="Danh sách mặt hàng")
            items_frame.pack(fill="both", expand=True, padx=10, pady=5)
            
            # Tạo Treeview để hiển thị mặt hàng
            columns = ("STT", "Mã SP", "Tên", "Số lượng", "Đơn giá", "Thành tiền")
            items_tree = ttk.Treeview(items_frame, columns=columns, show="headings")
            
            # Đặt tiêu đề cho các cột
            for col in columns:
                items_tree.heading(col, text=col)
            
            # Đặt chiều rộng cho các cột
            items_tree.column("STT", width=50)
            items_tree.column("Mã SP", width=100)
            items_tree.column("Tên", width=200)
            items_tree.column("Số lượng", width=100)
            items_tree.column("Đơn giá", width=150)
            items_tree.column("Thành tiền", width=150)
            
            # Thêm scrollbar
            scrollbar = ttk.Scrollbar(items_frame, orient="vertical", command=items_tree.yview)
            items_tree.configure(yscrollcommand=scrollbar.set)
            
            # Đặt vị trí
            items_tree.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            # Thêm các mặt hàng vào bảng
            for idx, item in enumerate(invoice.items, 1):
                product = self.product_manager.find_product(item.product_id)
                product_name = product.name if product else "[Sản phẩm không tồn tại]"
                
                items_tree.insert("", "end", values=(
                    idx,
                    item.product_id,
                    product_name,
                    item.quantity,
                    f"{item.unit_price:,.0f}",
                    f"{item.total_price:,.0f}"
                ))
            
            # Hiển thị tổng tiền
            summary_frame = ttk.Frame(detail_window)
            summary_frame.pack(fill="x", padx=10, pady=10)
            
            ttk.Label(summary_frame, text=f"Tổng số mặt hàng: {invoice.total_items}", font=("Arial", 11)).pack(side="left", padx=10)
            ttk.Label(summary_frame, text=f"Tổng tiền: {invoice.total_amount:,.0f} VND", font=("Arial", 11, "bold")).pack(side="right", padx=10)
            
            # Nút đóng
            ttk.Button(detail_window, text="Đóng", command=detail_window.destroy).pack(pady=10)
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xem chi tiết hóa đơn: {str(e)}")

    def create_new_invoice(self):
        """Hiển thị hộp thoại để tạo hóa đơn mới."""
        if self.invoice_manager is None or self.product_manager is None:
            messagebox.showwarning("Cảnh báo", "Trình quản lý chưa được khởi tạo đầy đủ")
            return
        
        if len(self.product_manager.products) == 0:
            messagebox.showinfo("Thông báo", "Không có sản phẩm nào trong hệ thống. Vui lòng thêm sản phẩm trước.")
            return
        
        # Tạo cửa sổ dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Tạo hóa đơn mới")
        dialog.geometry("700x500")
        dialog.transient(self.root)  # Làm cho cửa sổ này phụ thuộc vào cửa sổ chính
        dialog.grab_set()  # Ngăn người dùng tương tác với cửa sổ chính
        
        # Frame chứa thông tin hóa đơn
        info_frame = ttk.LabelFrame(dialog, text="Thông tin hóa đơn")
        info_frame.pack(fill="x", padx=10, pady=5)
        
        # Tạo các trường nhập liệu thông tin hóa đơn
        ttk.Label(info_frame, text="Mã hóa đơn:").grid(row=0, column=0, sticky="w", pady=5, padx=5)
        invoice_id_entry = ttk.Entry(info_frame, width=30)
        invoice_id_entry.grid(row=0, column=1, pady=5, padx=5)
        
        ttk.Label(info_frame, text="Tên khách hàng:").grid(row=1, column=0, sticky="w", pady=5, padx=5)
        customer_name_entry = ttk.Entry(info_frame, width=30)
        customer_name_entry.grid(row=1, column=1, pady=5, padx=5)
        
        # Frame chứa danh sách sản phẩm
        items_frame = ttk.LabelFrame(dialog, text="Mặt hàng")
        items_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Danh sách mặt hàng hiện có
        current_items = []  # Danh sách các mặt hàng trong hóa đơn
        
        # Tạo Treeview để hiển thị mặt hàng đã chọn
        columns = ("Mã SP", "Tên", "Số lượng", "Đơn giá", "Thành tiền")
        items_tree = ttk.Treeview(items_frame, columns=columns, show="headings")
        
        # Đặt tiêu đề cho các cột
        for col in columns:
            items_tree.heading(col, text=col)
            items_tree.column(col, width=100)
        
        # Thêm scrollbar
        scrollbar = ttk.Scrollbar(items_frame, orient="vertical", command=items_tree.yview)
        items_tree.configure(yscrollcommand=scrollbar.set)
        
        # Đặt vị trí
        items_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Frame chứa các nút thao tác với mặt hàng
        item_actions_frame = ttk.Frame(dialog)
        item_actions_frame.pack(fill="x", padx=10, pady=5)
        
        # Frame cho việc thêm mặt hàng
        add_item_frame = ttk.LabelFrame(item_actions_frame, text="Thêm mặt hàng")
        add_item_frame.pack(fill="x", padx=5, pady=5)
        
        # Dropdown chọn sản phẩm
        ttk.Label(add_item_frame, text="Sản phẩm:").grid(row=0, column=0, sticky="w", pady=5, padx=5)
        product_var = tk.StringVar()
        product_combo = ttk.Combobox(add_item_frame, textvariable=product_var, width=30)
        
        # Tạo danh sách sản phẩm cho combobox
        products = [(f"{p.product_id} - {p.name}") for p in self.product_manager.products]
        product_combo['values'] = products
        product_combo.grid(row=0, column=1, pady=5, padx=5)
        
        ttk.Label(add_item_frame, text="Số lượng:").grid(row=0, column=2, sticky="w", pady=5, padx=5)
        quantity_entry = ttk.Entry(add_item_frame, width=10)
        quantity_entry.grid(row=0, column=3, pady=5, padx=5)
        quantity_entry.insert(0, "1")  # Giá trị mặc định
        
        # Hàm cập nhật danh sách mặt hàng
        def update_items_list():
            # Xóa dữ liệu cũ
            for item in items_tree.get_children():
                items_tree.delete(item)
            
            # Hiển thị các mặt hàng hiện có
            total_amount = 0
            for idx, item in enumerate(current_items):
                product_id = item['product_id']
                quantity = item['quantity']
                product = self.product_manager.find_product(product_id)
                
                if product:
                    total_price = quantity * product.unit_price
                    total_amount += total_price
                    
                    items_tree.insert("", "end", values=(
                        product_id,
                        product.name,
                        quantity,
                        f"{product.unit_price:,.0f}",
                        f"{total_price:,.0f}"
                    ))
            
            # Hiển thị tổng tiền
            total_label.config(text=f"Tổng tiền: {total_amount:,.0f} VND")
        
        # Hàm thêm mặt hàng
        def add_item():
            if not product_var.get():
                messagebox.showinfo("Thông báo", "Vui lòng chọn sản phẩm")
                return
            
            try:
                quantity = int(quantity_entry.get().strip())
                if quantity <= 0:
                    messagebox.showinfo("Thông báo", "Số lượng phải lớn hơn 0")
                    return
            except ValueError:
                messagebox.showinfo("Thông báo", "Số lượng phải là số nguyên")
                return
            
            # Lấy ID sản phẩm từ combobox
            product_id = product_var.get().split(" - ")[0]
            
            # Kiểm tra xem mặt hàng đã tồn tại chưa
            for item in current_items:
                if item['product_id'] == product_id:
                    item['quantity'] += quantity
                    update_items_list()
                    return
            
            # Thêm mặt hàng mới
            current_items.append({
                'product_id': product_id,
                'quantity': quantity
            })
            
            # Cập nhật danh sách
            update_items_list()
        
        # Hàm xóa mặt hàng
        def remove_item():
            selected = items_tree.selection()
            if not selected:
                messagebox.showinfo("Thông báo", "Vui lòng chọn một mặt hàng để xóa")
                return
            
            # Lấy ID sản phẩm
            product_id = items_tree.item(selected[0], "values")[0]
            
            # Xóa khỏi danh sách
            current_items[:] = [item for item in current_items if item['product_id'] != product_id]
            
            # Cập nhật danh sách
            update_items_list()
        
        # Thêm nút để thêm và xóa mặt hàng
        ttk.Button(add_item_frame, text="Thêm", command=add_item).grid(row=0, column=4, padx=5, pady=5)
        ttk.Button(item_actions_frame, text="Xóa mặt hàng đã chọn", command=remove_item).pack(side="left", padx=5, pady=5)
        
        # Label hiển thị tổng tiền
        total_label = ttk.Label(dialog, text="Tổng tiền: 0 VND", font=("Arial", 12, "bold"))
        total_label.pack(pady=10)
        
        # Frame chứa các nút hành động
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill="x", padx=10, pady=10)
        
        # Hàm xử lý khi nhấn nút Tạo hóa đơn
        def on_create():
            try:
                # Lấy giá trị từ các trường nhập liệu
                invoice_id = invoice_id_entry.get().strip()
                customer_name = customer_name_entry.get().strip()
                
                # Kiểm tra dữ liệu nhập
                if not invoice_id:
                    messagebox.showinfo("Thông báo", "Vui lòng nhập mã hóa đơn")
                    return
                
                if not customer_name:
                    messagebox.showinfo("Thông báo", "Vui lòng nhập tên khách hàng")
                    return
                
                if not current_items:
                    messagebox.showinfo("Thông báo", "Vui lòng thêm ít nhất một mặt hàng")
                    return
                
                # Gọi phương thức tạo hóa đơn
                result = self.invoice_manager.create_invoice(
                    invoice_id=invoice_id,
                    customer_name=customer_name,
                    items_data=current_items
                )
                
                if result:
                    # Tìm hóa đơn vừa tạo để lấy thông tin chi tiết
                    invoice = self.invoice_manager.find_invoice(invoice_id)
                    if invoice:
                        # Thêm trực tiếp vào TreeView thay vì tải lại toàn bộ danh sách
                        self.invoice_tree.insert("", "end", values=(
                            invoice.invoice_id,
                            invoice.customer_name,
                            invoice.date,
                            f"{invoice.total_amount:,.0f}",
                            invoice.total_items
                        ))
                    dialog.destroy()  # Đóng hộp thoại
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể tạo hóa đơn: {str(e)}")
        
        # Nút Tạo hóa đơn và Hủy
        ttk.Button(button_frame, text="Tạo hóa đơn", command=on_create).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Hủy", command=dialog.destroy).pack(side="right", padx=5)

    def import_invoices_from_csv(self):
        """Nhập hóa đơn từ file CSV."""
        if self.invoice_manager is None or self.product_manager is None:
            messagebox.showwarning("Cảnh báo", "Trình quản lý chưa được khởi tạo đầy đủ")
            return
            
        # Mở hộp thoại chọn file
        filepath = filedialog.askopenfilename(
            title="Chọn file CSV hóa đơn",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if not filepath:  # Người dùng đã hủy
            return
            
        try:
            # Nhập hóa đơn từ CSV thông qua FileManager
            imported_invoices = self.invoice_manager.file_manager.import_invoices_from_csv(filepath)
            
            if not imported_invoices:
                messagebox.showinfo("Thông báo", "Không có hóa đơn nào được nhập từ file CSV.")
                return
                
            # Xác nhận số lượng hóa đơn sẽ nhập
            confirmed = messagebox.askyesno(
                "Xác nhận", 
                f"Đã tìm thấy {len(imported_invoices)} hóa đơn trong file CSV. Bạn muốn nhập vào hệ thống?"
            )
            
            if not confirmed:
                return
                
            # Thêm từng hóa đơn vào hệ thống
            invoices_added = 0
            invoices_skipped = 0
            
            # Với số lượng lớn (>5), dùng load_invoices() sẽ hiệu quả hơn
            large_import = len(imported_invoices) > 5
            
            for invoice in imported_invoices:
                # Kiểm tra xem hóa đơn đã tồn tại chưa
                existing_invoice = self.invoice_manager.find_invoice(invoice.invoice_id)
                
                if existing_invoice:
                    # Hóa đơn đã tồn tại
                    invoices_skipped += 1
                else:
                    # Kiểm tra tất cả các sản phẩm trong hóa đơn đều tồn tại
                    all_products_exist = True
                    for item in invoice.items:
                        if not self.product_manager.find_product(item.product_id):
                            all_products_exist = False
                            break
                    
                    if all_products_exist:
                        # Thêm hóa đơn mới
                        self.invoice_manager.invoices.append(invoice)
                        
                        # Thêm trực tiếp vào TreeView với số lượng nhỏ
                        if not large_import:
                            self.invoice_tree.insert("", "end", values=(
                                invoice.invoice_id,
                                invoice.customer_name,
                                invoice.date,
                                f"{invoice.total_amount:,.0f}",
                                invoice.total_items
                            ))
                            
                        invoices_added += 1
                    else:
                        invoices_skipped += 1
            
            # Lưu hóa đơn
            if invoices_added > 0:
                self.invoice_manager.file_manager.save_invoices(self.invoice_manager.invoices)
            
            # Thông báo kết quả
            messagebox.showinfo(
                "Kết quả nhập CSV", 
                f"Đã nhập thành công {invoices_added} hóa đơn.\n"
                f"Bỏ qua {invoices_skipped} hóa đơn (đã tồn tại hoặc chứa sản phẩm không tồn tại)."
            )
            
            # Chỉ tải lại danh sách nếu số lượng lớn
            if large_import and invoices_added > 0:
                self.load_invoices()
                
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể nhập hóa đơn từ CSV: {str(e)}")

    def export_invoices_to_csv(self):
        """Xuất hóa đơn ra file CSV."""
        if self.invoice_manager is None:
            messagebox.showwarning("Cảnh báo", "Trình quản lý hóa đơn chưa được khởi tạo")
            return
            
        if not self.invoice_manager.invoices:
            messagebox.showinfo("Thông báo", "Không có hóa đơn nào để xuất")
            return
            
        # Mở hộp thoại lưu file
        filepath = filedialog.asksaveasfilename(
            title="Lưu file CSV hóa đơn",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if not filepath:  # Người dùng đã hủy
            return
            
        try:
            # Xuất hóa đơn ra CSV thông qua FileManager
            self.invoice_manager.file_manager.export_invoices_to_csv(filepath, self.invoice_manager.invoices)
            
            # Thông báo kết quả
            messagebox.showinfo(
                "Thành công", 
                f"Đã xuất {len(self.invoice_manager.invoices)} hóa đơn ra file CSV."
            )
                
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xuất hóa đơn ra CSV: {str(e)}")

    def _create_statistics_tab(self):
        # Tạo các frame cho các loại thống kê
        stats_notebook = ttk.Notebook(self.statistics_tab)
        stats_notebook.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Tạo các tab thống kê
        revenue_tab = ttk.Frame(stats_notebook)
        product_tab = ttk.Frame(stats_notebook)
        customer_tab = ttk.Frame(stats_notebook)
        
        # Thêm các tab vào notebook
        stats_notebook.add(revenue_tab, text="Doanh thu")
        stats_notebook.add(product_tab, text="Sản phẩm")
        stats_notebook.add(customer_tab, text="Khách hàng")
        
        # Tab Doanh thu
        revenue_frame = ttk.LabelFrame(revenue_tab, text="Thống kê doanh thu")
        revenue_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Tạo các nút chức năng cho thống kê doanh thu
        revenue_buttons = ttk.Frame(revenue_frame)
        revenue_buttons.pack(fill="x", padx=5, pady=5)
        
        ttk.Button(revenue_buttons, text="Doanh thu theo sản phẩm", 
                  command=self.show_revenue_by_product).pack(side="left", padx=5)
        
        ttk.Button(revenue_buttons, text="Doanh thu theo thời gian", 
                  command=self.show_revenue_by_time).pack(side="left", padx=5)
        
        # Khu vực hiển thị kết quả thống kê doanh thu
        self.revenue_result = tk.Text(revenue_frame, height=20, width=80)
        self.revenue_result.pack(fill="both", expand=True, padx=5, pady=5)
        self.revenue_result.insert("1.0", "Chọn loại thống kê doanh thu để xem kết quả")
        self.revenue_result.config(state="disabled")
        
        # Tab Sản phẩm
        product_frame = ttk.LabelFrame(product_tab, text="Thống kê sản phẩm")
        product_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Tạo các nút chức năng cho thống kê sản phẩm
        product_buttons = ttk.Frame(product_frame)
        product_buttons.pack(fill="x", padx=5, pady=5)
        
        ttk.Button(product_buttons, text="Sản phẩm bán chạy nhất", 
                  command=self.show_top_products).pack(side="left", padx=5)
        
        ttk.Button(product_buttons, text="Phân loại sản phẩm", 
                  command=self.show_product_categories).pack(side="left", padx=5)
        
        # Khu vực hiển thị kết quả thống kê sản phẩm
        self.product_result = tk.Text(product_frame, height=20, width=80)
        self.product_result.pack(fill="both", expand=True, padx=5, pady=5)
        self.product_result.insert("1.0", "Chọn loại thống kê sản phẩm để xem kết quả")
        self.product_result.config(state="disabled")
        
        # Tab Khách hàng
        customer_frame = ttk.LabelFrame(customer_tab, text="Thống kê khách hàng")
        customer_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Tạo các nút chức năng cho thống kê khách hàng
        customer_buttons = ttk.Frame(customer_frame)
        customer_buttons.pack(fill="x", padx=5, pady=5)
        
        ttk.Button(customer_buttons, text="Khách hàng thân thiết", 
                  command=self.show_top_customers).pack(side="left", padx=5)
        
        # Khu vực hiển thị kết quả thống kê khách hàng
        self.customer_result = tk.Text(customer_frame, height=20, width=80)
        self.customer_result.pack(fill="both", expand=True, padx=5, pady=5)
        self.customer_result.insert("1.0", "Chọn loại thống kê khách hàng để xem kết quả")
        self.customer_result.config(state="disabled")

    def show_revenue_by_product(self):
        try:
            if self.statistics_manager is None:
                messagebox.showwarning("Cảnh báo", "Trình quản lý thống kê chưa được khởi tạo")
                return
            
            # Kiểm tra xem có hóa đơn nào không
            if not self.invoice_manager or not self.invoice_manager.invoices:
                messagebox.showinfo("Thông báo", "Không có dữ liệu hóa đơn để thống kê!")
                return
                
            # Thông báo đang xử lý
            self.revenue_result.config(state="normal")
            self.revenue_result.delete("1.0", tk.END)
            self.revenue_result.insert("1.0", "Đang xử lý dữ liệu...")
            self.revenue_result.config(state="disabled")
            self.root.update()  # Cập nhật giao diện để hiển thị thông báo
            
            # Chuyển hướng stdout để bắt kết quả in ra
            old_stdout = sys.stdout
            result = io.StringIO()
            sys.stdout = result
            
            # Gọi phương thức thống kê
            self.statistics_manager.revenue_by_product()
            
            # Khôi phục stdout và lấy kết quả
            sys.stdout = old_stdout
            output = result.getvalue()
            
            # Hiển thị kết quả trong tab Doanh thu
            self.revenue_result.config(state="normal")
            self.revenue_result.delete("1.0", tk.END)
            self.revenue_result.insert("1.0", output)
            self.revenue_result.config(state="disabled")
            
            # Debug: In ra console để xác định vấn đề
            print("Đã thực hiện thống kê doanh thu theo sản phẩm")
            print(f"Độ dài output: {len(output)}")
            if not output.strip():
                print("Cảnh báo: Output trống!")
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể hiển thị thống kê doanh thu theo sản phẩm: {str(e)}")
            # In thông tin lỗi chi tiết
            import traceback
            print(f"Chi tiết lỗi thống kê doanh thu: {str(e)}")
            print(traceback.format_exc())

    def show_revenue_by_time(self):
        try:
            if self.statistics_manager is None:
                messagebox.showwarning("Cảnh báo", "Trình quản lý thống kê chưa được khởi tạo")
                return
            
            # Kiểm tra xem có hóa đơn nào không
            if not self.invoice_manager or not self.invoice_manager.invoices:
                messagebox.showinfo("Thông báo", "Không có dữ liệu hóa đơn để thống kê!")
                return
                
            # Thông báo đang xử lý
            self.revenue_result.config(state="normal")
            self.revenue_result.delete("1.0", tk.END)
            self.revenue_result.insert("1.0", "Đang xử lý dữ liệu...")
            self.revenue_result.config(state="disabled")
            self.root.update()  # Cập nhật giao diện để hiển thị thông báo
            
            # Chuyển hướng stdout để bắt kết quả in ra
            old_stdout = sys.stdout
            result = io.StringIO()
            sys.stdout = result
            
            # Gọi phương thức thống kê
            self.statistics_manager.revenue_by_date()
            
            # Khôi phục stdout và lấy kết quả
            sys.stdout = old_stdout
            output = result.getvalue()
            
            # Hiển thị kết quả
            self.revenue_result.config(state="normal")
            self.revenue_result.delete("1.0", tk.END)
            self.revenue_result.insert("1.0", output)
            self.revenue_result.config(state="disabled")
            
            # Debug: In ra console để xác định vấn đề
            print("Đã thực hiện thống kê doanh thu theo thời gian")
            print(f"Độ dài output: {len(output)}")
            if not output.strip():
                print("Cảnh báo: Output trống!")
                
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể hiển thị thống kê doanh thu theo thời gian: {str(e)}")
            # In thông tin lỗi chi tiết
            import traceback
            print(f"Chi tiết lỗi thống kê doanh thu theo thời gian: {str(e)}")
            print(traceback.format_exc())

    def show_top_products(self):
        try:
            if self.statistics_manager is None:
                messagebox.showwarning("Cảnh báo", "Trình quản lý thống kê chưa được khởi tạo")
                return
            
            # Kiểm tra xem có hóa đơn nào không
            if not self.invoice_manager or not self.invoice_manager.invoices:
                messagebox.showinfo("Thông báo", "Không có dữ liệu hóa đơn để thống kê!")
                return
            
            # Thông báo đang xử lý
            self.product_result.config(state="normal")
            self.product_result.delete("1.0", tk.END)
            self.product_result.insert("1.0", "Đang xử lý dữ liệu...")
            self.product_result.config(state="disabled")
            self.root.update()  # Cập nhật giao diện để hiển thị thông báo
            
            # Tính toán số lượng sản phẩm bán ra
            product_quantity = defaultdict(int)
            for invoice in self.invoice_manager.invoices:
                for item in invoice.items:
                    product_quantity[item.product_id] += item.quantity
            
            if not product_quantity:
                messagebox.showinfo("Thông báo", "Không có dữ liệu sản phẩm bán ra để hiển thị!")
                return
            
            # Sắp xếp theo số lượng bán ra (cao nhất trước)
            sorted_products = sorted(
                product_quantity.items(),
                key=lambda x: x[1],
                reverse=True
            )
            
            # Tạo báo cáo
            report = io.StringIO()
            report.write("\n" + "="*80 + "\n")
            report.write("TOP SẢN PHẨM BÁN CHẠY NHẤT (THEO SỐ LƯỢNG)\n")
            report.write("="*80 + "\n")
            report.write(f"{'MÃ SP':<10} {'TÊN SẢN PHẨM':<30} {'SỐ LƯỢNG':<10} {'ĐƠN GIÁ':<15} {'DOANH THU':<15}\n")
            report.write("-"*80 + "\n")
            
            for product_id, quantity in sorted_products:
                product = self.product_manager.find_product(product_id)
                if product:
                    product_name = product.name
                    unit_price = product.unit_price
                    revenue = quantity * unit_price
                    report.write(f"{product_id:<10} {product_name:<30} {quantity:>10} {unit_price:>15,.2f} {revenue:>15,.2f}\n")
                else:
                    report.write(f"{product_id:<10} {'[Sản phẩm không tồn tại]':<30} {quantity:>10} {'N/A':>15} {'N/A':>15}\n")
            
            total_quantity = sum(product_quantity.values())
            report.write("-"*80 + "\n")
            report.write(f"{'TỔNG CỘNG:':<40} {total_quantity:>10}\n")
            report.write("="*80 + "\n")
            
            # Hiển thị kết quả
            self.product_result.config(state="normal")
            self.product_result.delete("1.0", tk.END)
            self.product_result.insert("1.0", report.getvalue())
            self.product_result.config(state="disabled")
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể hiển thị thống kê sản phẩm bán chạy: {str(e)}")
            # In thông tin lỗi chi tiết
            import traceback
            print(f"Chi tiết lỗi thống kê sản phẩm bán chạy: {str(e)}")
            print(traceback.format_exc())

    def show_product_categories(self):
        try:
            if self.product_manager is None:
                messagebox.showwarning("Cảnh báo", "Trình quản lý sản phẩm chưa được khởi tạo")
                return
            
            # Nhóm sản phẩm theo danh mục
            categories = {}
            for product in self.product_manager.products:
                category = product.category if product.category else "Chưa phân loại"
                if category not in categories:
                    categories[category] = []
                categories[category].append(product)
            
            # Tạo báo cáo
            report = io.StringIO()
            report.write("=" * 80 + "\n")
            report.write("THỐNG KÊ SẢN PHẨM THEO DANH MỤC\n")
            report.write("=" * 80 + "\n")
            
            total_products = len(self.product_manager.products)
            
            # Sắp xếp danh mục theo thứ tự bảng chữ cái
            for category in sorted(categories.keys()):
                products = categories[category]
                percentage = (len(products) / total_products * 100) if total_products > 0 else 0
                
                report.write(f"\nDANH MỤC: {category} ({len(products)} sản phẩm - {percentage:.2f}%)\n")
                report.write("-" * 80 + "\n")
                report.write(f"{'MÃ SP':<10} {'TÊN SẢN PHẨM':<30} {'ĐƠN VỊ':<10} {'ĐƠN GIÁ':>15}\n")
                report.write("-" * 80 + "\n")
                
                # Sắp xếp sản phẩm theo tên
                for product in sorted(products, key=lambda p: p.name):
                    report.write(f"{product.product_id:<10} {product.name:<30} {product.calculation_unit:<10} {product.unit_price:>15,.2f}\n")
            
            report.write("\n" + "=" * 80 + "\n")
            report.write(f"TỔNG SỐ: {total_products} sản phẩm trong {len(categories)} danh mục\n")
            report.write("=" * 80 + "\n")
            
            # Hiển thị kết quả
            self.product_result.config(state="normal")
            self.product_result.delete("1.0", tk.END)
            self.product_result.insert("1.0", report.getvalue())
            self.product_result.config(state="disabled")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể hiển thị thống kê sản phẩm theo danh mục: {str(e)}")

    def show_top_customers(self):
        try:
            if self.statistics_manager is None:
                messagebox.showwarning("Cảnh báo", "Trình quản lý thống kê chưa được khởi tạo")
                return
                
            # Kiểm tra xem có hóa đơn nào không
            if not self.invoice_manager or not self.invoice_manager.invoices:
                messagebox.showinfo("Thông báo", "Không có dữ liệu hóa đơn để thống kê!")
                return
            
            # Hỏi người dùng về số lượng khách hàng hàng đầu muốn xem
            limit = simpledialog.askinteger(
                "Số lượng khách hàng", 
                "Nhập số lượng khách hàng tiềm năng muốn xem:",
                minvalue=1, maxvalue=20, initialvalue=5
            )
            
            if limit is None:  # Người dùng đã hủy
                return
                
            # Thông báo đang xử lý
            self.customer_result.config(state="normal")
            self.customer_result.delete("1.0", tk.END)
            self.customer_result.insert("1.0", "Đang xử lý dữ liệu...")
            self.customer_result.config(state="disabled")
            self.root.update()  # Cập nhật giao diện để hiển thị thông báo
            
            # Chuyển hướng stdout để bắt kết quả in ra
            old_stdout = sys.stdout
            result = io.StringIO()
            sys.stdout = result
            
            # Gọi phương thức thống kê
            self.statistics_manager.top_customers(limit=limit)
            
            # Khôi phục stdout và lấy kết quả
            sys.stdout = old_stdout
            output = result.getvalue()
            
            # Hiển thị kết quả
            self.customer_result.config(state="normal")
            self.customer_result.delete("1.0", tk.END)
            self.customer_result.insert("1.0", output)
            self.customer_result.config(state="disabled")
            
            # Debug: In ra console để xác định vấn đề
            print(f"Đã thực hiện thống kê {limit} khách hàng tiềm năng")
            print(f"Độ dài output: {len(output)}")
            if not output.strip():
                print("Cảnh báo: Output trống!")
                
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể hiển thị thống kê khách hàng tiềm năng: {str(e)}")
            # In thông tin lỗi chi tiết
            import traceback
            print(f"Chi tiết lỗi thống kê khách hàng tiềm năng: {str(e)}")
            print(traceback.format_exc())

def start_gui():
    """Hàm khởi động giao diện đồ họa"""
    try:
        root = tk.Tk()
        app = InvoiceAppGUI(root)
        root.mainloop()
    except Exception as e:
        # Nếu không thể tạo GUI, hiển thị lỗi
        print(f"Lỗi nghiêm trọng: {str(e)}")
        try:
            error_root = tk.Tk()
            error_root.title("Lỗi nghiêm trọng")
            error_root.geometry("400x200")
            error_label = ttk.Label(error_root, text=f"Đã xảy ra lỗi nghiêm trọng: {str(e)}")
            error_label.pack(padx=20, pady=20)
            ttk.Button(error_root, text="Đóng", command=error_root.destroy).pack(pady=10)
            error_root.mainloop()
        except:
            # Nếu ngay cả cửa sổ lỗi cũng không hiển thị được, chỉ in ra console
            print("Không thể hiển thị cửa sổ lỗi")