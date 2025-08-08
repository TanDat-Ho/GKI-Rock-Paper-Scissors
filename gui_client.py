import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import socket
import threading
import time

class RockPaperScissorsGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎮 Rock Paper Scissors Game")
        self.root.geometry("600x700")
        self.root.configure(bg='#2c3e50')
        
        # Game variables
        self.client = None
        self.connected = False
        self.player_id = None
        self.room_id = None
        
        # Setup GUI
        self.setup_gui()
        
    def setup_gui(self):
        # Main container
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(
            main_frame, 
            text="🎮 Rock Paper Scissors Online",
            font=('Arial', 24, 'bold'),
            fg='#ecf0f1',
            bg='#2c3e50'
        )
        title_label.pack(pady=(0, 20))
        
        # Connection frame
        self.setup_connection_frame(main_frame)
        
        # Game status frame
        self.setup_status_frame(main_frame)
        
        # Game controls frame
        self.setup_game_frame(main_frame)
        
        # Chat/Log frame
        self.setup_log_frame(main_frame)
        
    def setup_connection_frame(self, parent):
        conn_frame = tk.LabelFrame(
            parent,
            text="🌐 Connection",
            font=('Arial', 12, 'bold'),
            fg='#ecf0f1',
            bg='#34495e',
            bd=2
        )
        conn_frame.pack(fill=tk.X, pady=(0, 10))
        
            
        # Server input
        input_frame = tk.Frame(conn_frame, bg='#34495e')
        input_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(input_frame, text="Server:", font=('Arial', 10), fg='#ecf0f1', bg='#34495e').pack(side=tk.LEFT)
        self.host_entry = tk.Entry(input_frame, font=('Arial', 10))
        self.host_entry.insert(0, "172.20.10.4")
        self.host_entry.pack(side=tk.LEFT, padx=(5, 10))
        
        tk.Label(input_frame, text="Port:", font=('Arial', 10), fg='#ecf0f1', bg='#34495e').pack(side=tk.LEFT)
        self.port_entry = tk.Entry(input_frame, font=('Arial', 10), width=8)
        self.port_entry.insert(0, "65433")
        self.port_entry.pack(side=tk.LEFT, padx=(5, 10))
        
        # Connect button
        self.connect_btn = tk.Button(
            input_frame,
            text="🔌 Connect",
            font=('Arial', 10, 'bold'),
            bg='#27ae60',
            fg='white',
            command=self.connect_to_server,
            padx=20
        )
        self.connect_btn.pack(side=tk.RIGHT)
        
        # Player name input (initially hidden)
        self.name_frame = tk.Frame(conn_frame, bg='#34495e')
        
        tk.Label(
            self.name_frame, 
            text="Enter your name:", 
            font=('Arial', 10, 'bold'), 
            fg='#ecf0f1', 
            bg='#34495e'
        ).pack(pady=5)
        
        name_input_frame = tk.Frame(self.name_frame, bg='#34495e')
        name_input_frame.pack(pady=5)
        
        self.name_entry = tk.Entry(
            name_input_frame, 
            font=('Arial', 12), 
            width=20
        )
        self.name_entry.pack(side=tk.LEFT, padx=5)
        self.name_entry.bind('<Return>', lambda event: self.submit_name())
        
        self.submit_name_btn = tk.Button(
            name_input_frame,
            text="✅ Submit",
            font=('Arial', 10, 'bold'),
            bg='#3498db',
            fg='white',
            command=self.submit_name
        )
        self.submit_name_btn.pack(side=tk.LEFT, padx=5)
        
        # Room choice frame (initially hidden)
        self.room_choice_frame = tk.Frame(conn_frame, bg='#34495e')
        
        choice_label = tk.Label(
            self.room_choice_frame,
            text="What would you like to do?",
            font=('Arial', 12, 'bold'),
            fg='#ecf0f1',
            bg='#34495e'
        )
        choice_label.pack(pady=10)
        
        choice_buttons_frame = tk.Frame(self.room_choice_frame, bg='#34495e')
        choice_buttons_frame.pack(pady=5)
        
        self.create_room_btn = tk.Button(
            choice_buttons_frame,
            text="🏠 Create New Room",
            font=('Arial', 11, 'bold'),
            bg='#3498db',
            fg='white',
            width=18,
            command=lambda: self.send_choice('1')
        )
        self.create_room_btn.pack(side=tk.LEFT, padx=10)
        
        self.join_room_btn = tk.Button(
            choice_buttons_frame,
            text="🚪 Join Existing Room",
            font=('Arial', 11, 'bold'),
            bg='#9b59b6',
            fg='white',
            width=18,
            command=lambda: self.send_choice('2')
        )
        self.join_room_btn.pack(side=tk.LEFT, padx=10)
        def setup_status_frame(self, parent):
        status_frame = tk.LabelFrame(
            parent,
            text="📊 Game Status",
            font=('Arial', 12, 'bold'),
            fg='#ecf0f1',
            bg='#34495e',
            bd=2
        )
        status_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Status labels
        info_frame = tk.Frame(status_frame, bg='#34495e')
        info_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.status_label = tk.Label(
            info_frame,
            text="Status: Disconnected",
            font=('Arial', 11),
            fg='#e74c3c',
            bg='#34495e'
        )
        self.status_label.pack(anchor=tk.W)
        
        self.room_label = tk.Label(
            info_frame,
            text="Room: Not joined",
            font=('Arial', 11),
            fg='#ecf0f1',
            bg='#34495e'
        )
        self.room_label.pack(anchor=tk.W)
        
    def setup_game_frame(self, parent):
        game_frame = tk.LabelFrame(
            parent,
            text="🎯 Game Controls",
            font=('Arial', 12, 'bold'),
            fg='#ecf0f1',
            bg='#34495e',
            bd=2
        )
        game_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Rounds selection (initially hidden)
        self.rounds_frame = tk.Frame(game_frame, bg='#34495e')
        
        rounds_label = tk.Label(
            self.rounds_frame,
            text="Choose number of rounds:",
            font=('Arial', 11),
            fg='#ecf0f1',
            bg='#34495e'
        )
        rounds_label.pack(pady=5)
        
        rounds_options_frame = tk.Frame(self.rounds_frame, bg='#34495e')
        rounds_options_frame.pack(pady=5)
        
        self.rounds_var = tk.StringVar(value="3")
        for rounds in ["3", "5", "7", "9", "11"]:
            tk.Radiobutton(
                rounds_options_frame,
                text=f"{rounds} rounds",
                variable=self.rounds_var,
                value=rounds,
                font=('Arial', 10),
                fg='#ecf0f1',
                bg='#34495e',
                selectcolor='#2c3e50'
            ).pack(side=tk.LEFT, padx=5)
        
        self.submit_rounds_btn = tk.Button(
            self.rounds_frame,
            text="✅ Confirm Rounds",
            font=('Arial', 10, 'bold'),
            bg='#3498db',
            fg='white',
            command=self.submit_rounds
        )
        self.submit_rounds_btn.pack(pady=5)
        
        # Game moves (initially hidden)
        self.moves_frame = tk.Frame(game_frame, bg='#34495e')
        
        moves_label = tk.Label(
            self.moves_frame,
            text="Choose your move:",
            font=('Arial', 14, 'bold'),
            fg='#ecf0f1',
            bg='#34495e'
        )
        moves_label.pack(pady=10)
        
        # Move buttons with emojis
        moves_buttons_frame = tk.Frame(self.moves_frame, bg='#34495e')
        moves_buttons_frame.pack(pady=10)
        
        self.rock_btn = tk.Button(
            moves_buttons_frame,
            text="🪨\nRock",
            font=('Arial', 12, 'bold'),
            bg='#95a5a6',
            fg='white',
            width=8,
            height=3,
            command=lambda: self.make_move('rock')
        )
        self.rock_btn.pack(side=tk.LEFT, padx=10)
        
        self.paper_btn = tk.Button(
            moves_buttons_frame,
            text="📄\nPaper",
            font=('Arial', 12, 'bold'),
            bg='#f39c12',
            fg='white',
            width=8,
            height=3,
            command=lambda: self.make_move('paper')
        )
        self.paper_btn.pack(side=tk.LEFT, padx=10)
        
        self.scissors_btn = tk.Button(
            moves_buttons_frame,
            text="✂️\nScissors",
            font=('Arial', 12, 'bold'),
            bg='#e74c3c',
            fg='white',
            width=8,
            height=3,
            command=lambda: self.make_move('scissors')
        )
        self.scissors_btn.pack(side=tk.LEFT, padx=10)
        
        # Replay frame (initially hidden)
        self.replay_frame = tk.Frame(game_frame, bg='#34495e')
        
        replay_label = tk.Label(
            self.replay_frame,
            text="Do you want to play again?",
            font=('Arial', 12, 'bold'),
            fg='#ecf0f1',
            bg='#34495e'
        )
        replay_label.pack(pady=10)
        
        replay_buttons_frame = tk.Frame(self.replay_frame, bg='#34495e')
        replay_buttons_frame.pack(pady=5)
        
        self.yes_btn = tk.Button(
            replay_buttons_frame,
            text="✅ Yes",
            font=('Arial', 11, 'bold'),
            bg='#27ae60',
            fg='white',
            width=10,
            command=lambda: self.replay_response('yes')
        )
        self.yes_btn.pack(side=tk.LEFT, padx=10)
        
        self.no_btn = tk.Button(
            replay_buttons_frame,
            text="❌ No",
            font=('Arial', 11, 'bold'),
            bg='#e74c3c',
            fg='white',
            width=10,
            command=lambda: self.replay_response('no')
        )
        self.no_btn.pack(side=tk.LEFT, padx=10)
        
        # Initially hide all game frames
        self.hide_all_game_frames()
        self.name_frame.pack_forget()  # Hide name input initially
        self.room_choice_frame.pack_forget()  # Hide room choice initially
        self.room_name_frame.pack_forget()  # Hide room name input initially
        self.room_list_frame.pack_forget()  # Hide room list initially
        
    def setup_log_frame(self, parent):
        log_frame = tk.LabelFrame(
            parent,
            text="📝 Game Log",
            font=('Arial', 12, 'bold'),
            fg='#ecf0f1',
            bg='#34495e',
            bd=2
        )
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            height=12,
            font=('Consolas', 10),
            bg='#2c3e50',
            fg='#ecf0f1',
            insertbackground='#ecf0f1'
        )
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)