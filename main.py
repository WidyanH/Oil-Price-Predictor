# main.py

import tkinter as tk
from views.app_ui import AppUI

if __name__ == "__main__":
    root = tk.Tk()
    app = AppUI(root)
    root.mainloop()

