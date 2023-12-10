import tkinter as tk
import customtkinter as ctk
from datetime import timedelta
from CTkMenuBar import *
from TicTacToe.timer import Timer
from PIL import Image, ImageTk
from TicTacToe.CTkGif import CTkGif
import os
from TicTacToe.ai import AI
import threading
import time
import playsound
class TicTacToeGame:
    def __init__(self, root):
        self.game_active = True
        self.root = root
        self.set_variables()
        self.setup_ui()
        self.timer = Timer()
        self.update_time()

    #Setting variables
    def set_variables(self):
        self.root.title("Tic-Tac-Toe")
        self.root.geometry("650x650")
        self.root.minsize(650, 650)
        self.root.iconbitmap(os.path.abspath("img\icon_ttc.ico"))
        self.x_countn = 0
        self.c_countn = 0
        self.blocks_click = [[False, ""] for _ in range(9)]
        self.round = 0
        self.turn = "c"
        self.blocks = []
        self.stop_start = timedelta(seconds=0)
        self.IMAGE_PATH = os.path.abspath(r"img/chatgpt_logo.gif")
        self.AUDIO_PATH = os.path.abspath(r"audio/barka.mp3")
        self.ai_mode = False
        self.ai = AI()
    #Setting up interface
    def setup_ui(self):
        self.create_title_menu()
        self.label_ai = CTkGif(master=self.root, path=self.IMAGE_PATH)
        self.app_frame = ctk.CTkFrame(master=self.root, fg_color="#8A2BE2")
        self.app_frame.place(relx=0.5, rely=0.5, relwidth=0.8, relheight=0.8, anchor="center")
        self.reset_button = ctk.CTkButton(master=self.root, fg_color="#B65FCF", anchor="center", text="Start again", command=self.new_gamebtn)
        self.reset_button.place(relx=0.5, anchor="center", rely=0.95, relwidth=0.20)
        self.turn_label = ctk.CTkLabel(master=self.root, text=f"Turn: {'❌' if self.turn == 'x' else None}   Round: {self.round}   Time: 00:00", font=("Arial", 20))
        self.turn_label.place(relwidth=1, relheight=0.1, rely=0.0, relx=0)
        self.x_count = ctk.CTkLabel(master=self.root, text="0  ❌", anchor="center", font=("Arial", 28))
        self.x_count.place(relx = 0.30, rely=0.95, relheight=0.08, relwidth=0.15, anchor = "center")
        self.c_count = ctk.CTkLabel(master=self.root, text="⚪  0", anchor="center", font=("Arial", 28))
        self.c_count.place(relx = 0.70, rely=0.95, relheight=0.08, relwidth=0.15, anchor = "center")
        self.create_squares()
    
    #Creating menu
    def create_title_menu(self):
        self.menubar = CTkTitleMenu(master=self.root)
        button1 = self.menubar.add_cascade("Game")
        button2 = self.menubar.add_cascade("Settings")
        button3 = self.menubar.add_cascade("About")
        button4 = self.menubar.add_cascade("Display")
        self.customdrop1 = CustomDropdownMenu(widget=button1)
        self.customdrop1.add_option("New", self.new_gamebtn)
        self.customdrop1.add_option("Exit", self.exit_gamebtn)
        self.customdrop1.add_option("2137", self.barka_btn)
        self.customdrop2 = CustomDropdownMenu(widget=button2)
        self.customdrop2.add_option("Custom")
        #self.customdrop2.add_option("AI", self.ai_modebtn)
        self.submenu = self.customdrop2.add_submenu("AI")
        self.submenu.add_option("Key", self.button_click_event)
        self.submenu.add_option("On/Off", self.ai_modebtn)
        self.customdrop3 = CustomDropdownMenu(widget=button3)
        self.customdrop3.add_option("Author")
        self.customdrop4 = CustomDropdownMenu(widget=button4)
        self.customdrop4.add_option("Reset score", self.reset_scorebtn)
        self.customdrop4.add_option("Reset timer", self.reset_timerbtn)

    def new_gamebtn(self):
        if not self.game_active:
            self.reset_game()
            return
        self.round = 0
        self.turn = "c"
        self.blocks_click = [[False, ""] for _ in range(9)]
        for block in self.blocks:
            block.configure(text="✎", state="normal")

    def barka_btn(self):
        barka = threading.Thread(target=lambda: playsound.playsound(self.AUDIO_PATH))
        barka.start()

    #Exit game
    def exit_gamebtn(self):
        quit()

    def reset_timerbtn(self):
        self.timer.reset()

    def reset_scorebtn(self):
        self.c_countn = 0
        self.x_countn = 0
        if not self.game_active:
            self.c_count.configure(text=f"⚪  {self.c_countn}")
            self.x_count.configure(text=f"{self.x_countn}  ❌")

    def ai_modebtn(self):
        if self.ai_mode:
            self.ai_mode_off()
            return
        self.label_ai.place(relx = 0.05, rely = 0.95, anchor="center", relwidth=0.2, relheight=0.2)
        self.label_ai.start()
        self.reset_timerbtn()
        self.reset_scorebtn()
        self.new_gamebtn()
        self.ai_mode_start()

    def button_click_event(self):
        dialog = ctk.CTkInputDialog(text="Type your chatgpt api key: ", title="API KEY")
        self.path = dialog.get_input()
        self.ai.api_key = self.path

    def ai_mode_start(self):
        self.ai_mode = True

    def ai_turn(self):
        if not self.game_active:
            return
        time.sleep(10)
        click_index = self.ai.process_response(side="x", positions=self.blocks_click, hard_level = 1)
        self.blocks_click[click_index-1] = [True, "x"]
        self.blocks[click_index-1].configure(text="❌", state="disabled")
        self.turn = 'c'
        self.round += 1
        self.check_win(True)
 
    def ai_mode_off(self):
        self.label_ai.stop()
        self.label_ai.place_forget()
        self.ai_mode = False
        self.reset_timerbtn()
        self.reset_scorebtn()
        self.new_gamebtn()

    #Definning and placing blocks
    def create_squares(self):
        for row in range(3):
            for col in range(3):
                block = ctk.CTkButton(master=self.app_frame, fg_color="#4B0082", text="✎", font=("Arial", 24))
                self.blocks.append(block)

        for i in range(len(self.blocks)):
            block = self.blocks[i]  # capture the current button
            block.configure(command=lambda el=block, id=i: self.on_click(None, el, id))
            block.bind("<Leave>", lambda event, el=block, id=i: self.on_leave(event, el, id))
            block.bind("<Enter>", lambda event, el=block, id=i: self.on_hover(event, el, id))

        self.blocks[0].grid(column=0, row=0, padx=(10,0), pady=(10,0), sticky="nsew")
        self.blocks[1].grid(column=1, row=0, padx=(10,0), pady=(10,0), sticky="nsew")
        self.blocks[2].grid(column=2, row=0, padx=(10,10), pady=(10,0), sticky="nsew")
        self.blocks[3].grid(column=0, row=1, padx=(10,0), pady=(10,0), sticky="nsew")
        self.blocks[4].grid(column=1, row=1, padx=(10,0), pady=(10,0), sticky="nsew")
        self.blocks[5].grid(column=2, row=1, padx=(10,10), pady=(10,0), sticky="nsew")
        self.blocks[6].grid(column=0, row=2, padx=(10,0), pady=10, sticky="nsew")
        self.blocks[7].grid(column=1, row=2, padx=(10,0), pady=10,sticky="nsew")
        self.blocks[8].grid(column=2, row=2, padx=(10,10), pady=10, sticky="nsew")

        for i in range(3):
            self.app_frame.rowconfigure(i, weight=1)
            self.app_frame.columnconfigure(i, weight=1)

    #Setting up on hover function
    def on_hover(self, event, el, id):
        if not self.game_active:
            return
        elif self.turn == 'x' and self.ai_mode:
            return
        if self.blocks_click[id][0]:
            pass
        elif self.turn == "x":
            el.configure(text="❌")
        elif self.turn == "c":
            el.configure(text="⚪")

    #Setting up on leave function
    def on_leave(self, event, el, id):
        if self.blocks_click[id][0]:
            pass
        else:
            el.configure(text="✎")
    #Getting time for update
    def get_time(self):
        elapsed_time = self.timer.get_seconds()
        minutes, seconds = divmod(elapsed_time.seconds, 60)
        return f"{minutes:02}:{seconds:02}"
    
    #Updating results
    def update_time(self):
        self.turn_label.configure(text=f"Turn: {'❌' if self.turn == 'x' else '⚪'}   Round: {'End' if self.round == 9 else self.round}   Time: {self.get_time()}")
        self.c_count.configure(text=f"⚪  {self.c_countn}")
        self.x_count.configure(text=f"{self.x_countn}  ❌")

        if self.game_active:
            self.root.after(1000, self.update_time)
        else:
            self.turn_label.configure(text=f"Turn: {'Win ❌' if self.character == 'x' else 'Win ⚪'}   Round: {self.round if self.game_active else 'End'}   Time: {self.get_time()}")
    
    #Setting up on click function
    def on_click(self, event, el, id):
        if not self.game_active:
            return
        elif self.turn == 'x' and self.ai_mode:
            return
        self.round += 1
        self.blocks_click[id][1] = self.turn

        match self.turn:
            case 'x':
                self.turn = 'c'
                el.configure(text="❌")
            case 'c':
                self.turn = 'x'
                el.configure(text="⚪")

        self.blocks_click[id][0] = True
        el.configure(state="disabled")
        self.check_win()

    #Checking if someone win
    def check_win(self, after_ai = False):
        # Check rows
        for i in range(0, 9, 3):
            if self.blocks_click[0 + i][1] == "x" and self.blocks_click[1 + i][1] == "x" and self.blocks_click[2 + i][1] == "x":
                self.if_win("x")
            if self.blocks_click[0 + i][1] == "c" and self.blocks_click[1 + i][1] == "c" and self.blocks_click[2 + i][1] == "c":
                self.if_win("c")

        # Check columns
        for i in range(3):
            if self.blocks_click[0 + i][1] == "x" and self.blocks_click[3 + i][1] == "x" and self.blocks_click[6 + i][1] == "x":
                self.if_win("x")
            if self.blocks_click[0 + i][1] == "c" and self.blocks_click[3 + i][1] == "c" and self.blocks_click[6 + i][1] == "c":
                self.if_win("c")

        # Check diagonals
        if self.blocks_click[0][1] == "x" and self.blocks_click[4][1] == "x" and self.blocks_click[8][1] == "x":
            self.if_win("x")
        if self.blocks_click[0][1] == "c" and self.blocks_click[4][1] == "c" and self.blocks_click[8][1] == "c":
            self.if_win("c")

        if self.blocks_click[2][1] == "x" and self.blocks_click[4][1] == "x" and self.blocks_click[6][1] == "x":
            self.if_win("x")

        if self.blocks_click[2][1] == "c" and self.blocks_click[4][1] == "c" and self.blocks_click[6][1] == "c":
            self.if_win("c")

        if self.ai_mode and self.turn == "x" and not after_ai:
            ai = threading.Thread(target=self.ai_turn)
            ai.start()

    #Reseting game
    def reset_game(self):
        self.timer.start_timer()
        self.round = 0
        self.turn = "c"
        self.blocks_click = [[False, ""] for _ in range(9)]
        for block in self.blocks:
            block.configure(text="✎", state="normal")
        self.game_active = True
        self.update_time()

    #Pausing game
    def pause_game(self):
        self.timer.stop_timer()
        self.game_active = False

    #When someone win
    def if_win(self, character):
        self.character = character
        match character:
            case "c":
                self.c_countn += 1
            case "x":
                self.x_countn += 1
        self.pause_game()
        self.update_time()


