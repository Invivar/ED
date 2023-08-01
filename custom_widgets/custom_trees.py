import tkinter as tk
from tkinter import ttk
import math
from side_functions_and_gui.others import sel_item_action, save_config
from settings.internal_data import BOOKMARKS_JSON_FILE

def sort_column(tree, column, reverse):
    try:
        local_list = [(float(tree.set(k, column)), k) for k in tree.get_children('')]
    except Exception as e:
        print('lol', e)
        local_list = [(tree.set(k, column), k) for k in tree.get_children('')]
    local_list.sort(reverse=reverse)
    for index, (val, k) in enumerate(local_list):
        tree.move(k, '', index)
    tree.heading(column, command=lambda _col=column: sort_column(tree, _col, not reverse))


class PlotTree(tk.Frame):
    def __init__(self, parent, plot, closing, ancestor):
        super().__init__(parent)
        self.fast_close = closing
        self.plot = plot
        label1 = ttk.Label(self, text='Selected Destination:', justify='left')
        label1.pack(fill='x', padx=10, ipady=5)
        columns = {0: 'No', 1: 'System Name', 2: 'Distance', 3: 'Remaining', 4: 'Jumps Required', 5: 'System Visited'}
        column_size = [30, 200, 120, 120, 120, 120]
        row_no = [x for x, _ in columns.items()]
        self.treeview = ttk.Treeview(self, show='tree headings', columns=str(row_no),
                                     style="Mystyle.Treeview", name='plot')
        self.treeview.pack(side='left', fill='both', padx=1, pady=5)
        verscrlbar = ttk.Scrollbar(self, orient="vertical", command=self.treeview.yview)
        verscrlbar.pack(side='left', fill='y', padx=1, pady=5)
        self.treeview.configure(height=20, yscrollcommand=verscrlbar.set)
        self.treeview.column('#0', width=0)
        for x, y in columns.items():
            self.treeview.heading(x, text=y, anchor='w', command=lambda _c=x: sort_column(self.treeview, _c, False))
        [self.treeview.column(i, width=x, anchor='w') for i, x in enumerate(column_size)]
        self.treeview.bind('<<TreeviewSelect>>', lambda g: sel_item_action(g, label1, self.fast_close, ancestor, 0))
        self.treeview.bind('<Double-1>', lambda g: sel_item_action(g, label1, self.fast_close, ancestor, 1))
        for i, (parent, values) in enumerate(plot.items()):
            try:
                distance = math.ceil(float(values["data"][0]))
                remaining = math.ceil(float(values["data"][1]))
                self.treeview.insert('', 'end', iid=parent, values=[i + 1, parent,
                                                                    f"{distance} Ly",
                                                                    f"{remaining} Ly",
                                                                    values['data'][3],
                                                                    values['done']], open=False)
            except tk.TclError as e:
                print(e)

    def update_tree(self, plot):
        self.plot = plot
        for item in self.treeview.get_children():
            self.treeview.delete(item)
        for i, (parent, values) in enumerate(plot.items()):
            try:
                distance = math.ceil(float(values["data"][0]))
                remaining = math.ceil(float(values["data"][1]))
                self.treeview.insert('', 'end', iid=parent, values=[i + 1, parent,
                                                                    f"{distance} Ly",
                                                                    f"{remaining} Ly",
                                                                    values['data'][3],
                                                                    values['done']], open=False)
            except tk.TclError as e:
                print(e)


class CCHTree(tk.Frame):
    def __init__(self, parent, plot, closing, ancestor, direction):
        super().__init__(parent)
        self.fast_close = closing
        self.plot = plot
        label1 = ttk.Label(self, text='Selected Destination:', justify='left')
        label1.pack(fill='x', padx=10, ipady=5)
        columns = {0: 'No', 1: 'System Name', 2: 'Port Name', 3: 'Remaining', 4: 'System Visited'}
        column_size = [30, 180, 180, 160, 160]
        row_no = [x for x, _ in columns.items()]
        self.treeview = ttk.Treeview(self, show='tree headings', columns=str(row_no),
                                     style="Mystyle.Treeview", name='plot')
        self.treeview.pack(side='left', fill='both', padx=1, pady=5)
        verscrlbar = ttk.Scrollbar(self, orient="vertical", command=self.treeview.yview)
        verscrlbar.pack(side='left', fill='y', padx=1, pady=5)
        self.treeview.configure(height=22, yscrollcommand=verscrlbar.set)
        self.treeview.column('#0', width=0)
        for x, y in columns.items():
            self.treeview.heading(x, text=y, anchor='w', command=lambda _c=x: sort_column(self.treeview, _c, False))
        [self.treeview.column(i, width=x, anchor='w') for i, x in enumerate(column_size)]
        self.treeview.bind('<<TreeviewSelect>>', lambda g: sel_item_action(g, label1, self.fast_close, ancestor, 0))
        self.treeview.bind('<Double-1>', lambda g: sel_item_action(g, label1, self.fast_close, ancestor, 1))
        for i, (parent, values) in enumerate(plot.items()):
            try:
                if direction:
                    remaining = values["data"][4].replace('\n', '')
                else:
                    remaining = values["data"][3].replace('\n', '')
                self.treeview.insert('', 'end', iid=parent, values=[i + 1, parent,
                                                                    values['data'][0],
                                                                    f"{remaining} Ly",
                                                                    values['done']], open=False)
            except tk.TclError as e:
                print(e)

    def update_tree(self, plot, direction):
        self.plot = plot
        for item in self.treeview.get_children():
            self.treeview.delete(item)
        for i, (parent, values) in enumerate(plot.items()):
            try:
                if direction:
                    remaining = values["data"][4].replace('\n', '')
                else:
                    remaining = values["data"][3].replace('\n', '')
                self.treeview.insert('', 'end', iid=parent, values=[i + 1, parent,
                                                                    values['data'][0],
                                                                    f"{remaining} Ly",
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
        self.treeview = ttk.Treeview(self, show='tree headings', columns=str(row_no), style="Mystyle.Treeview",
                                     name='commo')
        self.treeview.pack(side='left', fill='both', padx=1, pady=5)
        verscrlbar = ttk.Scrollbar(self, orient="vertical", command=self.treeview.yview)
        verscrlbar.pack(side='left', fill='y', padx=1, pady=5)
        self.treeview.configure(height=16, yscrollcommand=verscrlbar.set)
        self.treeview.column('#0', width=0)
        for x, y in columns.items():
            self.treeview.heading(x, text=y, anchor='w', command=lambda _c=x: sort_column(self.treeview, _c, False))
        [self.treeview.column(i, width=x, anchor='w') for i, x in enumerate(column_size)]
        self.treeview.bind('<<TreeviewSelect>>', lambda g: sel_item_action(g, label1, self.fast_close, ancestor, 0))
        self.treeview.bind('<Double-1>', lambda g: sel_item_action(g, label1, self.fast_close, ancestor, 1))
        self.update_tree(plot)

    def update_tree(self, plot):
        for item in self.treeview.get_children():
            self.treeview.delete(item)
        self.update()
        self.plot = plot
        if len(self.plot) > 0 and isinstance(self.plot, dict):
            for parent, values in self.plot.items():
                try:
                    self.treeview.insert('', 'end', iid=parent, values=values, open=False)
                except tk.TclError as e:
                    print(e)


class SettingTree(tk.Frame):
    def __init__(self, parent, plot):
        super().__init__(parent)
        self.plot = plot
        columns = {0: 'Name', 1: 'In use', 2: 'Size', 3: 'Number of systems', 4: 'Loaded'}
        column_size = [200, 150, 110, 150, 100]
        row_no = [x for x, _ in columns.items()]
        self.treeview = ttk.Treeview(self, show='tree headings', columns=str(row_no), style="Mystyle.Treeview",
                                     name='setting')
        self.treeview.pack(side='left', fill='both', padx=1, pady=5)
        verscrlbar = ttk.Scrollbar(self, orient="vertical", command=self.treeview.yview)
        verscrlbar.pack(side='left', fill='y', padx=1, pady=5)
        self.treeview.configure(height=9, yscrollcommand=verscrlbar.set)
        self.treeview.column('#0', width=0)
        for x, y in columns.items():
            self.treeview.heading(x, text=y, anchor='w', command=lambda _c=x: sort_column(self.treeview, _c, False))
        [self.treeview.column(i, width=x, anchor='w') for i, x in enumerate(column_size)]
        self.treeview.configure(height=7)
        self.update_tree(plot)

    def update_tree(self, plot):
        for item in self.treeview.get_children():
            self.treeview.delete(item)
        self.update()
        self.plot = plot
        if len(self.plot) > 0 and isinstance(self.plot, dict):
            for parent, values in self.plot.items():
                try:
                    temp_list = [parent]
                    [temp_list.append(x) for i, x in enumerate(values.values()) if i > 0]
                    self.treeview.insert('', 'end', iid=parent, values=temp_list, open=False)
                except tk.TclError as e:
                    print(e)


class AddBookmark(tk.Toplevel):
    def __init__(self, parent, combined_entry, position, mode, selected):
        super().__init__(parent)
        self.parent = parent
        self.attributes('-topmost', 1)
        self.grab_set()
        self.title('Add Bookmark')
        self.iconbitmap(r'favicon.ico')
        f1 = ttk.Frame(self)
        f1.pack(fill='x', padx=10, pady=10)
        self.combined_entry = combined_entry(self, position, 'Location')
        if mode == 1:
            self.combined_entry.entry.delete(0, 'end')
            self.combined_entry.entry.insert(0, selected[0])
            self.combined_entry.entry.configure(state='disabled')
            self.combined_entry.b1.configure(state='disabled')
        self.text_entry = tk.Text(self, relief='solid')
        self.text_entry.pack(fill='both', padx=10, pady=10)
        f2 = ttk.Frame(self)
        f2.pack(fill='x')
        b1 = ttk.Button(f2, text='OK', command=lambda: self._send_to_parent(mode))
        b1.pack(side='right', fill='x', padx=10, pady=10)

    def _send_to_parent(self, mode):
        if mode == 0:
            self.parent.add_to_bookmark(self.combined_entry.entry.get(), self.text_entry.get(1.0, 'end'))
        elif mode == 1:
            self.parent.edit_bookmark(self.combined_entry.entry.get(), self.text_entry.get(1.0, 'end'))


class BookmarkTree(tk.Frame):
    def __init__(self, parent, plot, closing, ancestor, combined, position):
        super().__init__(parent)
        self.plot = plot
        self.combined = combined
        self.position = position
        self.fast_close = closing
        f1 = ttk.Frame(self)
        f1.pack(fill='x')
        self._top_lvl = None
        label1 = ttk.Label(f1, text='Selected Destination:', justify='left')
        label1.pack(fill='x', padx=10, ipady=5, side='left')
        self.b1 = ttk.Button(f1, text='Add Bookmark', command=lambda: self._open_top_level(0))
        self.b1.pack(padx=10, pady=10, side='right')
        self.b2 = ttk.Button(f1, text='Edit Bookmark', command=lambda: self._open_top_level(1), state='disabled')
        self.b2.pack(padx=10, pady=10, side='right')
        self.b3 = ttk.Button(f1, text='Delete Bookmark', command=lambda: self._open_top_level(2), state='disabled')
        self.b3.pack(padx=10, pady=10, side='right')
        columns = {0: 'System Name', 1: 'Description'}
        column_size = [200, 510]
        row_no = [x for x, _ in columns.items()]
        self.treeview = ttk.Treeview(self, show='tree headings', columns=str(row_no), style="Mystyle.Treeview",
                                     name='bookmark')
        self.treeview.pack(side='left', fill='both', padx=1, pady=5)
        verscrlbar = ttk.Scrollbar(self, orient="vertical", command=self.treeview.yview)
        verscrlbar.pack(side='left', fill='y', padx=1, pady=5)
        self.treeview.configure(height=22, yscrollcommand=verscrlbar.set)
        self.treeview.column('#0', width=0)
        for x, y in columns.items():
            self.treeview.heading(x, text=y, anchor='w', command=lambda _c=x: sort_column(self.treeview, _c, False))
        [self.treeview.column(i, width=x, anchor='w') for i, x in enumerate(column_size)]
        self.treeview.bind('<<TreeviewSelect>>', lambda g: sel_item_action(g, label1, self.fast_close, ancestor, 0))
        self.treeview.bind('<Double-1>', lambda g: sel_item_action(g, label1, self.fast_close, ancestor, 1))
        self.update_tree(plot)

    # noinspection PyUnboundLocalVariable
    def _open_top_level(self, mode):
        pack = []
        if mode in [1, 2]:
            data = self.treeview.selection()[0]
            descr = self.plot[data]
            pack = data, descr
        if mode in [0, 1]:
            self._top_lvl = AddBookmark(self, self.combined, self.position, mode, pack)
            self._top_lvl.mainloop()
        else:
            del self.plot[data]
            self.update_tree(self.plot)

    def add_to_bookmark(self, name, description):
        if name not in self.plot:
            self.plot[name] = description
        self.update_tree(self.plot)

    def edit_bookmark(self, name, description):
        self.plot[name] = description
        self.update_tree(self.plot)

    def update_tree(self, plot):
        for item in self.treeview.get_children():
            self.treeview.delete(item)
        self.update()
        self.plot = plot
        if len(self.plot) > 0 and isinstance(self.plot, dict):
            for parent, values in self.plot.items():
                try:
                    self.treeview.insert('', 'end', iid=parent, values=[parent, values], open=False)
                except tk.TclError as e:
                    print(e)
        save_config(BOOKMARKS_JSON_FILE, self.plot)
