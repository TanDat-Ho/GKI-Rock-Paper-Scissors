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
        