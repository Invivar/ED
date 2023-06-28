from tkinter import ttk
import tkinter as tk
from settings.widgets import label_set, widget_set

class CombinedCombobox(tk.Frame):
    def __init__(self, parent, lista, tekst, current):
        super().__init__(parent)
        f1 = ttk.Frame(parent)
        f1.pack(fill='x')
        ttk.Label(f1, text=tekst, justify='left').pack(label_set)
        self.combo = ttk.Combobox(f1, values=lista, state='readonly', width=50)
        self.combo.set(current)
        self.combo.pack(widget_set)