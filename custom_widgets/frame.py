import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import webbrowser
from settings.internal_data import sites

def _open_website(event, what):
    if what:
        link = event.widget.data
    else:
        link = event.widget.image
    webbrowser.open(link)


class CombinedFrame(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent)
        self.canvas = tk.Canvas(self, height=528)
        self.scrollbar = ttk.Scrollbar(self, orient='vertical', command=self.canvas.yview)
        self.scroll_frame = tk.Frame(self.canvas)
        self.scroll_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        for name, link in sites.items():
            frame = tk.Frame(self.scroll_frame)
            frame.pack(fill='both', padx=5)
            label = tk.Label(frame, text=name, justify='left', width=20, anchor='w')
            label.pack(fill='both', padx=5, side='left')
            label.image = link['link']  # yes, silly
            label.bind('<Button-1>', lambda e: _open_website(e, 0))
            tk.Label(frame, text=link['desc'], justify='left', wraplength=440).pack(side='left', fill='both')
            load_image = Image.open(link['image'])
            load_image.thumbnail((100, 100))
            __image = ImageTk.PhotoImage(load_image)
            img = tk.Label(frame, image=__image)
            img.image = __image
            img.pack(side='right', pady=2)
            img.data = link['link']
            img.bind('<Button-1>', lambda e: _open_website(e, 1))
            ttk.Separator(self, orient='horizontal').pack(fill='x', padx=5)