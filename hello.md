Hệ thống Quản lý Hóa đơn
Mục lục
Mục lục ……………………………………………………. 2 1 Mô tả Bài toán …………………………………………… 7 2 Cấu trúc Chương trình …………………………………….. 8 2.1 Mô hình hóa Bài toán ……………………………………. 8
📊 Hình ảnh gợi ý: Sơ đồ hệ thống thể hiện mối quan hệ giữa quản lý sản phẩm và hóa đơn.
2.2 Xây dựng các Module Chức năng ……………………………. 9
2.2.1 Kiến trúc Hệ thống ……………………………………. 9
🏗️ Hình ảnh gợi ý: Sơ đồ mô hình MVC minh họa cấu trúc Model, View, Controller.
2.2.2 Lưu trữ Dữ liệu ………………………………………. 9
🗃️ Hình ảnh gợi ý: Sơ đồ ER thể hiện các bảng SQLite (products, invoices, invoice_items).
2.2.3 Xây dựng Chức năng Chính ………………………………. 10
🖥️ Hình ảnh gợi ý: Ảnh chụp màn hình GUI khi chương trình khởi động.
2.2.4 Xây dựng các Lớp Đối tượng …………………………….. 10
📐 Hình ảnh gợi ý: Sơ đồ lớp UML cho Product, Invoice, InvoiceItem.
2.2.5 Triển khai các Hàm Đọc/Ghi …………………………….. 11
💾 Hình ảnh tùy chọn: Mẫu dữ liệu chèn và truy xuất từ cơ sở dữ liệu.
2.2.6 Xây dựng các Hàm Quản lý và Thống kê ……………………. 11
📈 Hình ảnh tùy chọn: Biểu đồ cột doanh thu sản phẩm hoặc danh sách khách hàng hàng đầu.
2.2.7 Tích hợp GUI …………………………………………. 12
🖼️ Hình ảnh gợi ý: Ảnh chụp màn hình các tab GUI (Sản phẩm, Hóa đơn, Thống kê).
3 Thiết kế Chương trình …………………………………….. 14
3.1 Phân tích và Chuẩn bị Thiết kế …………………………… 14
🎯 Hình ảnh tùy chọn: Quy trình thiết kế hệ thống hoặc bảng kế hoạch.
3.2 Kỹ thuật Thiết kế ………………………………………. 15
🔧 Hình ảnh tùy chọn: Sơ đồ thể hiện thiết kế từ trên xuống và phát triển module.
4 Phong cách Lập trình ……………………………………… 17 4.1 Khái niệm Chung ………………………………………… 17 4.1.1 Viết Chương trình Tốt …………………………………. 17 4.1.2 Quy ước Lập trình …………………………………….. 17
4.2 Định dạng Code …………………………………………. 17
📝 Hình ảnh gợi ý: Ảnh chụp màn hình thể hiện căn lề và khoảng cách nhất quán.
4.3 Quy tắc Đặt tên và Chú thích …………………………….. 19
📋 Hình ảnh gợi ý: Đoạn code có chú thích với ví dụ đặt tên và chú thích.
5 Gỡ lỗi và Kiểm thử ………………………………………. 21
5.1 Gỡ lỗi ……………………………………………….. 21 5.1.1 Khái niệm ……………………………………………. 21 5.1.2 Ứng dụng trong Chương trình ……………………………. 21
🐛 Hình ảnh gợi ý: Ví dụ về traceback hoặc sử dụng pdb.
5.2 Kiểm thử ………………………………………………. 22 5.2.1 Khái niệm ……………………………………………. 22 5.2.2 Ứng dụng trong Chương trình ……………………………. 22
🧪 Hình ảnh gợi ý: Biểu đồ coverage test hoặc ảnh chụp màn hình kết quả unittest.
6 Kịch bản Kiểm thử ………………………………………… 25
6.1 Kiểm thử các Tính năng Quản lý Sản phẩm …………………… 26
📦 Hình ảnh gợi ý: - Thêm sản phẩm: ảnh chụp màn hình trước và sau - Chỉnh sửa sản phẩm: nhập dữ liệu và kết quả - Xóa sản phẩm: màn hình xác nhận và kết quả
6.2 Kiểm thử các Tính năng Quản lý Hóa đơn ……………………. 29
🧾 Hình ảnh gợi ý: Ảnh chụp màn hình cửa sổ chi tiết hóa đơn
1 Problem Statement
Hệ thống Quản lý Hóa đơn là ứng dụng Python được thiết kế để quản lý sản phẩm, hóa đơn và thống kê doanh thu cho doanh nghiệp nhỏ và vừa. Mục tiêu chính là xây dựng một hệ thống toàn diện và dễ sử dụng để:
1.	Quản lý sản phẩm: Lưu trữ thông tin về sản phẩm, bao gồm mã, tên, đơn giá, đơn vị tính và danh mục.
2.	Quản lý hóa đơn: Tạo và lưu trữ hóa đơn bán hàng với thông tin khách hàng và danh sách sản phẩm.
3.	Thống kê và báo cáo: Cung cấp các báo cáo thống kê về doanh thu, sản phẩm bán chạy và khách hàng tiềm năng.
Hệ thống cần đảm bảo tính toàn vẹn dữ liệu, khả năng mở rộng và trải nghiệm người dùng tốt thông qua giao diện đồ họa trực quan.
2 Program Structure
2.1 Problem Modeling
Để giải quyết bài toán quản lý hóa đơn, chương trình được thiết kế theo mô hình hóa các đối tượng thực tế và mối quan hệ giữa chúng. Cụ thể, các thực thể chính được mô hình hóa bao gồm:
1.	Sản phẩm (Product): Đại diện cho các mặt hàng được bán.
2.	Hóa đơn (Invoice): Đại diện cho giao dịch bán hàng.
3.	Chi tiết hóa đơn (InvoiceItem): Đại diện cho từng mặt hàng trong hóa đơn.
Mối quan hệ giữa các thực thể này được thể hiện như sau: - Một hóa đơn có thể chứa nhiều sản phẩm (quan hệ 1-n). - Một sản phẩm có thể xuất hiện trong nhiều hóa đơn (quan hệ n-1). - Chi tiết hóa đơn là bảng trung gian liên kết giữa hóa đơn và sản phẩm (quan hệ n-n).
📊 Suggested image: System flowchart showing how product and invoice management relate - demonstrating the relationships between Product, Invoice, and InvoiceItem entities with their cardinalities.
Việc mô hình hóa này cho phép hệ thống quản lý hiệu quả các giao dịch bán hàng, theo dõi sản phẩm và cung cấp thống kê chính xác.
2.2 Building Functional Modules
2.2.1 System Architecture
Hệ thống được xây dựng dựa trên kiến trúc MVC (Model-View-Controller) để phân tách rõ ràng các thành phần và tăng tính bảo trì:
1.	Model (Mô hình): Đại diện bởi các lớp trong thư mục models/, định nghĩa cấu trúc dữ liệu và các quy tắc nghiệp vụ.
o	Product: Định nghĩa cấu trúc dữ liệu sản phẩm.
o	Invoice và InvoiceItem: Định nghĩa cấu trúc dữ liệu hóa đơn và chi tiết hóa đơn.
2.	Controller (Bộ điều khiển): Đại diện bởi các lớp trong thư mục core/, xử lý logic nghiệp vụ và kết nối giữa Model và View.
o	ProductManager: Quản lý các thao tác với sản phẩm.
o	InvoiceManager: Quản lý các thao tác với hóa đơn.
o	StatisticsManager: Quản lý các thao tác thống kê.
3.	View (Giao diện): Đại diện bởi các lớp trong thư mục ui/, hiển thị dữ liệu và tương tác với người dùng.
o	gui.py: Định nghĩa giao diện đồ họa sử dụng Tkinter.
🏗️ Suggested image: MVC model diagram illustrating Model, View, Controller structure - showing the separation of concerns between data models (models/), business logic (core/), and user interface (ui/).
Kiến trúc này cho phép phát triển, bảo trì và mở rộng ứng dụng một cách hiệu quả, đồng thời tạo ra các thành phần có thể tái sử dụng.
2.2.2 Data Storage
Hệ thống sử dụng SQLite làm cơ sở dữ liệu để lưu trữ thông tin về sản phẩm, hóa đơn và chi tiết hóa đơn. Cấu trúc cơ sở dữ liệu bao gồm ba bảng chính:
1.	products: Lưu trữ thông tin về sản phẩm.
o	product_id (TEXT PRIMARY KEY): Mã sản phẩm, là khóa chính.
o	name (TEXT NOT NULL): Tên sản phẩm.
o	unit_price (REAL NOT NULL): Đơn giá sản phẩm.
o	calculation_unit (TEXT): Đơn vị tính (mặc định: “đơn vị”).
o	category (TEXT): Danh mục sản phẩm (mặc định: “General”).
2.	invoices: Lưu trữ thông tin về hóa đơn.
o	id (INTEGER PRIMARY KEY AUTOINCREMENT): Mã hóa đơn tự động tăng.
o	customer_name (TEXT NOT NULL): Tên khách hàng.
o	date (TEXT NOT NULL): Ngày lập hóa đơn (định dạng: YYYY-MM-DD).
3.	invoice_items: Lưu trữ thông tin về các mặt hàng trong hóa đơn.
o	id (INTEGER PRIMARY KEY AUTOINCREMENT): Mã tự động tăng.
o	invoice_id (INTEGER NOT NULL): Liên kết với bảng invoices.
o	product_id (TEXT NOT NULL): Liên kết với bảng products.
o	quantity (INTEGER NOT NULL): Số lượng sản phẩm.
o	unit_price (REAL NOT NULL): Đơn giá tại thời điểm bán.
🗃️ Suggested image: ER diagram showing SQLite tables (products, invoices, invoice_items) - illustrating the database schema with primary keys, foreign keys, and relationships between tables.
Mô hình dữ liệu này đảm bảo tính toàn vẹn dữ liệu thông qua việc sử dụng khóa ngoại và ràng buộc. Ví dụ, khi xóa một hóa đơn, tất cả các mục chi tiết liên quan cũng sẽ được xóa (CASCADE).
2.2.3 Building the Main Functionality
Hệ thống được xây dựng với các chức năng chính sau:
1.	Quản lý sản phẩm:
o	Thêm sản phẩm mới với validation đầy đủ
o	Cập nhật thông tin sản phẩm
o	Xóa sản phẩm với kiểm tra ràng buộc
o	Hiển thị danh sách sản phẩm
2.	Quản lý hóa đơn:
o	Tạo hóa đơn mới với nhiều sản phẩm
o	Xem chi tiết hóa đơn
o	Xóa hóa đơn
o	Hiển thị danh sách hóa đơn
3.	Thống kê và báo cáo:
o	Doanh thu theo sản phẩm
o	Doanh thu theo thời gian
o	Sản phẩm bán chạy nhất
o	Khách hàng thân thiết
🖥️ Suggested image: Screenshot of the GUI when the program starts - showing the main interface with tabs for Product Management, Invoice Management, and Statistics.
Mỗi chức năng được thiết kế để hoạt động độc lập nhưng vẫn có sự tương tác hiệu quả thông qua các giao diện được định nghĩa rõ ràng. Điều này cho phép dễ dàng thêm, sửa hoặc loại bỏ chức năng mà không ảnh hưởng đến các phần khác của hệ thống.
2.2.4 Building Object Classes
Hệ thống sử dụng các lớp đối tượng để mô hình hóa các thực thể và logic nghiệp vụ:
1.	Lớp Product: Định nghĩa trong models/product.py, đại diện cho một sản phẩm.
o	Thuộc tính: product_id, name, unit_price, calculation_unit, category
o	Phương thức: validation trong __post_init__
2.	Lớp Invoice và InvoiceItem: Định nghĩa trong models/invoice.py.
o	InvoiceItem: Đại diện cho một mặt hàng trong hóa đơn với thuộc tính product_id, quantity, unit_price và phương thức tính total_price.
o	Invoice: Đại diện cho một hóa đơn với thuộc tính invoice_id, customer_name, date, items và phương thức tính total_amount và total_items.
3.	Lớp ProductManager: Định nghĩa trong core/product_manager.py, quản lý các thao tác với sản phẩm.
o	Phương thức: load_products, add_product, update_product, delete_product, find_product
4.	Lớp InvoiceManager: Định nghĩa trong core/invoice_manager.py, quản lý các thao tác với hóa đơn.
o	Phương thức: load_invoices, create_invoice, delete_invoice, find_invoice
5.	Lớp StatisticsManager: Định nghĩa trong core/statistics_manager.py, quản lý các thao tác thống kê.
o	Phương thức: revenue_by_date, revenue_by_product, top_customers
📐 Suggested image: UML class diagram for Product, Invoice, InvoiceItem - showing the class attributes, methods, and relationships between the main data models.
Các lớp này được thiết kế theo nguyên tắc trách nhiệm đơn lẻ (Single Responsibility Principle), giúp code dễ đọc, dễ bảo trì và dễ mở rộng.
2.2.5 Implementing Read/Write Functions
Để đảm bảo tính nhất quán và hiệu quả trong việc truy cập dữ liệu, hệ thống sử dụng các hàm tiện ích trong utils/db_utils.py để thực hiện các thao tác đọc/ghi với cơ sở dữ liệu SQLite:
1.	save_data: Lưu dữ liệu mới vào bảng.
 	def save_data(table: str, data: Dict[str, Any]) -> Tuple[bool, str]:
    # Tạo câu lệnh INSERT
    columns = ', '.join(data.keys())
    placeholders = ', '.join(['?' for _ in data])
    query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
    cursor.execute(query, tuple(data.values()))
2.	load_data: Tải dữ liệu từ bảng với điều kiện tùy chọn.
 	def load_data(table: str, conditions: Dict[str, Any] = None) -> Tuple[List[Dict[str, Any]], str]:
    # Tạo câu lệnh SELECT
    query = f"SELECT * FROM {table}"
    if conditions:
        where_clauses = []
        for key, value in conditions.items():
            where_clauses.append(f"{key} = ?")
        query += " WHERE " + " AND ".join(where_clauses)
3.	update_data: Cập nhật dữ liệu trong bảng theo điều kiện.
 	def update_data(table: str, data: Dict[str, Any], conditions: Dict[str, Any]) -> Tuple[bool, str]:
    # Tạo câu lệnh UPDATE
    set_clauses = [f"{key} = ?" for key in data.keys()]
    where_clauses = [f"{key} = ?" for key in conditions.keys()]
    query = f"UPDATE {table} SET {', '.join(set_clauses)} WHERE {' AND '.join(where_clauses)}"
4.	delete_data: Xóa dữ liệu từ bảng theo điều kiện.
 	def delete_data(table: str, conditions: Dict[str, Any]) -> Tuple[bool, str]:
    # Tạo câu lệnh DELETE
    where_clauses = [f"{key} = ?" for key in conditions.keys()]
    query = f"DELETE FROM {table} WHERE {' AND '.join(where_clauses)}"
💾 Optional image: Sample data insert and retrieval from the database - showing examples of SQL operations and how data flows between the application and SQLite database.
Các hàm này cung cấp một interface đơn giản và an toàn để tương tác với cơ sở dữ liệu, đồng thời xử lý các lỗi và trả về thông báo rõ ràng. Việc sử dụng tham số hóa câu lệnh SQL giúp ngăn chặn các lỗ hổng SQL injection.
2.2.6 Building Management and Statistics Functions
Các chức năng quản lý và thống kê được xây dựng dựa trên các lớp quản lý trong thư mục core/:
1.	Quản lý sản phẩm (ProductManager):
o	load_products(): Tải tất cả sản phẩm từ database.
o	add_product(): Thêm sản phẩm mới với validation.
o	update_product(): Cập nhật thông tin sản phẩm.
o	delete_product(): Xóa sản phẩm với kiểm tra ràng buộc.
o	find_product(): Tìm sản phẩm theo mã.
2.	Quản lý hóa đơn (InvoiceManager):
o	load_invoices(): Tải tất cả hóa đơn và chi tiết từ database.
o	create_invoice(): Tạo hóa đơn mới với danh sách sản phẩm.
o	delete_invoice(): Xóa hóa đơn và các chi tiết liên quan.
o	find_invoice(): Tìm hóa đơn theo mã.
3.	Thống kê (StatisticsManager):
o	revenue_by_date(): Thống kê doanh thu theo ngày.
o	revenue_by_product(): Thống kê doanh thu theo sản phẩm.
o	top_customers(): Hiển thị danh sách khách hàng chi tiêu nhiều nhất.
📈 Optional image: Bar chart of product revenue or list of top customers - demonstrating the output of statistics functions like revenue analysis and customer ranking.
Các chức năng này tương tác với database thông qua các hàm tiện ích trong utils/db_utils.py và áp dụng các quy tắc nghiệp vụ để đảm bảo tính toàn vẹn và chính xác của dữ liệu.
2.2.7 GUI Integration
Giao diện đồ họa của hệ thống được xây dựng sử dụng Tkinter, một thư viện GUI tiêu chuẩn trong Python. Giao diện được tổ chức theo cấu trúc tab, với mỗi tab đại diện cho một chức năng chính của hệ thống:
1.	Tab Quản lý Sản phẩm:
o	Hiển thị danh sách sản phẩm trong Treeview
o	Các nút chức năng: Tải lại, Thêm, Cập nhật, Xóa
o	Form thêm/cập nhật sản phẩm với validation
2.	Tab Quản lý Hóa đơn:
o	Hiển thị danh sách hóa đơn trong Treeview
o	Các nút chức năng: Tải lại, Xem chi tiết, Tạo hóa đơn, Xóa hóa đơn
o	Form tạo hóa đơn mới với chọn sản phẩm và số lượng
3.	Tab Thống kê:
o	Các tab con: Doanh thu, Sản phẩm, Khách hàng
o	Các nút chức năng cho từng loại thống kê
o	Khu vực hiển thị kết quả thống kê
Mã nguồn của giao diện đồ họa được định nghĩa trong lớp InvoiceAppGUI trong tập tin ui/gui.py. Lớp này kết nối với các lớp quản lý để hiển thị và cập nhật dữ liệu, đồng thời xử lý các sự kiện người dùng.
Một ví dụ về cách kết nối GUI với lớp quản lý:
def load_products(self):
    """Tải lại danh sách sản phẩm từ manager và cập nhật Treeview."""
    try:
        success, message = self.product_manager.load_products()
        if not success:
            messagebox.showerror("Lỗi", f"Không thể tải danh sách sản phẩm: {message}")
            return

        # Xóa dữ liệu cũ
        for item in self.product_tree.get_children():
            self.product_tree.delete(item)

        # Hiển thị dữ liệu mới
        for product in self.product_manager.products:
            self.product_tree.insert("", "end", values=(
                product.product_id,
                product.name,
                f"{product.unit_price:,.0f}",
                product.calculation_unit,
                product.category
            ))
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể tải danh sách sản phẩm: {str(e)}")
🖼️ Suggested image: Screenshot of GUI tabs (Product, Invoice, Statistics) - showing the complete user interface with all functional areas clearly visible.
3 Program Design
3.1 Analysis and Design Preparation
Quá trình phân tích và thiết kế của Hệ thống Quản lý Hóa đơn tuân theo các bước sau:
1.	Thu thập yêu cầu: Xác định các chức năng cần thiết của hệ thống dựa trên nhu cầu của người dùng và các quy trình nghiệp vụ.
2.	Phân tích yêu cầu: Phân tích các yêu cầu chức năng và phi chức năng để hiểu rõ phạm vi và giới hạn của hệ thống.
3.	Thiết kế cơ sở dữ liệu: Xác định các thực thể chính (sản phẩm, hóa đơn, chi tiết hóa đơn) và mối quan hệ giữa chúng, sau đó thiết kế cấu trúc bảng.
4.	Thiết kế kiến trúc: Áp dụng mô hình MVC để phân tách rõ ràng các thành phần và tăng tính bảo trì của hệ thống.
5.	Thiết kế lớp: Xác định các lớp cần thiết, thuộc tính và phương thức của mỗi lớp, cũng như mối quan hệ giữa các lớp.
6.	Thiết kế giao diện người dùng: Thiết kế UI trực quan và dễ sử dụng, tổ chức theo cấu trúc tab để truy cập dễ dàng các chức năng.
7.	Xác định các quy tắc nghiệp vụ: Định nghĩa các quy tắc validation và xử lý lỗi để đảm bảo tính toàn vẹn dữ liệu.
🎯 Optional image: System design workflow or planning board - illustrating the systematic approach to analysis and design preparation.
Việc phân tích và thiết kế kỹ lưỡng đã giúp xây dựng một hệ thống có cấu trúc rõ ràng, dễ bảo trì và mở rộng.
3.2 Design Techniques
Trong quá trình thiết kế Hệ thống Quản lý Hóa đơn, một số kỹ thuật thiết kế quan trọng đã được áp dụng:
1.	Thiết kế từ trên xuống (Top-down Design): Bắt đầu từ cái nhìn tổng quan về hệ thống và dần chi tiết hóa từng thành phần.
o	Ví dụ: Hệ thống được chia thành các module chính (quản lý sản phẩm, quản lý hóa đơn, thống kê), sau đó mỗi module được chi tiết hóa thành các chức năng cụ thể.
2.	Thiết kế hướng đối tượng (Object-Oriented Design):
o	Tính đóng gói (Encapsulation): Mỗi lớp đóng gói dữ liệu và hành vi liên quan.
 	@dataclass
class Product:
    product_id: str
    name: str
    unit_price: float
    calculation_unit: str = field(default="đơn vị")
    category: str = field(default="General")
o	Tính kế thừa (Inheritance): Sử dụng kế thừa khi cần mở rộng chức năng.
o	Tính đa hình (Polymorphism): Sử dụng interface chung cho các đối tượng khác nhau.
3.	Mẫu thiết kế (Design Patterns):
o	Singleton: Đảm bảo chỉ có một instance của database connection.
o	Factory: Tạo đối tượng mà không cần chỉ định chính xác lớp.
o	Observer: Cập nhật UI khi dữ liệu thay đổi.
4.	Thiết kế module (Modular Design): Chia hệ thống thành các module có tính độc lập cao, giúp dễ dàng bảo trì và mở rộng.
o	core/: Chứa logic nghiệp vụ
o	models/: Chứa các mô hình dữ liệu
o	utils/: Chứa các hàm tiện ích
o	ui/: Chứa giao diện người dùng
5.	Thiết kế cơ sở dữ liệu (Database Design):
o	Áp dụng các nguyên tắc chuẩn hóa để giảm thiểu dư thừa dữ liệu.
o	Sử dụng khóa ngoại và ràng buộc để đảm bảo tính toàn vẹn dữ liệu.
o	Thiết kế các bảng liên kết (invoice_items) để thể hiện quan hệ nhiều-nhiều.
6.	Thiết kế giao diện (Interface Design):
o	Áp dụng nguyên tắc thiết kế UI đơn giản, nhất quán và trực quan.
o	Tổ chức UI theo cấu trúc tab logic, giúp người dùng dễ dàng tìm và sử dụng các chức năng.
🔧 Optional image: Diagram showing top-down design and modular development - demonstrating how the system is broken down from high-level concepts to specific implementation modules.
Các kỹ thuật thiết kế này giúp tạo ra một hệ thống có cấu trúc rõ ràng, dễ bảo trì và mở rộng, đồng thời đáp ứng được các yêu cầu của người dùng.
4 Programming Style
4.1 General Concepts
4.1.1 Writing Good Programs
Một chương trình tốt cần đáp ứng các tiêu chí sau, và Hệ thống Quản lý Hóa đơn đã áp dụng những nguyên tắc này:
1.	Chính xác (Correctness): Chương trình phải thực hiện đúng các chức năng yêu cầu và xử lý đúng đắn các trường hợp đặc biệt.
o	Ví dụ: Validation đầu vào kỹ lưỡng, xử lý lỗi toàn diện.
2.	Hiệu quả (Efficiency): Sử dụng tài nguyên (thời gian CPU, bộ nhớ) một cách hiệu quả.
o	Ví dụ: Tối ưu hóa truy vấn database, chỉ tải dữ liệu cần thiết.
3.	Dễ đọc (Readability): Code phải dễ đọc và hiểu, giúp giảm chi phí bảo trì.
o	Ví dụ: Sử dụng tên biến có ý nghĩa, docstrings đầy đủ, cấu trúc rõ ràng.
4.	Dễ bảo trì (Maintainability): Dễ dàng sửa lỗi và thêm tính năng mới.
o	Ví dụ: Tổ chức code theo module, giảm thiểu sự phụ thuộc.
5.	Khả chuyển (Portability): Có thể chạy trên nhiều nền tảng khác nhau.
o	Ví dụ: Sử dụng thư viện tiêu chuẩn Python, SQLite cho database.
4.1.2 Coding Conventions
Hệ thống Quản lý Hóa đơn tuân thủ các quy ước coding sau:
1.	PEP 8: Tuân thủ chuẩn coding style của Python.
o	Sử dụng 4 khoảng trắng cho indentation.
o	Giới hạn độ dài dòng 79-80 ký tự.
o	Đặt khoảng trắng xung quanh toán tử.
2.	Docstrings: Sử dụng docstrings cho modules, classes, functions.
o	Mô tả ngắn gọn về chức năng.
o	Liệt kê parameters và return values.
o	Cung cấp ví dụ nếu cần thiết.
3.	Type Hints: Sử dụng type hints để tăng tính rõ ràng và hỗ trợ IDE.
 	def save_data(table: str, data: Dict[str, Any]) -> Tuple[bool, str]:
4.	Error Handling: Xử lý lỗi với try-except blocks, cung cấp thông báo lỗi rõ ràng.
 	try:
    # Thực hiện thao tác
except Exception as e:
    return False, f"Lỗi: {str(e)}"
5.	DRY (Don’t Repeat Yourself): Tránh trùng lặp code, sử dụng hàm và lớp để tái sử dụng code.
4.2 Code Formatting
Code formatting là một phần quan trọng trong việc viết code dễ đọc và dễ bảo trì. Hệ thống Quản lý Hóa đơn áp dụng các quy tắc định dạng sau:
1.	Indentation: Sử dụng 4 khoảng trắng cho mỗi level indentation, không sử dụng tab.
 	def find_product(self, product_id: str) -> Optional[Product]:
    """Tìm kiếm sản phẩm theo ID trong danh sách đã tải."""
    product_id = format_product_id(product_id)
    for product in self.products:
        if product.product_id == product_id:
            return product
    return None
2.	Line Length: Giới hạn độ dài dòng không quá 79 ký tự để dễ đọc trên màn hình nhỏ và có thể in ấn.
 	# Dòng quá dài
result = calculate_something(very_long_variable_name1, very_long_variable_name2, very_long_variable_name3)

# Được định dạng lại
result = calculate_something(
    very_long_variable_name1,
    very_long_variable_name2,
    very_long_variable_name3
)
3.	Import Statements: Sắp xếp import theo thứ tự: standard library, third-party library, local application.
 	# Standard library
import os
import sqlite3
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# Local application
from models import Product
from utils.db_utils import load_data, save_data
4.	Khoảng trắng (Whitespace):
o	Đặt khoảng trắng xung quanh toán tử: a = b + c
o	Không đặt khoảng trắng trong dấu ngoặc: func(arg1, arg2)
o	Đặt một khoảng trắng sau dấu phẩy: func(a, b, c)
o	Không đặt khoảng trắng trước dấu phẩy: func(a, b)
5.	Dấu ngoặc (Brackets):
o	Sử dụng dấu ngoặc đơn cho tuples, parameters: (a, b)
o	Sử dụng dấu ngoặc vuông cho lists: [1, 2, 3]
o	Sử dụng dấu ngoặc nhọn cho dictionaries: {'a': 1, 'b': 2}
6.	Docstrings: Sử dụng triple quotes (""") cho docstrings, với dòng đầu là mô tả ngắn gọn và các dòng tiếp theo là mô tả chi tiết.
 	def format_date(date: Union[str, datetime], input_format: str = "%Y-%m-%d", output_format: str = "%d/%m/%Y") -> str:
    """
    Định dạng ngày tháng.

    Tham số:
        date: Ngày tháng cần định dạng (chuỗi hoặc datetime)
        input_format: Định dạng đầu vào (nếu date là chuỗi)
        output_format: Định dạng đầu ra

    Trả về:
        Chuỗi ngày tháng đã định dạng
    """
7.	Comments: Sử dụng # cho comments, với khoảng trắng sau dấu #.
 	# Đây là một comment
x = 5  # Comment inline
📝 Suggested image: Screenshot showing consistent indentation and spacing - demonstrating proper code formatting with 4-space indentation, proper line spacing, and organized imports.
Việc tuân thủ các quy tắc định dạng này giúp code dễ đọc, dễ hiểu và dễ bảo trì, đồng thời tạo ra một style nhất quán trong toàn bộ codebase.
4.3 Naming Rules and Comments
Hệ thống Quản lý Hóa đơn áp dụng các quy tắc đặt tên và comment sau:
1.	Quy tắc đặt tên:
o	Tên module và package: Viết thường, ngắn gọn, có thể sử dụng underscore.
 	core/product_manager.py
utils/db_utils.py
o	Tên class: Sử dụng PascalCase (viết hoa chữ cái đầu của mỗi từ).
 	class ProductManager:
class InvoiceItem:
o	Tên function và method: Sử dụng snake_case (viết thường, các từ nối bằng underscore).
 	def load_products():
def find_invoice():
o	Tên biến: Sử dụng snake_case, đặt tên có ý nghĩa.
 	product_id = "P001"
customer_name = "Nguyễn Văn A"
o	Hằng số: Viết HOA, các từ nối bằng underscore.
 	DATABASE_NAME = "invoicemanager.db"
o	Tên tham số: Sử dụng snake_case, đặt tên có ý nghĩa.
 	def add_product(product_id: str, name: str, unit_price: float):
2.	Comments:
o	Docstrings: Sử dụng để mô tả modules, classes, functions. Docstrings được viết bằng tiếng Việt để phù hợp với yêu cầu của dự án.
 	def validate_product_id(product_id: str) -> Tuple[bool, str]:
    """
    Kiểm tra định dạng mã sản phẩm.

    Tham số:
        product_id: Mã sản phẩm cần kiểm tra

    Trả về:
        Tuple[bool, str]: (True/False, thông báo lỗi nếu có)
    """
o	Block comments: Mô tả một khối code phức tạp, giúp người đọc hiểu logic của code.
 	# Nhóm doanh thu theo ngày và tính tổng
date_revenue = defaultdict(float)
for invoice in self.invoice_manager.invoices:
    date_revenue[invoice.date] += invoice.total_amount
o	Inline comments: Giải thích một dòng code cụ thể, đặt sau code và cách ít nhất 2 khoảng trắng.
 	product_id = format_product_id(product_id)  # Chuẩn hóa mã sản phẩm
o	TODO comments: Đánh dấu các phần cần hoàn thiện hoặc cải thiện trong tương lai.
 	# TODO: Cải thiện hiệu suất khi xử lý dữ liệu lớn
3.	Sử dụng comments hiệu quả:
o	Tập trung vào giải thích tại sao (why) thay vì làm gì (what).
o	Tránh comments thừa, chỉ comment khi cần thiết để giải thích logic phức tạp.
o	Cập nhật comments khi code thay đổi để tránh comments lỗi thời.
o	Sử dụng ngôn ngữ rõ ràng, súc tích trong comments.
📋 Suggested image: Annotated code snippet with naming and comment examples - showing proper variable naming, function naming, class naming, and effective commenting practices.
Việc tuân thủ các quy tắc đặt tên và comment này giúp code dễ đọc, dễ hiểu và dễ bảo trì, đồng thời tạo ra một style nhất quán trong toàn bộ codebase.
5 Debugging and Testing
5.1 Debugging
5.1.1 Concept
Debugging là quá trình tìm và sửa lỗi trong chương trình. Trong Hệ thống Quản lý Hóa đơn, debugging là một phần quan trọng của quy trình phát triển để đảm bảo chất lượng phần mềm.
Các loại lỗi thường gặp: 1. Syntax Errors: Lỗi cú pháp, được phát hiện bởi trình biên dịch/thông dịch. 2. Runtime Errors: Lỗi xảy ra khi chương trình đang chạy (ví dụ: chia cho 0, truy cập index ngoài phạm vi). 3. Logical Errors: Chương trình chạy nhưng kết quả không đúng như mong đợi.
Các kỹ thuật debugging: 1. Print Debugging: Thêm các câu lệnh print để theo dõi giá trị biến, luồng thực thi. 2. Logging: Sử dụng module logging để ghi lại thông tin chi tiết về hoạt động của chương trình. 3. Debugger: Sử dụng các công cụ debugger như pdb, IDE debugger để kiểm tra chương trình từng bước. 4. Exception Handling: Bắt và xử lý các ngoại lệ để hiểu rõ nguyên nhân lỗi.
5.1.2 Application in the Program
Trong Hệ thống Quản lý Hóa đơn, các kỹ thuật debugging sau đã được áp dụng:
1.	Xử lý ngoại lệ (Exception Handling):
 	try:
    success, message = self.product_manager.load_products()
    if not success:
        messagebox.showerror("Lỗi", f"Không thể tải danh sách sản phẩm: {message}")
        return
    # ...
except Exception as e:
    messagebox.showerror("Lỗi", f"Không thể tải danh sách sản phẩm: {str(e)}")
2.	Thông báo lỗi rõ ràng:
 	if not self.find_product(product_id):
    return False, f"Không tìm thấy sản phẩm với Mã '{product_id}'!"
3.	Validation đầu vào:
 	valid, error = validate_product_id(product_id)
if not valid:
    return False, error
valid, error = validate_required_field(name, "Tên sản phẩm")
if not valid:
    return False, error
4.	Kiểm tra điều kiện tiên quyết:
 	if not items_data:
    return None, "Hóa đơn phải có ít nhất một mặt hàng."
5.	Log lỗi đến UI thay vì console:
 	messagebox.showerror("Lỗi", f"Không thể tạo hóa đơn: {str(e)}")
🐛 Suggested image: Example of traceback or pdb usage - showing debugging techniques in action, such as error messages, stack traces, or debugger interface.
Các kỹ thuật này giúp: - Phát hiện và xử lý lỗi một cách hiệu quả - Cung cấp thông tin hữu ích cho người dùng khi xảy ra lỗi - Ngăn chặn chương trình crash khi gặp lỗi - Tạo điều kiện thuận lợi cho việc sửa lỗi và bảo trì
5.2 Testing
5.2.1 Concept
Testing là quá trình kiểm tra chương trình để đảm bảo nó hoạt động đúng như thiết kế và đáp ứng các yêu cầu. Testing giúp phát hiện lỗi trước khi phần mềm được triển khai và sử dụng.
Các loại testing: 1. Unit Testing: Kiểm tra các đơn vị nhỏ nhất của code (functions, methods, classes) một cách độc lập. 2. Integration Testing: Kiểm tra sự tương tác giữa các thành phần khi chúng được kết hợp với nhau. 3. System Testing: Kiểm tra toàn bộ hệ thống để đảm bảo nó đáp ứng các yêu cầu. 4. Acceptance Testing: Kiểm tra xem hệ thống có đáp ứng nhu cầu của người dùng không.
Các kỹ thuật testing: 1. Manual Testing: Kiểm tra bằng tay, thực hiện các thao tác và kiểm tra kết quả. 2. Automated Testing: Sử dụng các công cụ và scripts để tự động hóa quá trình kiểm tra. 3. Test-Driven Development (TDD): Viết test trước, sau đó viết code để pass test. 4. Black-box Testing: Kiểm tra chức năng mà không cần biết cấu trúc bên trong. 5. White-box Testing: Kiểm tra dựa trên cấu trúc và logic bên trong của code.
5.2.2 Application in the Program
Hệ thống Quản lý Hóa đơn sử dụng pytest làm framework testing chính, với **143 tests** và **coverage 95%** trên các module cốt lõi. Các loại test đã được triển khai:
1.	Unit Tests:
o	Test cho các hàm validation
 	def test_validate_product_id_valid():
    assert validate_product_id("P001") == (True, "")
    assert validate_product_id("ABC123") == (True, "")
o	Test cho các hàm formatting
 	def test_format_date():
    assert format_date("2023-05-15") == "15/05/2023"
    assert format_date("") == ""
o	Test cho các models
 	def test_product_model_valid():
    product = Product(product_id="P001", name="Test Product", unit_price=100)
    assert product.product_id == "P001"
    assert product.name == "Test Product"
    assert product.unit_price == 100
2.	Integration Tests:
o	Test cho luồng làm việc end-to-end
 	def test_create_invoice_workflow():
    # Setup
    product_manager = ProductManager()
    invoice_manager = InvoiceManager(product_manager)

    # Add product
    product_manager.add_product("P001", "Test Product", 100)

    # Create invoice
    items_data = [{"product_id": "P001", "quantity": 2}]
    invoice, _ = invoice_manager.create_invoice("Test Customer", items_data)

    # Verify
    assert invoice is not None
    assert invoice.customer_name == "Test Customer"
    assert len(invoice.items) == 1
    assert invoice.items[0].product_id == "P001"
    assert invoice.items[0].quantity == 2
    assert invoice.total_amount == 200
3.	Mocking:
o	Mock database để test không ảnh hưởng đến dữ liệu thật
 	@pytest.fixture
def mock_db_connection(monkeypatch):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    monkeypatch.setattr('sqlite3.connect', lambda _: mock_conn)
    return mock_conn, mock_cursor
4.	Fixtures:
o	Tạo dữ liệu test có thể tái sử dụng
 	@pytest.fixture
def sample_products():
    return [
        Product(product_id="P001", name="Product 1", unit_price=100),
        Product(product_id="P002", name="Product 2", unit_price=200),
    ]
5.	Test Categories:
o	Validation tests: 22 tests (100% coverage)
o	DB Utils tests: 17 tests (95% coverage)
o	Formatting tests: 31 tests (90% coverage)
o	Product model tests: 9 tests (100% coverage)
o	Invoice model tests: 6 tests (100% coverage)
o	Product Manager tests: 10 tests (77% coverage)
o	Invoice Manager tests: 7 tests (63% coverage)
o	Integration tests: 2 tests
7.	Testing Tools:
o	pytest: Framework testing chính
o	pytest-cov: Đo lường test coverage
o	pytest fixtures: Tạo và quản lý test data
o	monkeypatch: Thay thế tạm thời các hàm và attributes
6.	Coverage Analysis:
o	Core utilities (validation, db_utils, formatting): 90-100% coverage
o	Data models (Product, Invoice): 100% coverage
o	Business logic managers: 63-77% coverage
o	GUI components: Requires integration testing
o	Statistics module: Requires additional test development
🧪 Suggested image: Test coverage chart or unittest output screenshot - displaying test results, coverage percentages, and test execution summary.
Thông qua việc áp dụng các kỹ thuật testing này, Hệ thống Quản lý Hóa đơn đảm bảo chất lượng cao cho các thành phần cốt lõi, với kế hoạch mở rộng testing cho GUI và statistics modules.
6 Test Scenarios
6.1 Testing Product Management Features
Việc kiểm thử các chức năng quản lý sản phẩm là rất quan trọng để đảm bảo hệ thống có thể lưu trữ và quản lý thông tin sản phẩm một cách chính xác. Dưới đây là các kịch bản kiểm thử chi tiết:
📦 Suggested images: - Adding product: Before and after screenshot showing the product addition form and the updated product list - Editing product: Data entry form with validation and the result in the product list - Deleting product: Confirmation dialog and the result screen showing the product removed from the list
1. Thêm sản phẩm mới
Kịch bản: Thêm một sản phẩm mới vào hệ thống với thông tin hợp lệ.
Bước thực hiện: 1. Mở ứng dụng và chuyển đến tab “Quản lý Sản phẩm” 2. Nhấn nút “Thêm” 3. Nhập thông tin sản phẩm: - Mã sản phẩm: “LAPTOP01” - Tên sản phẩm: “Laptop Dell XPS 13” - Đơn giá: 25000000 - Đơn vị tính: “chiếc” - Danh mục: “Electronics” 4. Nhấn nút “Thêm” để lưu sản phẩm
Kết quả mong đợi: - Hiển thị thông báo thành công: “Đã thêm sản phẩm ‘Laptop Dell XPS 13’ thành công!” - Sản phẩm mới xuất hiện trong danh sách sản phẩm với thông tin chính xác
Kiểm tra validation: - Mã sản phẩm để trống: Hiển thị lỗi “Mã sản phẩm là bắt buộc.” - Mã sản phẩm không hợp lệ (ví dụ: “lap-01”): Hiển thị lỗi “Mã sản phẩm chỉ được chứa chữ in hoa và số.” - Tên sản phẩm để trống: Hiển thị lỗi “Tên sản phẩm là bắt buộc.” - Đơn giá không hợp lệ (ví dụ: “abc”): Hiển thị lỗi “Đơn giá phải là một số.” - Đơn giá âm: Hiển thị lỗi “Đơn giá phải lớn hơn 0.” - Mã sản phẩm đã tồn tại: Hiển thị lỗi “Sản phẩm với Mã ‘LAPTOP01’ đã tồn tại!”
2. Cập nhật thông tin sản phẩm
Kịch bản: Cập nhật thông tin của một sản phẩm đã tồn tại.
Bước thực hiện: 1. Mở ứng dụng và chuyển đến tab “Quản lý Sản phẩm” 2. Chọn một sản phẩm từ danh sách (ví dụ: “LAPTOP01”) 3. Nhấn nút “Cập nhật” 4. Sửa đổi thông tin: - Tên sản phẩm: “Laptop Dell XPS 15” - Đơn giá: 30000000 5. Nhấn nút “Cập nhật” để lưu thay đổi
Kết quả mong đợi: - Hiển thị thông báo thành công: “Đã cập nhật sản phẩm ‘LAPTOP01’ thành công!” - Thông tin sản phẩm trong danh sách được cập nhật với giá trị mới
Kiểm tra validation: - Tên sản phẩm để trống: Hiển thị lỗi “Tên sản phẩm là bắt buộc.” - Đơn giá không hợp lệ: Hiển thị lỗi phù hợp - Thử cập nhật sản phẩm không tồn tại: Hiển thị lỗi “Không tìm thấy sản phẩm với Mã ‘…’”
3. Xóa sản phẩm
Kịch bản: Xóa một sản phẩm khỏi hệ thống.
Bước thực hiện: 1. Mở ứng dụng và chuyển đến tab “Quản lý Sản phẩm” 2. Chọn một sản phẩm từ danh sách (ví dụ: “LAPTOP01”) 3. Nhấn nút “Xóa” 4. Xác nhận xóa sản phẩm khi hộp thoại hiện lên
Kết quả mong đợi: - Hiển thị thông báo xác nhận: “Bạn có chắc chắn muốn xóa sản phẩm ‘LAPTOP01’? Hành động này không thể hoàn tác.” - Sau khi xác nhận, hiển thị thông báo thành công: “Đã xóa sản phẩm ‘LAPTOP01’ thành công!” - Sản phẩm biến mất khỏi danh sách
Trường hợp đặc biệt: - Thử xóa sản phẩm đã có trong hóa đơn: Kiểm tra xem hệ thống có cảnh báo không cho phép xóa hoặc xử lý hợp lý - Thử xóa khi không chọn sản phẩm nào: Hiển thị thông báo “Vui lòng chọn một sản phẩm để xóa.”
4. Tải lại danh sách sản phẩm
Kịch bản: Tải lại danh sách sản phẩm từ database.
Bước thực hiện: 1. Mở ứng dụng và chuyển đến tab “Quản lý Sản phẩm” 2. Nhấn nút “Tải lại”
Kết quả mong đợi: - Danh sách sản phẩm được cập nhật từ database - Nếu có thay đổi từ nguồn khác (ví dụ: người dùng khác), những thay đổi đó sẽ được hiển thị
Trường hợp đặc biệt: - Database không khả dụng: Hiển thị thông báo lỗi phù hợp - Không có sản phẩm nào: Hiển thị danh sách trống
5. Tìm kiếm sản phẩm
Kịch bản: Tìm kiếm sản phẩm theo các tiêu chí khác nhau.
Bước thực hiện: 1. Mở ứng dụng và chuyển đến tab “Quản lý Sản phẩm” 2. Sử dụng chức năng tìm kiếm với các tiêu chí khác nhau: - Tìm theo mã sản phẩm - Tìm theo tên sản phẩm - Tìm theo danh mục
Kết quả mong đợi: - Hiển thị các sản phẩm phù hợp với tiêu chí tìm kiếm - Không tìm thấy kết quả: Hiển thị thông báo phù hợp hoặc danh sách trống
Các kịch bản kiểm thử này giúp đảm bảo các chức năng quản lý sản phẩm hoạt động chính xác và xử lý đúng đắn các trường hợp đặc biệt.
6.2 Testing Invoice Management Features
Việc kiểm thử các chức năng quản lý hóa đơn là rất quan trọng để đảm bảo hệ thống có thể tạo, lưu trữ và quản lý hóa đơn một cách chính xác. Dưới đây là các kịch bản kiểm thử chi tiết:
🧾 Suggested image: Screenshot of invoice detail window - showing the comprehensive invoice information including customer details, item list, quantities, prices, and total amount.
1. Tạo hóa đơn mới
Kịch bản: Tạo một hóa đơn mới với thông tin khách hàng và các sản phẩm.
Bước thực hiện: 1. Mở ứng dụng và chuyển đến tab “Quản lý Hóa đơn” 2. Nhấn nút “Tạo hóa đơn” 3. Nhập thông tin khách hàng: - Tên khách hàng: “Nguyễn Văn A” 4. Thêm sản phẩm vào hóa đơn: - Chọn sản phẩm “LAPTOP01 - Laptop Dell XPS 15” từ dropdown - Nhập số lượng: 2 - Nhấn nút “Thêm” 5. Thêm sản phẩm khác (nếu cần) 6. Nhấn nút “Tạo hóa đơn” để lưu
Kết quả mong đợi: - Hiển thị thông báo thành công: “Đã tạo thành công hóa đơn #X cho khách hàng ‘Nguyễn Văn A’.” - Hóa đơn mới xuất hiện trong danh sách hóa đơn với thông tin chính xác - Tổng tiền được tính đúng: 2 * 30000000 = 60000000
Kiểm tra validation: - Tên khách hàng để trống: Hiển thị lỗi “Vui lòng nhập tên khách hàng.” - Không thêm sản phẩm nào: Hiển thị lỗi “Hóa đơn phải có ít nhất một mặt hàng.” - Số lượng không hợp lệ (ví dụ: “abc”): Hiển thị lỗi “Số lượng phải là số nguyên.” - Số lượng âm hoặc 0: Hiển thị lỗi “Số lượng phải lớn hơn 0.”
2. Xem chi tiết hóa đơn
Kịch bản: Xem thông tin chi tiết của một hóa đơn.
Bước thực hiện: 1. Mở ứng dụng và chuyển đến tab “Quản lý Hóa đơn” 2. Chọn một hóa đơn từ danh sách 3. Nhấn nút “Xem chi tiết”
Kết quả mong đợi: - Hiển thị cửa sổ chi tiết hóa đơn với thông tin: - Mã hóa đơn - Ngày lập hóa đơn - Tên khách hàng - Danh sách các mặt hàng: mã sản phẩm, tên, số lượng, đơn giá, thành tiền - Tổng tiền hóa đơn
Trường hợp đặc biệt: - Thử xem chi tiết khi không chọn hóa đơn nào: Hiển thị thông báo “Vui lòng chọn một hóa đơn để xem chi tiết.” - Xem chi tiết hóa đơn có sản phẩm đã bị xóa: Hiển thị “[Sản phẩm không tồn tại]” hoặc xử lý phù hợp
3. Xóa hóa đơn
Kịch bản: Xóa một hóa đơn khỏi hệ thống.
Bước thực hiện: 1. Mở ứng dụng và chuyển đến tab “Quản lý Hóa đơn” 2. Chọn một hóa đơn từ danh sách 3. Nhấn nút “Xóa hóa đơn” 4. Xác nhận xóa hóa đơn khi hộp thoại hiện lên
Kết quả mong đợi: - Hiển thị thông báo xác nhận với thông tin chi tiết về hóa đơn - Sau khi xác nhận, hiển thị thông báo thành công: “Đã xóa thành công hóa đơn #X của khách hàng ‘Nguyễn Văn A’.” - Hóa đơn biến mất khỏi danh sách - Kiểm tra database để đảm bảo cả hóa đơn và các mục chi tiết đều đã bị xóa
Trường hợp đặc biệt: - Thử xóa khi không chọn hóa đơn nào: Hiển thị thông báo “Vui lòng chọn một hóa đơn để xóa.”
4. Tải lại danh sách hóa đơn
Kịch bản: Tải lại danh sách hóa đơn từ database.
Bước thực hiện: 1. Mở ứng dụng và chuyển đến tab “Quản lý Hóa đơn” 2. Nhấn nút “Tải lại”
Kết quả mong đợi: - Danh sách hóa đơn được cập nhật từ database - Nếu có thay đổi từ nguồn khác, những thay đổi đó sẽ được hiển thị
Trường hợp đặc biệt: - Database không khả dụng: Hiển thị thông báo lỗi phù hợp - Không có hóa đơn nào: Hiển thị danh sách trống
5. Thống kê doanh thu
Kịch bản: Xem thống kê doanh thu theo các tiêu chí khác nhau.
Bước thực hiện: 1. Mở ứng dụng và chuyển đến tab “Thống kê” 2. Chọn tab con “Doanh thu” 3. Nhấn nút “Doanh thu theo sản phẩm” hoặc “Doanh thu theo thời gian”
Kết quả mong đợi: - Hiển thị báo cáo thống kê với thông tin chính xác - Doanh thu theo sản phẩm: Hiển thị danh sách sản phẩm với doanh thu, số lượng bán và tỷ lệ phần trăm - Doanh thu theo thời gian: Hiển thị doanh thu theo ngày với tỷ lệ phần trăm
Trường hợp đặc biệt: - Không có dữ liệu hóa đơn: Hiển thị thông báo “Không có dữ liệu hóa đơn để thống kê!”
6. Thống kê sản phẩm và khách hàng
Kịch bản: Xem thống kê về sản phẩm bán chạy và khách hàng tiềm năng.
Bước thực hiện: 1. Mở ứng dụng và chuyển đến tab “Thống kê” 2. Chọn tab con “Sản phẩm” hoặc “Khách hàng” 3. Nhấn các nút chức năng tương ứng: - “Sản phẩm bán chạy nhất” - “Phân loại sản phẩm” - “Khách hàng thân thiết”
Kết quả mong đợi: - Hiển thị báo cáo thống kê với thông tin chính xác - Sản phẩm bán chạy: Hiển thị danh sách sản phẩm theo số lượng bán giảm dần - Phân loại sản phẩm: Hiển thị số lượng sản phẩm theo từng danh mục - Khách hàng thân thiết: Hiển thị danh sách khách hàng theo tổng chi tiêu giảm dần
Trường hợp đặc biệt: - Không có dữ liệu: Hiển thị thông báo phù hợp
Các kịch bản kiểm thử này giúp đảm bảo các chức năng quản lý hóa đơn và thống kê hoạt động chính xác và xử lý đúng đắn các trường hợp đặc biệt.
