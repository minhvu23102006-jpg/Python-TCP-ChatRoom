import socket
import threading

def receive_messages(sock):
    # LUỒNG PHỤ: Hàm này chạy song song ngầm, chỉ làm 1 việc duy nhất là CHỜ NHẬN TIN NHẮN
    while True:
        try:
            # Chờ dữ liệu từ Server gửi về. Vì tin nhắn truyền đi ở dạng Byte nên phải .decode() để thành chữ
            # Lệnh .recv() cũng làm luồng phụ này bị TẠM DỪNG cho tới khi có tin nhắn tới.
            data = sock.recv(1024).decode('utf-8')
            if not data:
                break
                
            # In tin nhắn ra màn hình (\r để ghi đè dòng chữ 'Bạn: ' đang gõ dở cho giao diện đỡ lộn xộn)
            print(f"\r{data}\nBạn: ", end="")
        except:
            print("\nĐã mất kết nối tới Server!")
            sock.close()
            break

def start_client():
    # BƯỚC 1: TẠO SOCKET (Giống Server, tạo một thiết bị mạng TCP)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    MY_NAME = 'Client A' 
    
    print(f"=== PHẦN MỀM CHAT ({MY_NAME}) ===")
    server_ip = input("Nhập IP Server (127.0.0.1 nếu chạy chung 1 máy): ")
    
    try:
        # BƯỚC 2: CONNECT (Chủ động gọi điện thoại đến Server)
        # Cần đúng số IP của Server và đúng Cổng (Port 5000)
        client_socket.connect((server_ip, 5000))
        print("Đã kết nối! Bắt đầu chat.")
        
        # BƯỚC 3: ĐA LUỒNG CHO CLIENT
        # Tại sao Client cũng cần đa luồng?
        # Máy tính không thể đồng thời vừa CHỜ bạn gõ phím (input), vừa CHỜ Server gửi tin tới (recv) trên cùng 1 luồng.
        # Do đó, ta sinh ra 1 luồng phụ để làm nhiệm vụ 'Lắng nghe tin nhắn' (gọi hàm receive_messages).
        recv_thread = threading.Thread(target=receive_messages, args=(client_socket,))
        recv_thread.start()
        
        # LUỒNG CHÍNH: Kể từ đây, luồng chính chỉ làm nhiệm vụ CHỜ GÕ PHÍM và GỬI ĐI
        while True:
            # Lệnh input() sẽ TẠM DỪNG luồng chính cho đến khi bạn gõ xong và bấm Enter
            message = input("Bạn: ")
            
            if message.lower() == 'exit':
                break
                
            if message.strip():
                # Ghép tên và tin nhắn
                full_message = f"{MY_NAME}: {message}"
                
                # BƯỚC 4: SEND (Biến chữ thành dạng Byte bằng .encode() rồi đẩy vào đường ống mạng để gửi đi)
                client_socket.send(full_message.encode('utf-8'))
                
    except Exception as e:
        print(f"Không thể kết nối. Lỗi: {e}")
        
    # Đóng kết nối khi kết thúc
    client_socket.close()

if __name__ == '__main__':
    start_client()
