import tkinter as tk
from tkinter import ttk
import sv_ttk
import getHardware
from pathlib import Path
import threading
import multiprocessing

if __name__ == '__main__':

    multiprocessing.freeze_support()

    root = tk.Tk()
    root.title("WebUI Launcher")
    root.geometry("1000x600")
    icon = tk.PhotoImage(file="WindowIcon.png")
    root.iconphoto(False, icon)

    sv_ttk.set_theme("dark")
    Notebookstyle = ttk.Style()

    Notebookstyle.layout("TNotebook.Tab", [
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

    launchbuttonstyle = ttk.Style()

    launchbuttonstyle.configure('Launch.TButton', background='green', font=('Helvetica', 12, 'bold'))


    notebook = ttk.Notebook()

    launch = ttk.Frame(notebook)
    recs = ttk.Frame(notebook, padding = 10)
    discover = ttk.Frame(notebook)
    settings = ttk.Frame(notebook)

    notebook.add(launch, text="Launch")

    launchbutton = ttk.Button(launch, style='Launch.TButton', text="LAUNCH")
    launchbutton.pack(pady=10, anchor="w")
    notebook.add(recs, text="Recommendations")
    notebook.add(discover, text="Discover")
    notebook.add(settings, text="Settings")



    Hardware = ttk.LabelFrame(recs, text="Hardware", padding=10)
    Hardware.pack(fill="x", pady=(0, 10))
    labelCPU = ttk.Label(Hardware, text="CPU: ")
    labelCPU.pack(pady=10, anchor="w")
    labelGPU = ttk.Label(Hardware, text="GPU: ")
    labelGPU.pack(pady=10, anchor="w")
    labelRAM = ttk.Label(Hardware, text="RAM: ")
    labelRAM.pack(pady=10, anchor="w")

    thread = threading.Thread(target=getHardware.updateHardware, args=(labelCPU, labelGPU, labelRAM))
    thread.daemon = True
    thread.start()


    notebook.pack(fill="both", expand=True)


    root.mainloop()