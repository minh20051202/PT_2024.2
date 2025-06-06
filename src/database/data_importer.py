import sqlite3
import json
import os
from datetime import datetime

# Define paths relative to this script file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'invoicemanager.db')
PRODUCTS_JSON_PATH = os.path.join(BASE_DIR, '..', 'invoicemanager', 'data', 'products.json')
INVOICES_JSON_PATH = os.path.join(BASE_DIR, '..', 'invoicemanager', 'data', 'invoices.json')

def clear_data(cursor):
    """Xóa tất cả dữ liệu khỏi các bảng để tránh trùng lặp khi chạy lại."""
    print("Đang xóa dữ liệu hiện có từ các bảng...")
    cursor.execute("DELETE FROM invoice_items;")
    cursor.execute("DELETE FROM products;")
    cursor.execute("DELETE FROM invoices;")
    # Đặt lại chuỗi tự động tăng cho hóa đơn
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='invoices';")
    print("Đã xóa dữ liệu.")

def import_products(cursor, products_data):
    """Nhập sản phẩm vào database."""
    print("Đang nhập sản phẩm...")
    product_count = 0
    for product in products_data:
        try:
            cursor.execute("""
                INSERT INTO products (product_id, name, unit_price, calculation_unit, category)
                VALUES (?, ?, ?, ?, ?)
            """, (
                product['product_id'],
                product['name'],
                product['unit_price'],
                product.get('calculation_unit', 'đơn vị'),
                product.get('category', 'General')
            ))
            product_count += 1
        except sqlite3.IntegrityError:
            print(f"Sản phẩm với ID {product['product_id']} đã tồn tại. Bỏ qua.")
    print(f"Đã nhập {product_count} sản phẩm.")

def import_invoices(cursor, invoices_data):
    """Nhập hóa đơn và các mặt hàng của chúng vào database."""
    print("Đang nhập hóa đơn...")
    invoice_count = 0
    item_count = 0
    for invoice in invoices_data:
        # `invoice_id` gốc (ví dụ: 'INV001') bị bỏ qua.
        # Cột `id` sẽ tự động tăng.
        try:
            invoice_date = invoice.get('date', datetime.now().strftime('%Y-%m-%d'))

            cursor.execute("""
                INSERT INTO invoices (customer_name, date)
                VALUES (?, ?)
            """, (
                invoice['customer_name'],
                invoice_date
            ))
            
            # Lấy ID tự động tăng mới cho hóa đơn
            new_invoice_id = cursor.lastrowid
            invoice_count += 1

            # Bây giờ, chèn các mặt hàng cho hóa đơn này
            for item in invoice.get('items', []):
                cursor.execute("""
                    INSERT INTO invoice_items (invoice_id, product_id, quantity, unit_price)
                    VALUES (?, ?, ?, ?)
                """, (
                    new_invoice_id,
                    item['product_id'],
                    item['quantity'],
                    item['unit_price']
                ))
                item_count += 1

        except KeyError as e:
            print(f"Bỏ qua một hóa đơn do thiếu trường: {e}")
        except Exception as e:
            print(f"Đã xảy ra lỗi khi nhập một hóa đơn: {e}")

    print(f"Đã nhập {invoice_count} hóa đơn và {item_count} mặt hàng.")


def main():
    """Hàm chính để chạy quá trình nhập dữ liệu."""
    
    if not os.path.exists(DB_PATH):
        print(f"Không tìm thấy database tại {DB_PATH}. Vui lòng chạy src/core/database.py trước.")
        return

    # Tải dữ liệu từ các file JSON
    try:
        with open(PRODUCTS_JSON_PATH, 'r', encoding='utf-8') as f:
            products_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Lỗi khi đọc file sản phẩm: {e}")
        return

    try:
        with open(INVOICES_JSON_PATH, 'r', encoding='utf-8') as f:
            invoices_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Lỗi khi đọc file hóa đơn: {e}")
        return
        
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Xóa dữ liệu cũ trước khi nhập
        clear_data(cursor)

        # Nhập sản phẩm trước
        import_products(cursor, products_data)

        # Nhập hóa đơn
        import_invoices(cursor, invoices_data)

        conn.commit()
        print("\nNhập dữ liệu thành công!")

    except sqlite3.Error as e:
        print(f"Lỗi database: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    main() 