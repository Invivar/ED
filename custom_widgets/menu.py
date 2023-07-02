import tkinter as tk
import os
from tkinter import filedialog, TclError, ttk


class CombinedMenu(tk.Frame):

    def __init__(self, parent, tekst, command, path=None):
        super().__init__(parent)
        self.tekst = tekst
        self.path = path
        self.f1 = ttk.Frame(parent)
        self.f1.pack(fill='both')
        ttk.Label(self.f1, text=tekst, justify='left').pack(fill='both', side='left', padx=10)
        self.b1 = ttk.Button(self.f1, text='...', command=lambda: self._select_action(command))
        self.b1.pack(side='right', padx=5)
        self.e1 = ttk.Entry(self.f1)
        try:
            self.e1.insert(0, self.path)
        except TclError:
            pass
        self.e1.pack(side='right', fill='x', ipady=1, ipadx=100, padx=5)
        self.e1.bind('<Key>', lambda e: self._pressed_entry(e))
        self.e1.image = command
        self.e1.xview('end')
        self.selected_log = path
        self.selected_csv = path
        self.selected_route = path

    # noinspection PyUnresolvedReferences
    def _pressed_entry(self, event):
        if event.widget.image == 1:
            if os.path.exists(self.e1.get()):
                self.selected_log = self.e1.get()
            else:
                print('Not reachable')
        elif event.widget.image == 2:
            if os.path.exists(self.e1.get()):
                self.selected_csv = self.e1.get()
            else:
                print('Not reachable')
        elif event.widget.image == 3:
            if os.path.exists(self.e1.get()):
                self.selected_route = self.e1.get()
            else:
                print('Not reachable')

    def _select_action(self, command):
        if command == 1:
            self.selected_log = filedialog.askdirectory(initialdir=self.path, title=self.tekst)
            if len(self.selected_log) > 0 and os.path.exists(self.selected_log):
                self.e1.insert(0, self.selected_log)
                self.e1.xview('end')
        elif command == 2:
            self.selected_csv = filedialog.askopenfilename(initialdir=self.path, title=self.tekst,
                                                           filetypes=[('CSV Files', '*.csv')])
            if len(self.selected_csv) > 0 and os.path.exists(self.selected_csv):
                self.e1.insert(0, self.selected_csv)
                self.e1.xview('end')
        elif command == 3:
            self.selected_route = filedialog.askopenfilename(initialdir=self.path, title=self.tekst,
                                                             filetypes=[('JSON Files', '*.json')])
            if len(self.selected_route) > 0 and os.path.exists(self.selected_route):
                self.e1.insert(0, self.selected_route)
                self.e1.xview('end')
