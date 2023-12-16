import customtkinter as ctk
from TicTacToe.CTkGif import CTkGif
import CTkMenuBar
class ButtonTTT(ctk.CTkButton):
    def __init__(self, parent, col:int, row:int) -> None:
        super().__init__(master=parent)
        self.configure(fg_color="#4B0082", text="✎", font=("Arial", 24))
        self.set_grid(col, row)
    def set_grid(self, col:int, row:int) -> None:
        match col:
            case 0:
                padx=(10,0)
            case 1:
                padx=(10,0)
            case 2:
                padx=(10,10)
        match row:
            case 0:
                pady=(10,0)
            case 1:
                pady=(10,0)
            case 2:
                pady=10
        self.grid(row=row, column=col, padx=padx, pady=pady, sticky="nsew")

class AppFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#8A2BE2")
        self.place(relx=0.5, rely=0.5, relwidth=0.8, relheight=0.8, anchor="center")
        for i in range(3):
            self.rowconfigure(i, weight=1)
            self.columnconfigure(i, weight=1)

        for row in range(3):
            for col in range(3):
                block = ButtonTTT(self, col, row)
                parent.blocks.append(block)

        for i in range(len(parent.blocks)):
            block = parent.blocks[i]
            block.configure(command=lambda el=block, id=i: parent.on_click(None, el, id))
            block.bind("<Leave>", lambda event, el=block, id=i: parent.on_leave(event, el, id))
            block.bind("<Enter>", lambda event, el=block, id=i: parent.on_hover(event, el, id))

class MenuTTT(CTkMenuBar.CTkTitleMenu):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        button1 = self.add_cascade("Game")
        button2 = self.add_cascade("Settings")
        button3 = self.add_cascade("About")
        button4 = self.add_cascade("Display")
        self.customdrop1 = CTkMenuBar.CustomDropdownMenu(widget=button1)
        self.customdrop1.add_option("New", parent.new_gamebtn)
        self.customdrop1.add_option("Exit", parent.exit_gamebtn)
        self.customdrop1.add_option("2137", parent.barka_btn)
        self.customdrop2 = CTkMenuBar.CustomDropdownMenu(widget=button2)
        self.customdrop2.add_option("Custom")
        self.submenu = self.customdrop2.add_submenu("AI")
        self.submenu.add_option("Key", parent.button_click_event)
        self.submenu.add_option("On/Off", parent.ai_modebtn)
        self.customdrop3 = CTkMenuBar.CustomDropdownMenu(widget=button3)
        self.customdrop3.add_option("Author")
        self.customdrop4 = CTkMenuBar.CustomDropdownMenu(widget=button4)
        self.customdrop4.add_option("Reset score", parent.reset_scorebtn)
        self.customdrop4.add_option("Reset timer", parent.reset_timerbtn)

class LabelAI(CTkGif):
    def __init__(self, parent, path):
        super().__init__(parent, path=path)

class ResetButton(ctk.CTkButton):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#B65FCF", anchor="center", text="Start again", command=parent.new_gamebtn)
        self.place(relx=0.5, anchor="center", rely=0.95, relwidth=0.20)

class TurnLabel(ctk.CTkLabel):
    def __init__(self, parent):
        super().__init__(parent, text=f"Turn: {'❌' if parent.turn == 'x' else None}   Round: {parent.round}   Time: 00:00", font=("Arial", 20))
        self.place(relwidth=1, relheight=0.1, rely=0.0, relx=0)

class XCount(ctk.CTkLabel):
    def __init__(self, parent):
        super().__init__(parent, text="0  ❌", anchor="center", font=("Arial", 28))
        self.place(relx = 0.30, rely=0.95, relheight=0.08, relwidth=0.15, anchor = "center")

class CCount(ctk.CTkLabel):
    def __init__(self, parent):
        super().__init__(parent, text="⚪  0", anchor="center", font=("Arial", 28))
        self.place(relx = 0.70, rely=0.95, relheight=0.08, relwidth=0.15, anchor = "center")
