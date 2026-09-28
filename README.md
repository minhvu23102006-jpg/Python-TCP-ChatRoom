# 🌐 Bài Tập Mạng Máy Tính - Ứng dụng Chat Room (Socket TCP)

Dự án này là một hệ thống phòng chat (Chat Room) cơ bản sử dụng kiến trúc Client-Server thông qua giao thức **TCP Socket** và kỹ thuật **Đa luồng (Threading)** trong Python.

Repository này bao gồm 2 phiên bản triển khai:
1. **Phiên bản Terminal (.py):** Do sinh viên tự xây dựng để chạy thực chiến trên Command Line/Terminal.
2. **Phiên bản Jupyter Notebook (.ipynb):** Base code tham khảo của giảng viên (00_Server, 01_Client_A, 02_Client_B).

---

## Phân công và thành viên
1. Trần Yến Nhi - 2410750: làm server   
2. Trần Ngọc Hải - 2410424: làm client A
3. Trương Minh Vũ - 2411082: làm client B

## Hướng dẫn sử dụng (Phiên bản Terminal)

1. Mở Terminal đầu tiên và khởi động máy chủ:
   `ash
   python server.py
   `
2. Mở các Terminal tiếp theo để khởi động máy khách:
   `ash
   python client.py
   `
3. Nhập IP của Server (hoặc 127.0.0.1 nếu chạy thử trên cùng 1 máy) và bắt đầu chat!

---

## 🔍 So sánh kiến trúc: Phiên bản Terminal (.py) vs Phiên bản Notebook (.ipynb)

Mặc dù cả hai phiên bản đều sử dụng chung một lõi logic (TCP Socket + Threading), cách thiết kế chi tiết lại có sự khác biệt nhằm phục vụ môi trường chạy khác nhau:

### 1. Cơ chế Đọc/Gửi dữ liệu
* **Bản Terminal:** Sử dụng lệnh 
ecv(1024) và send() cơ bản để truyền nhận chuỗi Byte thô. Ưu điểm là vô cùng tối giản, dễ hiểu cho người mới học.
* **Bản Notebook:** Bọc Socket lại thành một đối tượng file ảo bằng lệnh conn.makefile('rb') và dùng 
eadline(). Cách này ép tin nhắn phải kết thúc bằng ký tự xuống dòng \n và giới hạn cứng dung lượng (4096 bytes) để chống nghẽn mạng (Buffer Overflow).

### 2. Cách hiển thị tin nhắn ở Client
* **Bản Terminal:** Nhờ chạy trên màn hình console (đen trắng), mỗi khi luồng phụ nhận được tin, nó lập tức in thẳng ra màn hình bằng lệnh print().
* **Bản Notebook:** Vì Jupyter Notebook không hỗ trợ in bất đồng bộ tốt (dễ gây lỗi giao diện), luồng nhận tin sẽ âm thầm nhét tin nhắn vào một Hàng đợi (queue.Queue()). Người dùng phải tự chạy ô code 
ead_messages() để lấy tin từ hộp thư ra xem.

### 3. Vấn đề Tranh chấp luồng (Race Condition)
* **Bản Terminal:** Sử dụng một mảng clients = [] cơ bản. Nhược điểm nhỏ là nếu nhiều người cùng gửi tin ở mức một phần nghìn giây, Server có thể bị lỗi đè dữ liệu.
* **Bản Notebook:** Rất chặt chẽ. Sử dụng 	hreading.Lock() (Khóa an toàn). Khi Server chuẩn bị gửi tin cho một Client, nó sẽ khóa kênh đó lại, gửi xong mới mở khóa. Đảm bảo dữ liệu trơn tru hoàn toàn khi có hàng chục người chat cùng lúc.

### 4. Quy trình Đóng kết nối
* **Bản Terminal:** Dừng bằng cách ngắt Terminal trực tiếp (Ctrl+C). 
* **Bản Notebook:** Xử lý ''hạ cánh mềm''. Dùng cờ hiệu 	hreading.Event() để báo các luồng ngưng hoạt động, và dùng socket.shutdown(socket.SHUT_RDWR) để thông báo lịch sự tới đối phương trước khi chính thức ngắt kết nối close().

---
*Ghi chú: Phiên bản Terminal được tối ưu để dễ đọc, dễ hiểu bản chất hệ thống mạng, trong khi bản Notebook là bộ khung an toàn, chặt chẽ chuẩn mực cho các ứng dụng lớn hơn.*
