# Hệ thống Quản lý Hóa đơn

Hệ thống Quản lý Hóa đơn là ứng dụng giúp quản lý sản phẩm, hóa đơn và thống kê doanh thu cho doanh nghiệp nhỏ và vừa.

## Tính năng

- **Quản lý Sản phẩm**: Thêm, sửa, xóa và tìm kiếm sản phẩm
- **Quản lý Hóa đơn**: Tạo và quản lý hóa đơn bán hàng
- **Thống kê**: Xem báo cáo doanh thu, sản phẩm bán chạy và khách hàng tiềm năng
- **Cơ sở dữ liệu SQLite**: Lưu trữ dữ liệu bền vững và hiệu quả
- **Giao diện đồ họa**: Giao diện thân thiện sử dụng Tkinter

## Cấu trúc dự án

```
PT_2024.2/
│
├── src/                 # Mã nguồn
│   ├── core/            # Logic nghiệp vụ cốt lõi
│   │   ├── product_manager.py      # Quản lý sản phẩm
│   │   ├── invoice_manager.py      # Quản lý hóa đơn
│   │   └── statistics_manager.py   # Quản lý thống kê
│   ├── database/        # Quản lý cơ sở dữ liệu SQLite
│   │   ├── database.py             # Khởi tạo và cấu hình database
│   │   └── invoicemanager.db       # File database SQLite
│   ├── models/          # Các mô hình dữ liệu
│   │   ├── product.py              # Mô hình sản phẩm
│   │   └── invoice.py              # Mô hình hóa đơn
│   ├── ui/              # Giao diện người dùng
│   │   └── gui.py                  # Giao diện đồ họa Tkinter
│   ├── utils/           # Các hàm tiện ích
│   │   ├── db_utils.py             # Tiện ích database
│   │   ├── file_utils.py           # Tiện ích file
│   │   ├── formatting.py           # Định dạng dữ liệu
│   │   └── validation.py           # Xác thực dữ liệu
│   └── main.py          # Điểm vào chính của ứng dụng
├── tests/               # Bộ kiểm thử
│   ├── integration/     # Kiểm thử tích hợp
│   │   └── test_main_workflow.py
│   └── unit/            # Kiểm thử đơn vị
│       ├── test_product_manager.py
│       ├── test_invoice_manager.py
│       ├── test_product_model.py
│       ├── test_invoice_model.py
│       └── test_validation.py
└── README.md            # Tài liệu dự án
```

## Yêu cầu hệ thống

- Python 3.7 hoặc cao hơn
- Tkinter (thường đã được cài đặt sẵn với Python)
- SQLite3 (thường đã được cài đặt sẵn với Python)

## Cài đặt

1. Tải mã nguồn về máy:

```bash
git clone https://github.com/minh20051202/PT_2024.2
cd PT_2024.2
```

2. Khởi tạo cơ sở dữ liệu (tùy chọn):

```bash
python3 src/database/database.py
```

**Lưu ý**: Ứng dụng sử dụng các thư viện có sẵn trong Python, không cần cài đặt thêm gói nào khác.

## Sử dụng

### Chạy chương trình

Cách đơn giản nhất để chạy chương trình là sử dụng file `src/main.py`:

```bash
# Chạy giao diện đồ họa (GUI) -> mặc định
python src/main.py --gui

# Chạy giao diện dòng lệnh (CLI)
python src/main.py --cli
```

## Hướng dẫn sử dụng

### Quản lý Sản phẩm

- Thêm sản phẩm mới với ID, tên, đơn giá, danh mục và đơn vị tính
- Cập nhật thông tin sản phẩm đã có
- Xóa sản phẩm không còn kinh doanh
- Nhập/xuất danh sách sản phẩm từ/ra file CSV

### Quản lý Hóa đơn

- Tạo hóa đơn mới với thông tin khách hàng và danh sách sản phẩm
- Xem chi tiết hóa đơn đã tạo
- Nhập/xuất danh sách hóa đơn từ/ra file CSV

### Thống kê

- Xem doanh thu theo sản phẩm
- Xem doanh thu theo thời gian
- Xem danh sách sản phẩm bán chạy nhất
- Xem danh sách phân loại sản phẩm theo danh mục
- Xem danh sách khách hàng tiềm năng
