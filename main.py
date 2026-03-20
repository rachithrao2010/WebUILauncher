import tkinter as tk
from tkinter import ttk
import sv_ttk
root = tk.Tk()
root.title("WebUI Launcher")
root.geometry("1000x600")
icon = tk.PhotoImage(file="WindowIcon.png")
root.iconphoto(False, icon)

notebook = ttk.Notebook()
tab1 = ttk.Frame(notebook, padding=10)
notebook.add(tab1, text="Tab 1")
notebook.add(ttk.Frame(notebook), text="Tab 2")
notebook.pack(fill="both", expand=True)

sv_ttk.set_theme("dark")

root.mainloop()