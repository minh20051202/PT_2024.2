# Hệ thống Quản lý Hóa đơn

Hệ thống Quản lý Hóa đơn là ứng dụng giúp quản lý sản phẩm, hóa đơn và thống kê doanh thu cho doanh nghiệp nhỏ và vừa.

## Tính năng

- **Quản lý Sản phẩm**: Thêm, sửa, xóa và tìm kiếm sản phẩm
- **Quản lý Hóa đơn**: Tạo và quản lý hóa đơn bán hàng
- **Thống kê**: Xem báo cáo doanh thu, sản phẩm bán chạy và khách hàng tiềm năng
- **Nhập/Xuất dữ liệu**: Hỗ trợ nhập/xuất dữ liệu dưới dạng CSV
- **Giao diện thân thiện**: Hỗ trợ cả giao diện đồ họa (GUI) và giao diện dòng lệnh (CLI)

## Cài đặt

1. Đảm bảo bạn đã cài đặt Python 3.8 hoặc cao hơn
2. Tải mã nguồn về máy
3. Cài đặt các thư viện cần thiết (nếu cần)

## Sử dụng

### Khởi động nhanh

Cách đơn giản nhất để chạy ứng dụng là sử dụng file `runapp.py`:

```bash
python runapp.py
```

Hoặc làm cho file có quyền thực thi và chạy trực tiếp:

```bash
chmod +x runapp.py
./runapp.py
```

### Chạy từ thư mục nguồn

Bạn cũng có thể chạy từ thư mục nguồn, có thể chọn giao diện GUI hoặc CLI:

```bash
# Chạy giao diện đồ họa (mặc định)
python src/invoicemanager/main.py --gui

# Chạy giao diện dòng lệnh
python src/invoicemanager/main.py --cli
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

## Giải quyết sự cố

Nếu bạn gặp lỗi khi chạy ứng dụng, vui lòng thử các giải pháp sau:

1. Đảm bảo đã cài đặt Python 3.8 hoặc cao hơn
2. Kiểm tra xem các thư viện cần thiết đã được cài đặt chưa
3. Thử chạy file `runapp.py` ở thư mục gốc
4. Nếu GUI không hoạt động, thử chạy ở chế độ CLI với lệnh `python src/invoicemanager/main.py --cli`

## Liên hệ hỗ trợ

Nếu bạn có bất kỳ câu hỏi hoặc đề xuất nào, vui lòng liên hệ qua email hoặc tạo issue trên trang dự án.
# PT_2024.2
