import tkinter as tk
from tkinter import ttk
import sv_ttk
root = tk.Tk()
root.title("WebUI Launcher")
root.geometry("1000x600")
icon = tk.PhotoImage(file="WindowIcon.png")
root.iconphoto(False, icon)

main_frame = ttk.Frame(root, padding=10)
main_frame.pack(fill="both", expand=True)

left_col = ttk.Frame(main_frame)
left_col.grid(row=0, column=0, sticky="nsew", padx=5)



radio_frame = ttk.LabelFrame(left_col, text="Radiobuttons", padding=10)
radio_frame.pack(fill="x")
var = tk.IntVar()
ttk.Radiobutton(radio_frame, text="Dog", variable=var, value=1).pack(anchor="w")
ttk.Radiobutton(radio_frame, text="Cat", variable=var, value=2).pack(anchor="w")

center_frame = ttk.Frame(main_frame, padding=10)
center_frame.grid(row=0, column=1, sticky="nsew", padx=5)

ttk.Entry(center_frame).pack(fill="x", pady=5)
ttk.Spinbox(center_frame, from_=0, to=10).pack(fill="x", pady=5)
ttk.Combobox(center_frame, values=["Option 1", "Option 2"]).pack(fill="x", pady=5)
ttk.Button(center_frame, text="Click me!").pack(fill="x", pady=20)

accent_btn = ttk.Button(center_frame, text="I love it!", style="Accent.TButton")
accent_btn.pack(fill="x")

right_col = ttk.Frame(main_frame)
right_col.grid(row=0, column=2, sticky="nsew", padx=5)

tree = ttk.Treeview(right_col, columns=("year", "type"), height=8)
tree.heading("#0", text="Name")
tree.insert("", "end", text="Ubuntu", values=("2004", "Fixed"))
tree.insert("", "end", text="Arch", values=("2002", "Rolling"))
tree.pack(fill="x", pady=(0, 10))

notebook = ttk.Notebook(right_col)
tab1 = ttk.Frame(notebook, padding=10)
notebook.add(tab1, text="Tab 1")
notebook.add(ttk.Frame(notebook), text="Tab 2")
notebook.pack(fill="both", expand=True)

# Slider inside Tab 1
ttk.Scale(tab1, from_=0, to=100).pack(fill="x", pady=10)
ttk.Checkbutton(tab1, text="Dark theme", style="Switch.TCheckbutton").pack()

sv_ttk.set_theme("dark")

root.mainloop()