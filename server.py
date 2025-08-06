import socket
import threading

# Để cho phép tất cả máy kết nối, sử dụng '0.0.0.0'
# Hoặc sử dụng IP cụ thể của máy này nếu bạn biết
HOST = 'localhost'  # Sử dụng localhost để test
PORT = 65433  # Thay đổi port để tránh xung đột

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Cho phép tái sử dụng port
server.bind((HOST, PORT))
server.listen()

rooms = []  # Danh sách các phòng hiện tại
room_id = 1
lock = threading.Lock()

def main():
    print("[*] Server started.")
    while True:
        conn, addr = server.accept()
        # TODO: Implement handle_client function
        print(f"[+] New connection from {addr}")
        conn.close()

if __name__ == "__main__":
    main()
