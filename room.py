import threading

class Room:
    def __init__(self, room_id, room_name="Room", creator_name="Unknown"):
        self.room_id = room_id
        self.room_name = room_name
        self.creator_name = creator_name
        self.players = {}  # {1: conn1, 2: conn2}
        self.player_names = {}  # {1: name1, 2: name2}
        self.choices = {}
        self.scores = {1: 0, 2: 0}
        self.round = 1
        self.total_rounds = None  # Sẽ được set khi người chơi đầu tiên chọn
        self.lock = threading.Lock()
        self.waiting_for_rounds = True  # Đợi người chơi đầu tiên chọn số vòng
        self.game_in_progress = False  # Đánh dấu game đang diễn ra
        self.active_players = set()  # Theo dõi players còn kết nối

    def is_waiting(self):
        return len(self.players) == 1 and not self.game_in_progress

    def is_full(self):
        return len(self.players) == 2
    
    def get_room_info(self):
        """Trả về thông tin phòng để hiển thị trong danh sách"""
        return {
            "id": self.room_id,
            "name": self.room_name,
            "creator": self.creator_name,
            "players": len(self.players),
            "max_players": 2,
            "rounds": self.total_rounds if self.total_rounds else "TBD",
            "status": "In Game" if self.game_in_progress else "Waiting"
        }

    def add_player(self, conn, name="Unknown"):
        player_id = 1 if 1 not in self.players else 2
        self.players[player_id] = conn
        self.player_names[player_id] = name
        self.active_players.add(player_id)
        return player_id

    def get_player_name(self, player_id):
        return self.player_names.get(player_id, f"Player {player_id}")

    def remove_player(self, player_id):
        """Remove player khi disconnect"""
        if player_id in self.players:
            try:
                self.players[player_id].close()
            except:
                pass
            del self.players[player_id]
        if player_id in self.player_names:
            del self.player_names[player_id]
        self.active_players.discard(player_id)
        print(f"[Room {self.room_id}] {self.get_player_name(player_id)} disconnected")
