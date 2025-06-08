# Chương trình Quản lý Hóa đơn

Chương trình quản lý hóa đơn được xây dựng bằng Python với kiến trúc sạch, giao diện thân thiện và độ phủ test cao. Ứng dụng hỗ trợ quản lý sản phẩm, tạo hóa đơn và thống kê doanh thu cho doanh nghiệp vừa và nhỏ.

## Cài đặt nhanh

```bash
# 1. Clone repository
git clone https://github.com/minh20051202/PT_2024.2
cd PT_2024.2

# 2. Chạy ứng dụng
python3 src/main.py
```

**Yêu cầu**: Python 3.8+ (chỉ sử dụng thư viện có sẵn)

## 📁 Cấu trúc dự án

```
PT_2024.2/
├── src/                          # Mã nguồn chính
│   ├── main.py                   # Entry point
│   ├── models/                   # Data models
│   │   ├── product.py            # Model sản phẩm
│   │   └── invoice.py            # Model hóa đơn
│   ├── core/                     # Business logic
│   │   ├── product_manager.py    # Quản lý sản phẩm
│   │   ├── invoice_manager.py    # Quản lý hóa đơn
│   │   └── statistics_manager.py # Thống kê
│   ├── database/                 # Database layer
│   │   └── database.py           # SQLite setup
│   │   └── invoicemanager.db.py  # SQLite database
│   ├── utils/                    # Utilities
│   │   ├── validation.py         # Input validation
│   │   ├── formatting.py         # Data formatting
│   │   ├── db_utils.py           # Database operations
│   └── ui/                       # User interface
│       └── gui.py                # Tkinter GUI
├── tests/                        # Test suite
│   ├── unit/                     # Unit tests
│   ├── integration/              # Integration tests
│   ├── conftest.py               # Pytest fixtures
│   └── test_helpers.py           # Test utilities
└── requirements.txt              # Python dependencies
└── README.md                     # Documentation
```

## 💻 Sử dụng

### Chạy ứng dụng
```bash
python3 src/main.py              # Giao diện GUI
```

## 🧪 Testing
```bash
# Cài đặt dependencies cho testing
pip install pytest pytest-cov
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
