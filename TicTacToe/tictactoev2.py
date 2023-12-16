import customtkinter as ctk
from datetime import timedelta
from CTkMenuBar import *
from TicTacToe.timer import Timer
from TicTacToe.ai import AI
import threading
import time
import playsound
from TicTacToe.elements import AppFrame, MenuTTT, LabelAI, ResetButton, TurnLabel, XCount, CCount
from TicTacToe.constants import Constants
class TicTacToeGame(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.const = Constants()
        self.game_active = True
        self.set_variables()
        self.setup_ui()
        self.timer = Timer()
        self.update_time()
        self.mainloop()

    #Setting variables
    def set_variables(self):
        self.title("Tic-Tac-Toe")
        self.geometry("650x650")
        self.minsize(650, 650)
        self.iconbitmap(self.const.ICON_PATH)
        self.x_countn = 0
        self.c_countn = 0
        self.blocks_click = [[False, ""] for _ in range(9)]
        self.round = 0
        self.turn = "c"
        self.blocks = []
        self.stop_start = timedelta(seconds=0)
        self.ai_mode = False
        self.ai = AI()
    #Setting up interface
    def setup_ui(self):
        self.create_title_menu()
        self.label_ai = LabelAI(self, self.const.IMAGE_PATH)
        self.app_frame = AppFrame(self)
        self.reset_button = ResetButton(self)
        self.turn_label = TurnLabel(self)
        self.x_count = XCount(self)
        self.c_count = CCount(self)
    
    #Creating menu
    def create_title_menu(self):
        self.menubar = MenuTTT(self)

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
        barka = threading.Thread(target=lambda: playsound.playsound(self.const.AUDIO_PATH))
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
    
    #Updating results
    def update_time(self):
        self.turn_label.configure(text=f"Turn: {'❌' if self.turn == 'x' else '⚪'}   Round: {'End' if self.round == 9 else self.round}   Time: {self.timer.get_time()}")
        self.c_count.configure(text=f"⚪  {self.c_countn}")
        self.x_count.configure(text=f"{self.x_countn}  ❌")

        if self.game_active:
            self.after(1000, self.update_time)
        else:
            self.turn_label.configure(text=f"Turn: {'Win ❌' if self.character == 'x' else 'Win ⚪'}   Round: {self.round if self.game_active else 'End'}   Time: {self.timer.get_time()}")
    
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


