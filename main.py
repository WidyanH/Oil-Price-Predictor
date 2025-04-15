# main.py
from views.app_ui import AppUI
import tkinter as tk

def main():
    root = tk.Tk()
    app = AppUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
