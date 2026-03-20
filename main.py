import tkinter as tk
from tkinter import ttk
import sv_ttk
root = tk.Tk()
root.title("WebUI Launcher")
root.geometry("1000x600")
icon = tk.PhotoImage(file="WindowIcon.png")
root.iconphoto(False, icon)

sv_ttk.set_theme("dark")
style = ttk.Style()

style.layout("TNotebook.Tab", [
    ('Notebook.tab', {
        'sticky': 'nswe', 
        'children': [
            ('Notebook.padding', {
                'side': 'top', 
                'sticky': 'nswe', 
                'children': [
                    ('Notebook.label', {'side': 'top', 'sticky': ''})
                ]
            })
        ]
    })
])



notebook = ttk.Notebook()

launch = ttk.Frame(notebook)
recs = ttk.Frame(notebook, padding = 10)
discover = ttk.Frame(notebook)
settings = ttk.Frame(notebook)

notebook.add(launch, text="Launch")
notebook.add(recs, text="Recommendations")
notebook.add(discover, text="Discover")
notebook.add(settings, text="Settings")

Hardware = ttk.LabelFrame(recs, text="Hardware", padding=10)
Hardware.pack(fill="x", pady=(0, 10))
label = tk.Label(Hardware, text="CPU")
label.pack(pady=20)
label = tk.Label(Hardware, text="RAM")
label.pack(pady=20)
label = tk.Label(Hardware, text="GPU")
label.pack(pady=20)






notebook.pack(fill="both", expand=True)


root.mainloop()