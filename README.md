# Hệ thống Quản lý Hóa đơn

Hệ thống Quản lý Hóa đơn là ứng dụng giúp quản lý sản phẩm, hóa đơn và thống kê doanh thu cho doanh nghiệp nhỏ và vừa.

## Tính năng

- **Quản lý Sản phẩm**: Thêm, sửa, xóa và tìm kiếm sản phẩm
- **Quản lý Hóa đơn**: Tạo và quản lý hóa đơn bán hàng
- **Thống kê**: Xem báo cáo doanh thu, sản phẩm bán chạy và khách hàng tiềm năng
- **Nhập/Xuất dữ liệu**: Hỗ trợ nhập/xuất dữ liệu dưới dạng CSV
- **Giao diện thân thiện**: Hỗ trợ cả giao diện đồ họa (GUI) và giao diện dòng lệnh (CLI)

## Cấu trúc dự án

```
final-project/
│
├── sample_data/         # Dữ liệu mẫu để kiểm thử
├── src/                 # Mã nguồn
│   ├── core/            # Logic nghiệp vụ cốt lõi
│   ├── data/            # Các module xử lý dữ liệu
│   ├── invoicemanager/  # Module ứng dụng chính
│   │   └── data/        # Dữ liệu quản lý hóa đơn
│   ├── models/          # Các mô hình dữ liệu
│   ├── ui/              # Giao diện người dùng
│   │   ├── cli/         # Giao diện dòng lệnh
│   │   └── gui/         # Giao diện đồ họa
│   └── utils/           # Các hàm tiện ích
├── tests/               # Bộ kiểm thử
│   ├── integration/     # Kiểm thử tích hợp
│   └── unit/            # Kiểm thử đơn vị
└── pyproject.toml       # Cấu hình dự án
```

## Cài đặt

1. Đảm bảo bạn đã cài đặt Python 3.8 hoặc cao hơn
2. Tải mã nguồn về máy

```bash
git clone https://github.com/minh20051202/PT_2024.2

cd PT_2024.2
```

3. Cài đặt các thư viện cần thiết:

```bash
pip install [TÊN_THƯ_VIỆN]
```

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
