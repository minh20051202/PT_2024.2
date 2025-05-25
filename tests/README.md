# Bài kiểm tra cho Hệ thống Quản lý Hóa đơn

Thư mục này chứa các bài kiểm tra đơn vị và tích hợp cho Hệ thống Quản lý Hóa đơn.

## Cấu trúc thư mục

- **unit/**: Chứa các bài kiểm tra đơn vị cho từng thành phần riêng lẻ

  - `test_validation.py`: Kiểm tra các hàm validation
  - `test_product_model.py`: Kiểm tra mô hình Product
  - `test_invoice_model.py`: Kiểm tra mô hình Invoice và InvoiceItem
  - `test_product_manager.py`: Kiểm tra ProductManager
  - `test_invoice_manager.py`: Kiểm tra InvoiceManager

- **integration/**: Chứa các bài kiểm tra tích hợp cho các thành phần kết hợp
  - `test_main_workflow.py`: Kiểm tra luồng làm việc chính của ứng dụng

## Các điều kiện được kiểm tra

### Các điều kiện thành công (Thỏa mãn tất cả điều kiện)

- Tạo sản phẩm với dữ liệu hợp lệ
- Cập nhật sản phẩm với dữ liệu hợp lệ
- Xóa sản phẩm tồn tại
- Tạo hóa đơn với dữ liệu hợp lệ
- Xem chi tiết hóa đơn tồn tại
- Các tính toán thống kê chính xác

### Các điều kiện thất bại (Không thỏa mãn từng điều kiện một)

- **Validation:**

  - Đơn giá không được âm
  - Các trường bắt buộc không được để trống

- **ProductManager:**

  - Không thể thêm sản phẩm với ID rỗng
  - Không thể thêm sản phẩm với tên rỗng
  - Không thể thêm sản phẩm với đơn giá âm
  - Không thể thêm sản phẩm với ID trùng lặp
  - Không thể cập nhật sản phẩm không tồn tại
  - Không thể cập nhật sản phẩm với đơn giá âm
  - Không thể xóa sản phẩm không tồn tại

- **InvoiceManager:**
  - Không thể tạo hóa đơn với ID rỗng
  - Không thể tạo hóa đơn với tên khách hàng rỗng
  - Không thể tạo hóa đơn với danh sách mặt hàng rỗng
  - Không thể tạo hóa đơn với ID trùng lặp
  - Không thể tạo hóa đơn với sản phẩm không tồn tại
  - Không thể xem chi tiết hóa đơn không tồn tại

## Cách chạy các bài kiểm tra

### Chạy tất cả các bài kiểm tra:

```bash
python -m unittest discover -s tests
```

### Chạy các bài kiểm tra đơn vị:

```bash
python -m unittest discover -s tests/unit
```

### Chạy các bài kiểm tra tích hợp:

```bash
python -m unittest discover -s tests/integration
```

### Chạy một file kiểm tra cụ thể:

```bash
python -m unittest tests/unit/test_validation.py
```

### Chạy một bài kiểm tra cụ thể:

```bash
python -m unittest tests.unit.test_validation.TestValidation.test_validate_positive_number_valid
```
