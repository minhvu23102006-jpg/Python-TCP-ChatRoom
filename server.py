import socket
import threading

# MẢNG LƯU TRỮ: Giống như một cuốn danh bạ, lưu lại 'số điện thoại' (socket) của từng khách đang kết nối
clients = []

def handle_client(client_socket, client_address):
    # LUỒNG PHỤ (NHÂN VIÊN CHĂM SÓC KHÁCH HÀNG):
    # Hàm này giống như một nhân viên. Mỗi khi có khách mới, Server sẽ gọi một nhân viên ra để chăm riêng khách đó.
    print(f"[+] Người mới tham gia từ {client_address}")
    
    while True:
        try:
            # .recv(1024): Đứng chờ nhận dữ liệu từ khách. 1024 là số byte tối đa nhận 1 lần.
            # LƯU Ý: Lệnh này sẽ làm code TẠM DỪNG (Block) ở đây cho tới khi khách gửi tin nhắn.
            data = client_socket.recv(1024)
            
            # Nếu data rỗng nghĩa là khách đã ngắt kết nối (bấm X hoặc mạng đứt)
            if not data:
                break
            
            # VÒNG LẶP BROADCAST (PHÁT SÓNG): 
            # Lấy tin nhắn vừa nhận được, đem gửi cho TẤT CẢ những người khác trong danh bạ
            for c in clients:
                if c != client_socket: # Bỏ qua người vừa gửi (không gửi lại tiếng vọng cho chính họ)
                    try:
                        c.send(data) # .send() dùng để đẩy dữ liệu qua mạng
                    except:
                        pass
        except:
            # Nếu có lỗi mạng (đứt mạng, khách đóng đột ngột), thoát vòng lặp
            break
            
    # Xử lý sau khi khách thoát: Xóa khỏi danh bạ và đóng kết nối
    print(f"[-] {client_address} đã thoát.")
    if client_socket in clients:
        clients.remove(client_socket)
    client_socket.close()

def start_server():
    # BƯỚC 1: TẠO SOCKET (Tạo một cái Điện Thoại / Thiết bị mạng)
    # AF_INET: Dùng địa chỉ IP (IPv4)
    # SOCK_STREAM: Dùng giao thức TCP (đảm bảo gửi tin không bị thất lạc, đến đúng thứ tự)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # BƯỚC 2: BIND (Gắn cái Điện Thoại đó vào một số cố định / Cánh cửa của máy tính)
    # '0.0.0.0' là mở tất cả các mặt IP, 5000 là số cổng (Port)
    server_socket.bind(('0.0.0.0', 5000))
    
    # BƯỚC 3: LISTEN (Chuyển thiết bị sang chế độ 'nghe ngóng' chờ cuộc gọi tới)
    # 5: Cho phép tối đa 5 người xếp hàng đợi ngoài cửa nếu Server đang bận chưa kịp ra mở
    server_socket.listen(5)
    
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    print("=== MÁY CHỦ ĐANG CHẠY ===")
    print(f"IP Server: {local_ip} | Port: 5000")
    print("Đang mở cửa chờ khách...")
    
    # BƯỚC 4: VÒNG LẶP CHÍNH CỦA SERVER (Đứng ở cửa đón khách)
    while True:
        # .accept(): Đứng chờ khách gõ cửa. Code sẽ bị TẠM DỪNG (Block) ở đây cho tới khi có người kết nối.
        # Nó trả về 1 cái 'đường ống' (client_socket) để chat riêng với người đó, và địa chỉ của họ (client_address)
        client_socket, client_address = server_socket.accept()
        
        # Có khách tới -> Lưu khách vào danh bạ
        clients.append(client_socket)
        
        # BƯỚC 5: ĐA LUỒNG (THREADING) - Yếu tố cốt lõi của Chat Room
        # Nếu không có đa luồng: Server tự đứng chat với khách này, mấy khách đến sau sẽ bị chặn đứng ngoài cửa.
        # Khi có đa luồng: Server đẻ ra một 'luồng' mới (gọi hàm handle_client) và giao khách này cho luồng đó.
        # Sau đó Server (luồng chính) lại quay lên đầu vòng lặp While, tiếp tục chờ đón khách tiếp theo.
        thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        thread.start()

if __name__ == '__main__':
    start_server()
