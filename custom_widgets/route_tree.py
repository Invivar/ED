import tkinter as tk
from tkinter import ttk
import math
from side_functions_and_gui.others import selected_item_action


class PlotTree(tk.Frame):
    def __init__(self, parent, plot):
        super().__init__(parent)
        label1 = ttk.Label(self, text='Selected Destination:', justify='left')
        label1.pack(fill='x', padx=10, ipady=5)
        columns = {0: 'No', 1: 'System Name', 2: 'Distance', 3: 'Remaining', 4: 'Jumps Required', 5: 'System Visited'}
        column_size = [30, 200, 120, 100, 100]
        row_no = [x for x, _ in columns.items()]
        treeview = ttk.Treeview(self, show='tree headings', columns=str(row_no), style="Mystyle.Treeview")
        treeview.pack(side='left', fill='both', padx=1, pady=5)
        verscrlbar = ttk.Scrollbar(self, orient="vertical", command=treeview.yview)
        verscrlbar.pack(side='left', fill='y', padx=1, pady=5)
        treeview.configure(height=20, yscrollcommand=verscrlbar.set)
        treeview.column('#0', width=0)
        [treeview.heading(x, text=y, anchor='w') for x, y in columns.items()]
        [treeview.column(i, width=x, anchor='w') for i, x in enumerate(column_size)]
        treeview.bind('<ButtonRelease-1>', lambda g: selected_item_action(g, label1))
        for i, (parent, values) in enumerate(plot.items()):
            try:
                distance = math.ceil(float(values["data"][0]))
                remaining = math.ceil(float(values["data"][1]))
                treeview.insert('', 'end', iid=parent, values=[i + 1, parent,
                                                               f"{distance} Ly",
                                                               f"{remaining} Ly",
                                                               values['data'][3],
                                                               values['done']], open=False)
            except tk.TclError as e:
                print(e)
                pass