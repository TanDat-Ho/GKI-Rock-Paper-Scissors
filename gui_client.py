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
        