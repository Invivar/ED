import tkinter as tk
from tkinter import ttk
import math
from side_functions_and_gui.others import selected_item_action


class PlotTree(tk.Frame):
    def __init__(self, parent, plot, closing, ancestor):
        super().__init__(parent)
        self.fast_close = closing
        label1 = ttk.Label(self, text='Selected Destination:', justify='left')
        label1.pack(fill='x', padx=10, ipady=5)
        columns = {0: 'No', 1: 'System Name', 2: 'Distance', 3: 'Remaining', 4: 'Jumps Required', 5: 'System Visited'}
        column_size = [30, 200, 120, 120, 40]
        row_no = [x for x, _ in columns.items()]
        treeview = ttk.Treeview(self, show='tree headings', columns=str(row_no), style="Mystyle.Treeview")
        treeview.pack(side='left', fill='both', padx=1, pady=5)
        verscrlbar = ttk.Scrollbar(self, orient="vertical", command=treeview.yview)
        verscrlbar.pack(side='left', fill='y', padx=1, pady=5)
        treeview.configure(height=20, yscrollcommand=verscrlbar.set)
        treeview.column('#0', width=0)
        [treeview.heading(x, text=y, anchor='w') for x, y in columns.items()]
        [treeview.column(i, width=x, anchor='w') for i, x in enumerate(column_size)]
        treeview.bind('<ButtonRelease-1>', lambda g: selected_item_action(g, label1, self.fast_close, ancestor, 0))
        treeview.bind('<Double-1>', lambda g: selected_item_action(g, label1, self.fast_close, ancestor, 1))
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


class CommodityTree(tk.Frame):
    def __init__(self, parent, plot, closing, ancestor):
        super().__init__(parent)
        self.plot = plot
        self.fast_close = closing
        label1 = ttk.Label(self, text='Selected Destination:', justify='left')
        label1.pack(fill='x', padx=10, ipady=5)
        columns = {0: 'System Name', 1: 'Station Name', 2: 'Pad Size', 3: 'Sell Price', 4: 'Buy Price',
                   5: 'Demand', 6: 'Supply', 7: 'Distance(LY)', 8: 'Updated'}
        column_size = [100, 100, 30, 80, 80, 80, 80, 80, 80]
        row_no = [x for x, _ in columns.items()]
        self.treeview = ttk.Treeview(self, show='tree headings', columns=str(row_no), style="Mystyle.Treeview")
        self.treeview.pack(side='left', fill='both', padx=1, pady=5)
        verscrlbar = ttk.Scrollbar(self, orient="vertical", command=self.treeview.yview)
        verscrlbar.pack(side='left', fill='y', padx=1, pady=5)
        self.treeview.configure(height=18, yscrollcommand=verscrlbar.set)
        self.treeview.column('#0', width=0)
        [self.treeview.heading(x, text=y, anchor='w') for x, y in columns.items()]
        [self.treeview.column(i, width=x, anchor='w') for i, x in enumerate(column_size)]
        self.treeview.bind('<ButtonRelease-1>', lambda g: selected_item_action(g, label1, self.fast_close, ancestor, 0))
        self.treeview.bind('<Double-1>', lambda g: selected_item_action(g, label1, self.fast_close, ancestor, 1))

    def update_tree(self, plot):
        for item in self.treeview.get_children():
            self.treeview.delete(item)
        self.update()
        self.plot = plot
        if len(self.plot) > 0 and isinstance(self.plot, dict):
            for _, values in self.plot.items():
                try:
                    self.treeview.insert('', 'end', iid=values[0], values=values, open=False)
                except tk.TclError as e:
                    print(e)
