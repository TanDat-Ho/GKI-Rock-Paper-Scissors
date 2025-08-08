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

def handle_client(conn, addr):
    global room_id
    print(f"[+] New connection from {addr}")
    target_room = None
    player_id = None
    player_name = None

    try:
        # Yêu cầu nhập tên người chơi
        conn.sendall("🎮 Welcome to Rock Paper Scissors! 🎮\nPlease enter your name: ".encode())
        try:
            player_name = conn.recv(1024).decode().strip()
            if not player_name:
                player_name = f"Player_{addr[1]}"  # Sử dụng port làm tên mặc định
        except Exception as e:
            print(f"Error receiving player name from {addr}: {e}")
            player_name = f"Player_{addr[1]}"

        print(f"[+] Player '{player_name}' connected from {addr}")
        # TODO: Implement room creation and joining logic
        
    except Exception as e:
        print(f"Error handling client {addr}: {e}")
    finally:
        conn.close()

def cleanup_empty_rooms():
    """Dọn dẹp các phòng rỗng hoặc đã kết thúc"""
    global rooms
    with lock:
        active_rooms = []
        for room in rooms:
            should_keep = False
            
            # Giữ phòng nếu đang có game trong progress
            if room.game_in_progress and len(room.players) > 0:
                should_keep = True
            # Giữ phòng nếu có 1 player đang chờ (chưa trong game)
            elif len(room.players) == 1 and not room.game_in_progress:
                should_keep = True
            # Giữ phòng nếu có 2 players (dù chưa bắt đầu game)
            elif len(room.players) == 2:
                should_keep = True
            
            if should_keep:
                active_rooms.append(room)
            else:
                # Phòng thực sự rỗng hoặc đã kết thúc hoàn toàn
                print(f"[Cleanup] Removing empty room {room.room_id}")
                # Đóng tất cả connections còn lại trong phòng
                for pid, conn in list(room.players.items()):
                    try:
                        conn.close()
                    except:
                        pass
        
        rooms = active_rooms
        print(f"[Cleanup] Active rooms: {len(rooms)}")

def main():
    print("[*] Server started.")
    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    main()
