import tkinter as tk
from interface import App

def start_app():
    root = tk.Tk()
    root.geometry("900x550")
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    start_app()