import customtkinter as ctk
from TicTacToe.tictactoev2 import TicTacToeGame

if __name__ == "__main__":
    root = ctk.CTk()
    ctk.set_appearance_mode("dark")
    app = TicTacToeGame(root)
    root.mainloop()