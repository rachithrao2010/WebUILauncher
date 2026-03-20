import tkinter as tk

root = tk.Tk()
root.title("WebUI Launcher")
root.geometry("1000x600")
icon = tk.PhotoImage(file="WindowIcon.png")
root.iconphoto(False, icon)
root.mainloop()