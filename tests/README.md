# Comprehensive Test Suite

This directory contains a comprehensive test suite for the invoice management system.

## Test Structure

```
tests/
├── conftest.py              # Pytest fixtures and configuration
├── test_helpers.py          # Test helper functions and assertions
├── test_runner.py           # Test runner script
├── unit/                    # Unit tests for individual components
│   ├── test_validation.py   # Validation function tests
│   ├── test_db_utils.py     # Database utility tests
│   ├── test_product_model.py # Product model tests
│   ├── test_invoice_model.py # Invoice model tests
│   ├── test_product_manager.py # ProductManager tests
│   ├── test_invoice_manager.py # InvoiceManager tests
│   └── test_formatting.py   # Formatting utility tests
└── integration/             # Integration tests
    └── test_main_workflow.py # End-to-end workflow tests
```

## Running Tests

### Using the Test Runner (Recommended)

```bash
# Run all tests
python tests/test_runner.py

# Run with verbose output
python tests/test_runner.py --verbose

# Run with coverage report
python tests/test_runner.py --coverage

# Run specific test category
python tests/test_runner.py --category unit
python tests/test_runner.py --category integration
python tests/test_runner.py --category validation

# Run specific test file
python tests/test_runner.py --file tests/unit/test_validation.py

# List available test categories
python tests/test_runner.py --list-categories
```

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
