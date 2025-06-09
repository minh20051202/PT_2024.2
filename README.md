# Chương trình Quản lý Hóa đơn

Chương trình quản lý hóa đơn cho phép quản lý sản phẩm, tạo hóa đơn và thống kê doanh thu.

## Cài đặt

```bash
# 1. Clone repository
git clone https://github.com/minh20051202/PT_2024.2
cd PT_2024.2

# 2. Chạy ứng dụng
python3 src/main.py
```

## 📁 Cấu trúc dự án

PT_2024.2/
├── src/
│   ├── main.py                    # Điểm bắt đầu chương trình
│   ├── models/                    # Mô hình dữ liệu
│   │   ├── product.py             # Mô hình sản phẩm
│   │   └── invoice.py             # Mô hình hoá đơn
│   ├── core/                      # Logic nghiệp vụ
│   │   ├── product_manager.py     # Quản lý sản phẩm
│   │   ├── invoice_manager.py     # Quản lý hoá đơn
│   │   └── statistics_manager.py  # Thống kê
│   ├── database/                  # Tầng cơ sở dữ liệu
│   │   ├── database.py            # Thiết lập SQLite
│   │   └── invoicemanager.db.py   # Cơ sở dữ liệu SQLite
│   ├── utils/                     # Tiện ích hỗ trợ
│   │   ├── validation.py          # Kiểm tra đầu vào
│   │   ├── formatting.py          # Định dạng dữ liệu
│   │   └── db_utils.py            # Tác vụ cơ sở dữ liệu
│   └── ui/                        # Giao diện người dùng
│       └── gui.py                 # Giao diện Tkinter
├── tests/                         # Bộ kiểm thử
│   ├── unit/                      # Kiểm thử đơn vị
│   │   ├── test_db_utils.py       # Test tiện ích cơ sở dữ liệu
│   │   ├── test_formatting.py     # Test định dạng dữ liệu
│   │   ├── test_invoice_manager.py # Test quản lý hóa đơn
│   │   ├── test_invoice_model.py  # Test mô hình hóa đơn
│   │   ├── test_product_manager.py # Test quản lý sản phẩm
│   │   ├── test_product_model.py  # Test mô hình sản phẩm
│   │   ├── test_statistics_manager.py # Test thống kê
│   │   └── test_validation.py     # Test kiểm tra đầu vào
│   ├── integration/               # Kiểm thử tích hợp
│   │   └── test_main_workflow.py  # Test luồng chính
│   ├── conftest.py                # Thiết lập pytest fixtures
│   └── test_helpers.py            # Tiện ích kiểm thử
├── .coveragerc                    # Cấu hình coverage.py
├── requirements.txt               # Thư viện phụ thuộc
└── README.md                      # Tài liệu hướng dẫn

## Cài đặt dependencies
```bash
pip install -r requirements.txt
```

## Sử dụng

### Chạy ứng dụng
```bash
python3 src/main.py
```

### Chạy tests
```bash
# Chạy tất cả tests
pytest tests/ -v

# Test với coverage
pytest tests/ --cov

# Test cụ thể
pytest tests/unit/test_validation.py -v
```
