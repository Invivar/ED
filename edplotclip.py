"""
At the beginning it was just a smart copypaste addon for route plotter csv.
Now, I like it and add some features in free time.
Not everything works, some lags exists, soo.. yeah.
TODO:
    - Extended configuration file - still extending
    - MySQL requests - connected or not, login client ect.
    - Pinned Locations with short Notes (I have no idea what I have saved in the tabs in the game)

FIXME:
    - APPROX JUMPS
    - LOAD CSV, JSON AND TREEVIEW IN PLOTROUTE, CORRECT CATALOGS
"""
import os
import re
import threading
from tkinter import TclError, filedialog
from pynput.keyboard import Listener
import time
from json.decoder import JSONDecodeError
import pyperclip
from win32gui import GetWindowText, GetForegroundWindow
from copy import deepcopy as dc
import requests
import gc
from bs4 import BeautifulSoup
from ctypes import windll
from multiprocessing import Pipe, Process, freeze_support
from settings.internal_data import *
from settings.widgets import label_set, entry_set
from settings.separate_process import Dswedrftgyhuji
from custom_widgets.frame import CombinedFrame
from custom_widgets.menu import CombinedMenu
from custom_widgets.combobox import CombinedCombobox
from custom_widgets.custom_trees import *
from side_functions_and_gui.others import help_, smart_gui, sizeof_fmt
import mysql.connector
import password
import json
from side_functions_and_gui import gui_bridge, others

windll.shcore.SetProcessDpiAwareness(1)
windll.user32.ShowWindow(windll.kernel32.GetConsoleWindow(), 6)
gc.set_threshold(1, 20, 20)


def _setvar(opt):
    if plot_route.settings[opt]:
        plot_route.settings[opt] = False
    else:
        plot_route.settings[opt] = True
    plot_route.send_settings = True
    save_config(CONFIG_JSON_FILE, plot_route.settings)
    pass


class SettingWidget(ttk.Frame):
    def __init__(self, parent, text, option):
        super().__init__(parent)
        self.boolvar = tk.BooleanVar()
        self.select = ttk.Checkbutton(self, text=text, command=lambda: _setvar(option),
                                      name=option, variable=self.boolvar)  # rip ttk :<
        if plot_route.settings[option]:
            self.boolvar.set(True)
        else:
            self.boolvar.set(False)
        if 'use_local_database' in option:
            temp_list = [x['in_use'] for x in plot_route.settings['stored_data'].values()]
            if any('Yes' in x for x in temp_list):
                self.select.configure(state='normal')
            else:
                self.boolvar.set(False)
                self.select.configure(state='disabled')
        self.select.pack(label_set)
        self.pack(fill='x')


def _set_clicked(event, mode):
    if mode == 1:
        event.widget.clicked = True
        event.widget.focus_set()
        event.widget.configure(highlightbackground='#6433FF')
    elif mode == 2:
        event.widget.configure(bg='#FCFFB7', text='<BindKey>', anchor='center')
        event.widget.grab_set()
        event.widget.selected = True


def _on_motion(event, _in):
    if _in:
        if not event.widget.clicked:
            event.widget.configure(highlightbackground='black')
        else:
            event.widget.configure(highlightbackground='#6433FF')
    else:
        event.widget.configure(highlightbackground='grey')
        event.widget.clicked = False


class ShortCuts(tk.Frame):
    def __init__(self, parent, text, option, shortcuts):
        super().__init__(parent)
        ttk.Label(self, text=text, justify='left', width=25).pack(side='left')
        e1 = tk.Label(self, text=shortcuts[option], highlightbackground='grey', highlightthickness=1,
                      width=10, anchor='e', bg='white')
        e1.bind('<Motion>', lambda e: _on_motion(e, 1))
        e1.bind('<Button-1>', lambda e: _set_clicked(e, 1))
        e1.bind('<Double-1>', lambda e: _set_clicked(e, 2))
        e1.bind('<Leave>', lambda e: _on_motion(e, 0))
        e1.bind('<KeyRelease>', lambda e: self._validate(e))
        e1.pack(side='left')
        e1.clicked = False
        e1.selected = False
        self.shortcuts = shortcuts
        self.option = option
        self.pack(fill='x', padx=10, pady=2)

    def _validate(self, event):
        if event.widget.selected:
            key = plot_route.current_k
            if key not in self.shortcuts.values():
                self.shortcuts[self.option] = key
                event.widget.selected = False
                event.widget.configure(bg='white', text=key, anchor='e')
                event.widget.grab_release()
                save_config(CONFIG_JSON_FILE, plot_route.settings)


class PartSettingTree(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.b1 = ttk.Button(self, text='Load Local Maps (.json)', command=plot_route.load_custom_data)
        self.b1.pack(padx=5, pady=5, side='left')
        self.b2 = ttk.Button(self, text='Load Map', command=plot_route.pipe_request)
        self.b2.pack(padx=5, pady=5, side='left')
        self.b3 = ttk.Button(self, text='Delete', command=plot_route.delete_stored, state='disabled')
        self.b3.pack(padx=5, pady=5, side='right')
        self.b3.data = ''


class PartSettingFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.c1 = SettingWidget(self, text='Use local database (json)', option='use_local_database')
        SettingWidget(self, text='Close after double click location', option='close_clipping')
        # SettingWidget(self, text='Copy CSV to App', option='copy_to_app')
        SettingWidget(self, text='Inara result in short commodity', option='use_inara')
        self.c2 = SettingWidget(self, text='Use Colonia Connection Highway', option='use_cch')
        ttk.Separator(self, orient='horizontal').pack(fill='x', padx=5, pady=2)
        ShortCuts(self, text='Open Smart ED', shortcuts=plot_route.settings['shortcuts'], option='setting')
        ShortCuts(self, text='Copy Next PyPlotter', shortcuts=plot_route.settings['shortcuts'], option='next')
        ShortCuts(self, text='Copy Best Commodities', shortcuts=plot_route.settings['shortcuts'], option='shop')
        ShortCuts(self, text='Exit App', shortcuts=plot_route.settings['shortcuts'], option='exit')


class CombinedEntry(tk.Frame):

    def __init__(self, parent, reference, text):
        super().__init__(parent)
        self.parent = parent
        self.galactic_maps = {}
        self.reference = reference
        self.f1 = ttk.Frame(parent)
        self.f1.pack(fill='x')
        ttk.Label(self.f1, text=text, justify='left').pack(label_set)
        self.b1 = ttk.Button(self.f1, text='Current', command=self._paste_ship_pos)
        self.b1.pack(fill='x', side='right', padx=5)
        self.f2 = ttk.Frame(self.f1)
        self.f2.pack(fill='x', side='right')
        self.entry = ttk.Entry(self.f2, width=38)
        self.entry.bind('<KeyRelease>', lambda e: self.request_from(e))
        self.entry.bind('<Escape>', lambda e: self.listbox.place_forget())
        try:
            self.entry.insert(0, self.reference.replace('+', ' '))
        except TclError:
            pass
        except AttributeError:
            pass
        self.entry.pack(entry_set)
        self.listbox = tk.Listbox(parent, relief='flat', width=200, height=100)
        self.scroll = ttk.Scrollbar(self.listbox, command=self.listbox.yview)
        self.listbox.configure(yscrollcommand=self.scroll.set)
        self.listbox.bind('<Return>', lambda e: self._check_selection(e))
        self.listbox.bind('<Double-Button-1>', lambda e: self._check_selection(e))
        self.listbox.bind('<Escape>', lambda e: self.listbox.place_forget())

    def _paste_ship_pos(self):
        self.entry.delete(0, "end")
        try:
            self.entry.insert(0, plot_route.ship_pos)
        except TclError:
            pass
        plot_route.com_data['ref'] = self.entry.get().replace(' ', '+')
        save_config(LAST_COMMODITY_FILE, plot_route.com_data)
        pass

    def _check_selection(self, event):
        selected = str(event.widget.selection_get())
        self.entry.delete(0, 'end')
        self.entry.insert(0, selected)
        self.listbox.place_forget()

    def request_from(self, event):
        if plot_route.settings['use_local_database']:
            self._request_local(event)
        else:
            self._request_mysql(event)

    def _request_local(self, event):
        if str(event.keysym) != 'Escape':
            text = event.widget.get()
            if len(text) >= 1:
                regrex = re.compile(f'^{text}', re.I)
                self.galactic_maps = [x for x in plot_route.galactic_maps if regrex.match(x)]
            self._check_database()

    def _request_mysql(self, event):
        if str(event.keysym) != 'Escape':
            text = event.widget.get()
            if len(text) >= 1 and plot_route.cursor is not None:
                command = f"SELECT name FROM ed.powerplay WHERE name REGEXP '^{text}'"
                plot_route.cursor.execute(command)
                self.galactic_maps = plot_route.cursor.fetchall()
                for i, item in enumerate(self.galactic_maps):
                    try:
                        # noinspection PyTypeChecker
                        self.galactic_maps[i] = item[0]
                    except Exception as e:
                        print(e)
            self._check_database()

    def _check_database(self):
        if len(self.galactic_maps) > 0 and len(self.entry.get()) > 0:
            if not self.listbox.winfo_viewable():
                self.scroll.pack(side='right', fill='y')
                x = self.f2.winfo_x() + 5
                y = self.f1.winfo_y() + 24
                self.listbox.place(x=x, y=y, width=506, height=300)
                self.listbox.lift()
                self.listbox.update()
            self.listbox.delete(0, "end")
            self.listbox.insert(0, *self.galactic_maps)
            pass
        else:
            self.listbox.delete(0, "end")
            self.listbox.place_forget()
            self.scroll.pack_forget()
        pass


def _req(i, zbior, element):
    if i + 1 != len(zbior):
        if i == 3:
            return int(element.text)
        else:
            return str(element.text).strip()
    else:
        return int(str(time.time()).split('.')[0]) - int(element.attrs['data-sort'])


def _load_config(path):
    with open(path) as json_manager:
        try:
            dict_data = json.load(json_manager)
            return dict_data
        except JSONDecodeError as e:
            print(e, f'in {path}.json')
            exit(1)
        except IndexError:
            raise IndexError('Config file compromised')
    print('CONFIG FILE LOADED')


def save_config(path, data):
    with open(path, 'w') as json_manager:
        json.dump(data, json_manager, indent=2)
        json_manager.close()


def _recreate(data):
    if '-' in data:
        data = str(data).split('-')[1].strip()
    data = data.replace(',', '').strip()
    return int(data)


class PlotPyperClip:

    def __init__(self):

        self.parent_pipe, self.child_pipe = Pipe()

        self.ship_pos_regrex = re.compile(SHIP_SYNTAX, re.I)
        self.cmdr_regrex = re.compile(UID_SYNTAX, re.I)
        self.log_path_is_safe = re.compile(SAFE_LOG_PATH_REQ, re.I)
        self.inara_time = re.compile(INARA_SYNTAX, re.I)

        self._log_thread = threading.Thread(target=self._background_loop)
        self._keyboard_thread = threading.Thread(target=self._run_listener)
        self._compare_thread = threading.Thread(target=self._pos_to_csv_loop)
        self._once_pipe_loop = threading.Thread(target=self._pipe_loop)

        self.checked_systems = []
        self.replace_loop = ['\ue823\ufe0e', '\ue81d\ufe0e', '\ue81d\ue84f', '\ue84f\ufe0e', "PP+", '\ue84e\ufe0e',
                             '\ue84d\ufe0e', '\ue823\ufe0e', 'Cr']

        self.newest_log_file = ''
        self.log_content = ''
        self.next_system = ''
        self.port = ''
        self.last_system = ''
        self.current_k = ''
        self.selected_json_data = ''

        self.process = None
        self.ship_pos = None
        self.cmdr = None
        self.start_up = True
        self.comparision_founded = False
        self.wake_gui = False
        self.monitoring_route = False
        self.validate_route = False
        self.continous_path = False
        self.run_script = False
        self.remaining = None
        self.close_thread = False
        self.key_manager = None
        self.open_commodity = False
        self.commodity_error = False
        self.check_commodity = False
        self.sql = None
        self.cursor = None
        self.gui_started = False
        self.send_settings = False
        self.update_data_from_process = False
        self.updating = False
        self.short_present = False
        self.custom_event_1 = None
        self.gui_closed = False

        self.processed = 0

        self.galactic_maps = set()
        self.drogie = {}
        self.inara_comm = {}
        self.empty_dict = {}
        self.plot_route_from_csv = {}
        self.cch_route = {}
        self.settings = {'log_path': '',
                         'csv_path': '',
                         'json_path': '',
                         'data_base_file': '',
                         'cmdr': '',
                         'CCHTC': True,
                         'use_local_database': False,
                         'close_clipping': False,
                         'use_inara': True,
                         'use_cch': False,
                         'copy_to_app': False,
                         'stored_data': {},
                         'shortcuts': {'setting': 'Key.f2',
                                       'next': 'Key.f3',
                                       'shop': 'Key.f4',
                                       'exit': 'Key.f10'}
                         }
        self.com_data = {'way': 'selling',
                         'what': 'platinum',
                         'ref': 'omicron+capricorni+b',
                         'last': {}}
        self.time_recalc = {0: 1, 1: 60, 2: 3600, 3: 86400}
        self.bookmarks = {}

        self.link = fr'http://edlegacy.iloveitmore.com.au/?action=' \
                    fr'{self.com_data["way"]}&commodity={self.com_data["what"]}&reference={self.com_data["ref"]}'

    def _gui(self):
        gui_bridge.gui_started = True
        self.root = tk.Tk()
        self.root.geometry('+%d+%d' % (10, 20))
        self.root.protocol('WM_DELETE_WINDOW', self._ready)
        self.root.withdraw()  # hide during loading all frames etc.
        self.root.iconbitmap(r'favicon.ico')
        self.root.attributes('-topmost', 1)
        self.root.title('Smart ED Legacy')
        self.root.resizable(False, False)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(padx=10, fill='both')

        self.ntbkf_1 = ttk.Frame(self.notebook)
        self.f1 = CombinedMenu(self.ntbkf_1, 'Select Log Folder', 1, self.settings['log_path'])
        self.f1.pack()
        self.f2 = CombinedMenu(self.ntbkf_1, 'Select CSV File', 2,
                               self.settings['csv_path'])
        self.f2.pack()
        self.f3 = CombinedMenu(self.ntbkf_1, 'Select JSON  Neutron Route', 3,
                               self.settings['json_path'])
        self.f3.pack()
        ttk.Separator(self.ntbkf_1, orient='horizontal').pack(fill='x', padx=5, pady=2)
        self.settings_gui = PartSettingFrame(self.ntbkf_1)
        self.settings_gui.pack(fill='x')
        ttk.Separator(self.ntbkf_1, orient='horizontal').pack(fill='x', padx=5, pady=2)
        self.f8 = PartSettingTree(self.ntbkf_1)
        self.f8.pack(fill='x')
        self.f7 = SettingTree(self.ntbkf_1, self.settings['stored_data'])
        self.f7.treeview.bind('<<TreeviewSelect>>', lambda e: self.current_selection(e))
        self.f7.treeview.bind('<Double-1>', lambda e: self.current_selection(e, True))
        self.f7.pack(fill='x')
        self.ntbkf_1.pack(fill='x')

        self.ntbkf_2 = ttk.Frame(self.notebook)
        self.ntbkf_2_notebook = ttk.Notebook(self.ntbkf_2)
        self.ntbkf_2_legacy = ttk.Frame(self.ntbkf_2_notebook)
        self.ntbkf_2_inara = ttk.Frame(self.ntbkf_2_notebook)
        self.e1 = CombinedEntry(self.ntbkf_2, self.com_data["ref"], 'Select Start System')
        self.e1.pack(fill='x')
        self.c1 = CombinedCombobox(self.ntbkf_2, what, 'Action', self.com_data["way"])
        self.c2 = CombinedCombobox(self.ntbkf_2_legacy, products_list, 'Product', self.com_data["what"])
        self.c3 = CombinedCombobox(self.ntbkf_2_inara, [x for _, x in self.inara_comm.items()],
                                   'Product', self.com_data["what"])
        self.f5 = ttk.Frame(self.ntbkf_2)
        self.f5.pack(fill='both')
        self.button = ttk.Button(self.ntbkf_2_legacy, text='Check Price',
                                 command=lambda: self._set_commodity(0))
        self.button.pack(padx=5, pady=3, side='right')
        self.butto2 = ttk.Button(self.ntbkf_2_inara, text='Check Price', command=lambda: self._set_commodity(1))
        self.butto2.pack(padx=5, pady=3, side='right')
        self.ntbkf_2_notebook.pack(padx=10, fill='both')
        self.tree = CommodityTree(self.ntbkf_2, self.com_data["last"], self.settings['close_clipping'], self.root)
        self.tree.pack(fill='both')
        self.ntbkf_2_legacy.pack(fill='both')
        self.ntbkf_2_inara.pack(fill='both')
        self.ntbkf_2_notebook.add(self.ntbkf_2_legacy, text='Legacy')
        self.ntbkf_2_notebook.add(self.ntbkf_2_inara, text='Inara')
        self.ntbkf_2.pack()

        self.ntbkf_3 = ttk.Frame(self.notebook)
        t1 = f"Current Ship Position: {self.ship_pos}"
        self.lab_ship_pos = ttk.Label(self.root, text=t1, justify='left')
        self.lab_ship_pos.pack(fill='x', padx=10, ipady=5)
        t2 = f"Next System: {self.next_system}"
        self.next_system_lab = ttk.Label(self.ntbkf_3, text=t2, justify='left')
        self.next_system_lab.pack(fill='x', padx=10, ipady=5)
        t3 = f"Approx Jumps: {self.remaining}"
        self.jumps_re_lab = ttk.Label(self.ntbkf_3, text=t3, justify='left')
        self.jumps_re_lab.pack(fill='x', padx=10, ipady=5)
        self.f6 = PlotTree(self.ntbkf_3, self.plot_route_from_csv, self.settings['close_clipping'], self.root)
        self.f6.pack(fill='both')
        self.ntbkf_3.pack()

        self.ntbkf_4 = ttk.Frame(self.notebook)
        pack = (self.ntbkf_4, self.bookmarks, self.settings['close_clipping'], self.root, CombinedEntry, self.ship_pos)
        self.f9 = BookmarkTree(*pack)
        self.f9.pack(fill='both')
        self.ntbkf_4.pack()

        self.ntbkf_5 = ttk.Frame(self.notebook)
        self.shortcut_frame = CombinedFrame(self.ntbkf_5)
        self.shortcut_frame.pack(fill='both')
        self.ntbkf_5.pack()

        self.ntbkf_6 = ttk.Frame(self.notebook)
        f1 = ttk.Frame(self.ntbkf_6)
        f1.pack(fill='both')
        self.cch_button = ttk.Button(f1, command=self._cch_set_to, text='Direction')
        self.cch_button.pack(side='left')
        self.cch_label = ttk.Label(f1)
        self.cch_label.pack(side='left', padx=10)
        if self.settings['use_cch']:
            if self.settings['CCHTC']:
                self.cch_label.configure(text='Colonia')
            else:
                self.cch_label.configure(text='Sol')
        else:
            self.cch_label.configure(text='Switch Checkbox')
        self.f10 = CCHTree(self.ntbkf_6, standard_highway, self.settings['close_clipping'], self.root,
                           self.settings['CCHTC'])
        self.f10.pack(fill='both')
        self.ntbkf_6.pack()

        self.notebook.add(self.ntbkf_1, text='Settings')
        self.notebook.add(self.ntbkf_2, text='Commodity')
        self.notebook.add(self.ntbkf_3, text='Current Travel')
        self.notebook.add(self.ntbkf_6, text='CC Highway')
        self.notebook.add(self.ntbkf_4, text='Bookmarks')
        self.notebook.add(self.ntbkf_5, text='Usefull Sites')

        self.f4 = ttk.Frame(self.root)
        self.f4.pack(fill='both')
        self.b1 = ttk.Button(self.f4, text='OK', command=self._ready)
        self.b1.pack(padx=5, pady=5, side='right')
        self.b2 = ttk.Button(self.f4, text='Finish JSON & CSV', command=self._delete)
        self.b2.pack(padx=5, pady=5, side='right')
        self.b4 = ttk.Button(self.f4, text='Copy Ship Pos', command=self._copy_position)
        self.b4.pack(padx=5, pady=5, side='right')
        self.b3 = ttk.Button(self.f4, text='Help', command=help_)
        self.b3.pack(padx=5, pady=5, side='left')
        self.info_label = tk.Label(self.f4)
        self.info_label.pack(padx=5, pady=5, side='left')
        self.root.after(0, self._gui_loop)
        self.root.after(100, self.root.deiconify)  # return visibility after frames loads
        self.root.mainloop()

    def _gui_loop(self):
        t1 = f"Current Ship Position: {self.ship_pos}"
        t2 = f"Next System: {self.next_system}"
        t3 = f"Approx Jumps: {self.remaining}"
        self.remaining = sum([int(x['data'][-1]) for x in self.plot_route_from_csv.values() if x['done'] == 0])
        if t1 != self.lab_ship_pos.cget('text'):
            self.lab_ship_pos.configure(text=t1)
            self.next_system_lab.configure(text=t2)
            self.jumps_re_lab.configure(text=t3)
        if not gui_bridge.gui_started:
            if not self.gui_closed:
                self.gui_closed = True
                self.root.after(0, self.root.withdraw)  # sie musi sam zamykac
                self._ready()
        else:
            self.gui_closed = False
        if self.updating:
            text = 'Loading Local Maps'
            if text != self.info_label.cget('text'):
                self.info_label.configure(text=text)
        if self.update_data_from_process:
            text = 'Local Maps Loaded'
            if text != self.info_label.cget('text'):
                self.info_label.configure(text=text)
            self.update_data_from_process = False
            self.f7.update_tree(self.settings['stored_data'])
        self.check_entry_fields()
        self.window_locker = (GetWindowText(GetForegroundWindow()))
        if 'Elite - Dangerous (CLIENT)' in self.window_locker:
            self.run_script = True
        else:
            self.run_script = False
        if self.comparision_founded and not self.settings['use_cch']:
            self.comparision_founded = False
            self.checked_systems.append(self.ship_pos)
            self.plot_route_from_csv[self.ship_pos]['done'] = 1
            self.remaining = sum([int(x['data'][-1]) for x in self.plot_route_from_csv.values() if x['done'] == 0])
            self._short_presentation()
            self._save_json()
            self.f6.update_tree(self.plot_route_from_csv)
        elif self.comparision_founded and self.settings['use_cch']:
            self.comparision_founded = False
            self.checked_systems.append(self.ship_pos)
            self.cch_route[self.ship_pos]['done'] = 1
            self._short_presentation()
            self._save_json()
        if self.wake_gui or self.start_up:
            self.start_up = False
            self.wake_gui = False
            self.root.deiconify()
        if self.monitoring_route:
            self.monitoring_route = False
            self._check_pos()
        if self.open_commodity:
            self.open_commodity = False
            smart_gui(commodity=self.port, mode=1, parent=self.root, way=self.com_data)
        if self.commodity_error:
            self.commodity_error = False
            smart_gui(mode=5, parent=self.root)
        if self.short_present:
            self.short_present = False
            self._short_presentation()
        if self.check_commodity:
            self.check_commodity = False
            self._set_commodity(self.settings['use_inara'], False)
        if self.settings_gui.c2.boolvar.get():
            if self.custom_event_1 != 0:
                self.custom_event_1 = 0
                self.f2.set_disabled()
                self.f3.set_disabled()
                self.f6.update_tree(self.empty_dict)
                self.f10.update_tree(self.cch_route, self.settings['CCHTC'])
                if self.settings['CCHTC']:
                    self.cch_label.configure(text='Colonia')
                else:
                    self.cch_label.configure(text='Sol')
        else:
            if self.custom_event_1 != 1:
                self.custom_event_1 = 1
                self.f2.set_enabled()
                self.f3.set_enabled()
                self.f6.update_tree(self.plot_route_from_csv)
                self.f10.update_tree(self.empty_dict, self.settings['CCHTC'])
                self.cch_label.configure(text='Switch Checkbox')
        pass
        if self.close_thread:
            smart_gui(cmdr=self.cmdr, parent=self.root)
            self.root.after(3000, self.root.destroy)
            return
        self.root.after(100, self._gui_loop)

    def _close_all(self):
        self.close_thread = True
        if self.key_manager is not None:
            self.key_manager.stop()
        if self.cursor is not None:
            self.cursor.close()
            self.sql.close()
        if self.process is not None:
            if self.process.is_alive:
                self.process.kill()
        exit()

    def _cch_set_to(self):
        if self.settings['use_cch']:
            if self.settings['CCHTC']:
                self.settings['CCHTC'] = False
                self.cch_label.configure(text='Sol')
                temp = [x for x in standard_highway.keys()]
                temp.reverse()
                self.cch_route = {x: standard_highway[x] for x in temp}
                del temp
            else:
                self.settings['CCHTC'] = True
                self.cch_label.configure(text='Colonia')
                self.cch_route = dc(standard_highway)
            self.f10.update_tree(self.cch_route, self.settings['CCHTC'])
            self._save_json()

    def my_sql_connect(self):
        try:
            self.sql = mysql.connector.connect(host='localhost',
                                               user='root',
                                               password=password.my_pass)
            self.cursor = self.sql.cursor(buffered=True)
        except Exception as e:
            self.sql = None
            self.cursor = None
            print(e)

    def pipe_request(self):
        self.processed = 0
        self._once_pipe_loop = threading.Thread(target=self._pipe_loop)
        self._once_pipe_loop.start()

    def _proccess_side_loop(self):
        self.updating = True
        while True:
            if self.process.is_alive():
                try:
                    self.galactic_maps, self.settings['stored_data'] = self.parent_pipe.recv()
                    self.updating = False
                    self.update_data_from_process = True
                except BrokenPipeError:
                    break
                except EOFError:
                    break
            if self.galactic_maps is not None:
                print('MAPS LOADED FROM PIPE')
                break
        self.updating = False

    def _background_loop(self):
        while True:
            if self.run_script:
                self._read_log()
                self._parse_ship_position()
            if self.send_settings:
                self.send_settings = False
                self.tree.fast_close = self.settings['close_clipping']
                self.f6.fast_close = self.settings['close_clipping']
            if self.close_thread:
                break
            time.sleep(0.5)

    def _read_log(self):
        s = self.log_path_is_safe.findall(self.settings['log_path'])
        if s:
            if os.path.exists(self.settings['log_path']):
                log_file = os.listdir(self.settings['log_path'])
                self.newest_log_file = os.path.normpath(os.path.join(self.settings['log_path'], log_file[-1]))
                with open(self.newest_log_file) as read_manager:
                    self.log_content = read_manager.readlines()
                    self.log_content.reverse()
                    read_manager.close()
        pass

    def _parse_ship_position(self):
        ship_founded = False
        for i, line in enumerate(self.log_content):
            search_ship_pos = self.ship_pos_regrex.match(line)

            if search_ship_pos and not ship_founded:
                ship_founded = True
                self.ship_pos = search_ship_pos.groupdict()['current_pos']
            if self.cmdr is None:
                search_cmdr = self.cmdr_regrex.match(line)
                if search_cmdr:
                    self.cmdr = search_cmdr.groupdict()['name']
            if ship_founded and self.cmdr is not None:
                break

    def _run_listener(self):
        print('KEY SHORTCUTS LOADED')
        with Listener(on_press=self._check_pressed, on_release=self._current_key) as self.key_manager:
            self.key_manager.join()

    def _current_key(self, *args):
        self.current_k = str(args[0])

    # noinspection PyTypeChecker
    def _check_pressed(self, *args):
        if str(args[0]) == self.settings['shortcuts']['setting']:
            if gui_bridge.gui_started:
                gui_bridge.gui_started = False
            else:
                gui_bridge.gui_started = True
                self.wake_gui = True
        if str(args[0]) == self.settings['shortcuts']['next'] and not gui_bridge.gui_started:
            self.short_present = True
        if str(args[0]) == self.settings['shortcuts']['shop'] and not gui_bridge.gui_started:
            self.check_commodity = True
        if str(args[0]) == self.settings['shortcuts']['exit'] and not gui_bridge.gui_started:
            self._close_all()

    def _convert_txt(self, text):
        for repl in self.replace_loop:
            text = text.replace(repl, '')
        return text

    def _edit_result(self, pack, way):
        step_1 = [x.text for x in pack]
        stacja = step_1[0].split('|')[0].strip()
        system = self._convert_txt(step_1[0].split('|')[1].strip())
        pad = step_1[1]
        cena = self._convert_txt(step_1[5])
        demand = self._convert_txt(step_1[4])
        updated = step_1[6]
        dystans = self._convert_txt(step_1[3])
        if "2" in way:
            zwrot = [system, stacja, pad, cena, '', demand, '', dystans, updated]
        else:
            zwrot = [system, stacja, pad, '', cena, demand, '', dystans, updated]

        return zwrot

    def _legacy_com(self):
        reorganizacja = {x[3]: y for y, x in self.com_data["last"].items()}
        reorganizacja_ceny = sorted(x for x in reorganizacja.keys())
        reorganizacja_ceny.reverse()
        for price in reorganizacja_ceny[:5]:
            miasto = reorganizacja[price]
            self.drogie[self.com_data['last'][miasto][8]] = self.com_data['last'][miasto]
        reorganizacja = sorted(self.drogie.keys())
        if len(reorganizacja) > 0:
            self.port = self.drogie[reorganizacja[0]]
            pyperclip.copy(self.port[0])
        else:
            self.port = ['Empty results', 'Please change search settings in commodity section', '', 'None', 'None']
        self.open_commodity = True

    def _timelapse(self, datatime):
        s = self.inara_time.findall(datatime)
        num = re.findall('\d+', datatime, re.I)
        numer = [i for i, x in enumerate(s[0]) if len(x) > 0]
        numer = int(numer[0]) if len(numer) > 0 else None
        my_time = 1000000000000000000000000000000000000
        if numer is not None:
            my_time = self.time_recalc[numer] * int(num[0])
        return my_time

    def _inara_com(self):
        if self.com_data["way"] == 'selling':
            reorganizacja = {_recreate(x[3]): y for y, x in self.com_data["last"].items()}
        else:
            reorganizacja = {_recreate(x[4]): y for y, x in self.com_data["last"].items()}
        reorganizacja_ceny = sorted(x for x in reorganizacja.keys())
        if self.com_data["way"] == 'selling':
            reorganizacja_ceny.reverse()
        for price in reorganizacja_ceny[:5]:
            miasto = reorganizacja[price]
            self.drogie[self._timelapse(self.com_data['last'][miasto][8])] = self.com_data['last'][miasto]
        reorganizacja = sorted(self.drogie.keys())
        if len(reorganizacja) > 0:
            self.port = self.drogie[reorganizacja[0]]
            pyperclip.copy(self.port[0])
        else:
            self.port = ['Empty results', 'Please change search settings in commodity section', '', 'None', 'None']
        self.open_commodity = True

    def _check_commodities(self, manual, is_inara, way='0'):
        del self.com_data["last"]
        del self.drogie
        self.com_data["last"] = {}
        self.drogie = {}
        try:
            self.page_content = requests.get(self.link, headers=headers).content
        except Exception as e:
            print(e)
            self.commodity_error = True
            return False
        soup = BeautifulSoup(self.page_content, 'html.parser')
        tablica = soup.select('tbody')
        if len(tablica) == 0:
            self.port = ['Empty results', 'Please change search settings in commodity section', '', 'None', 'None']
            self.open_commodity = True
            return
        for markets in tablica[0].contents:
            # noinspection PyUnresolvedReferences
            coto = markets.contents
            if is_inara:
                lokalna_tablica = self._edit_result(coto, way)
            else:
                lokalna_tablica = [_req(i, coto, x) for i, x in enumerate(coto) if _req(i, coto, x)]
            self.com_data["last"][lokalna_tablica[1]] = lokalna_tablica
        if manual:
            return
        if not is_inara:
            self._legacy_com()
        else:
            self._inara_com()

    def _short_presentation(self):
        self._define_next_system()
        if not self.settings['use_cch']:
            if self.next_system in self.plot_route_from_csv:
                smart_gui(system=self.next_system, d_data=self.plot_route_from_csv[self.next_system],
                          jumps=self.remaining, mode=2, parent=self.root)
            else:
                smart_gui(mode=3, parent=self.root)
        else:
            smart_gui(system=self.next_system, d_data=self.cch_route[self.next_system], mode=4, parent=self.root,
                      way=self.cch_label.cget('text'))

    def _read_json(self):
        with open(self.settings['json_path']) as json_manager:
            self.plot_route_from_csv = json.load(json_manager)
            json_manager.close()
        print("JSON LOADED")

    def _save_json(self):
        if not self.settings['use_cch']:
            correct_name = False
            if self.settings['json_path'] == '':
                name = f"{os.path.splitext(os.path.basename(self.settings['csv_path']))[0]}.json"
                self.settings['json_path'] = name
                correct_name = True
            elif not os.path.isfile(self.settings['json_path']):
                name = f"{os.path.splitext(os.path.basename(self.settings['csv_path']))[0]}.json"
                self.settings['json_path'] = name
                correct_name = True
            elif os.path.isfile(self.settings['json_path']):
                correct_name = True
            if correct_name and self.settings['json_path'] != '.json':
                with open(self.settings['json_path'], 'w') as json_manager:
                    json.dump(self.plot_route_from_csv, json_manager, indent=2)
                    json_manager.close()
                    print(f'PROGRESS SAVED')
            else:
                self.settings['json_path'] = ''
                print(f'PROGRESS NOT SAVED, PLS CHECK PATH')
        else:
            with open(JSON_CCH, 'w') as json_manager:
                json.dump(self.cch_route, json_manager, indent=2)
                json_manager.close()
                print(f'PROGRESS SAVED')

    def _read_csv(self, force=False):
        csv_name = os.path.splitext(os.path.basename(self.settings['csv_path']))[0]
        json_name = os.path.splitext(os.path.basename(self.settings['json_path']))[0]
        if csv_name != json_name or force:
            del self.plot_route_from_csv
            self.plot_route_from_csv = {}
            print('SEARCH CSV')
            if os.path.exists(self.settings['csv_path']):
                print(f'FOUNDED CSV {self.settings["csv_path"]}')
                with open(self.settings['csv_path']) as csv_manager:
                    csv_plot = csv_manager.readlines()
                    csv_plot = csv_plot[2:]
                    csv_manager.close()

                for line in csv_plot:
                    s_line = line.strip().replace('"', '').split(',')
                    self.plot_route_from_csv[s_line[0]] = {'data': s_line[1:], 'done': 0}
                print('PLOT ROUTE COPIED')
            else:
                if os.path.exists(self.settings['json_path']):
                    self._read_json()
                    print('ACTIVE PROGRESS FOUNDED')
        else:
            if os.path.exists(self.settings['json_path']):
                self._read_json()
                print('ACTIVE PROGRESS FOUNDED')
            if len(self.plot_route_from_csv) == 0:
                self._read_csv(True)

    def _pos_to_csv_loop(self):
        print('COMPARE LOOP STARTED')
        while True:
            if self.run_script:
                if not self.settings['use_cch']:
                    if self.ship_pos in self.plot_route_from_csv.keys() and self.ship_pos not in self.checked_systems:
                        self.comparision_founded = True
                    elif self.ship_pos in self.plot_route_from_csv.keys():
                        self.monitoring_route = True
                    elif self.ship_pos not in self.plot_route_from_csv.keys() and self.ship_pos != self.last_system:
                        self.validate_route = False
                else:
                    if self.ship_pos in self.cch_route.keys() and self.ship_pos not in self.checked_systems:
                        self.comparision_founded = True
                    elif self.ship_pos in self.cch_route.keys():
                        self.monitoring_route = True
                    elif self.ship_pos not in self.cch_route.keys() and self.ship_pos != self.last_system:
                        self.validate_route = False
            if self.close_thread:
                break
            time.sleep(0.5)

    def _define_next_system(self):
        if not self.settings['use_cch']:
            for system, values in self.plot_route_from_csv.items():
                if values['done'] == 0:
                    self.next_system = system
                    print(f'NEW SYSTEM DEFINED - {system}')
                    break
                else:
                    self.next_system = system
        else:
            for system, values in self.cch_route.items():
                if values['done'] == 0:
                    self.next_system = system
                    print(f'NEW SYSTEM DEFINED - {system}')
                    break
                else:
                    self.next_system = system
        pyperclip.copy(self.next_system)

    def load_custom_data(self):

        selected_json_data = filedialog.askopenfilename(title='Load Custom Maps', filetypes=[('json files', '*.json')])
        if len(selected_json_data) > 0 and os.path.exists(selected_json_data):
            name_info = os.path.basename(selected_json_data)
            size_info = os.path.getsize(selected_json_data)
            size_info = sizeof_fmt(size_info)
            temp_dict = {'path': selected_json_data, 'in_use': 'No', 'size': size_info,
                         'systems': 'Unknown', 'loaded': 'No'}
            self.settings['stored_data'][name_info] = dc(temp_dict)
            save_config(CONFIG_JSON_FILE, self.settings)
            self.f7.update_tree(self.settings['stored_data'])
            pass

    def _ready(self):
        self.settings['log_path'] = self.f1.e1.get()
        self.settings['csv_path'] = self.f2.e1.get()
        self.settings['json_path'] = self.f3.e1.get()
        self._read_csv()
        self._save_json()
        save_config(CONFIG_JSON_FILE, self.settings)
        gui_bridge.gui_started = False

    def delete_stored(self):
        try:
            # noinspection PyUnresolvedReferences
            key = self.f8.b3.data
            del self.settings['stored_data'][key]
            self.f7.update_tree(self.settings['stored_data'])
            save_config(CONFIG_JSON_FILE, self.settings)
        except Exception as e:
            print(e)

    def _delete(self):
        self.settings['csv_path'] = r''
        self.settings['json_path'] = r''
        self.f2.e1.delete(0, 'end')
        self.f3.e1.delete(0, 'end')
        self._read_csv()
        save_config(CONFIG_JSON_FILE, self.settings)

    def _copy_position(self):
        if self.ship_pos is not None:
            pyperclip.copy(self.ship_pos)
            self.info_label.configure(text=f'Location {self.ship_pos}, copied!')

    # noinspection PyAttributeOutsideInit
    def check_entry_fields(self):
        text1 = self.f2.e1.get()
        text2 = self.f3.e1.get()
        if len(text1) > 0 and len(text2) == 0:
            self.settings['log_path'] = self.f1.e1.get()
            self.settings['csv_path'] = self.f2.e1.get()
            self.settings['json_path'] = self.f3.e1.get()
            self._read_csv()
            self._save_json()
            self.f3.e1.delete(0, 'end')
            self.f3.e1.insert(0, self.settings['json_path'])
            self.f6.update_tree(self.plot_route_from_csv)

    # noinspection PyTypeChecker,PyUnresolvedReferences
    def current_selection(self, event, double=False):
        if double:
            try:
                if self.settings['stored_data'][event.widget.selection()[0]]['in_use'] == 'No':
                    self.settings['stored_data'][event.widget.selection()[0]]['in_use'] = "Yes"
                else:
                    self.settings['stored_data'][event.widget.selection()[0]]['in_use'] = "No"
                self.f7.update_tree(self.settings['stored_data'])
                temp_list = [x['in_use'] for x in self.settings['stored_data'].values()]
                if any('Yes' in x for x in temp_list):
                    self.settings_gui.c1.select.configure(state='normal')
                else:
                    self.settings_gui.c1.boolvar.set(False)
                    self.settings_gui.c1.select.configure(state='disabled')
                    self.settings['use_local_database'] = False
                save_config(CONFIG_JSON_FILE, self.settings)
            except IndexError:
                pass
            except KeyError as e:
                print(e)
        else:
            try:
                item = event.widget.selection()[0]
                self.f8.b3.data = item
                self.f8.b3.configure(state='normal')
            except IndexError:
                self.f8.b3.data = ''
                self.f8.b3.configure(state='disabled')

    def _requested_comm(self):
        REQ_COMMO = self.com_data["what"].upper()
        for number, commodity in self.inara_comm.items():
            COMMO = commodity.upper()
            if REQ_COMMO in COMMO:
                return number
        return False

    def _set_commodity(self, inara_request, emanuel=True):
        way = '0'
        self.com_data["way"] = self.c1.combo.get()
        if inara_request:
            self.com_data["what"] = self.c3.combo.get()
        else:
            self.com_data["what"] = self.c2.combo.get()
        if len(self.e1.entry.get()) > 0:
            self.com_data["ref"] = self.e1.entry.get().replace(' ', '+')
        if inara_request:
            number = self._requested_comm()
            if 'selling' in self.com_data['way']:
                way = '2'
            else:
                way = '1'
            self.link = fr'https://inara.cz/elite/commodities/?pi1={way}&pa1%5B%5D={number}&ps1=' \
                        fr'{self.com_data["ref"]}&pi10=3&pi11=0&pi3=1&pi9=0&pi4=0&pi5=720&pi12=0&pi7=0&pi8=0'
            pass
        else:
            self.link = fr'http://edlegacy.iloveitmore.com.au/?action={self.com_data["way"]}&commodity=' \
                        fr'{self.com_data["what"]}&reference={self.com_data["ref"]}'
        self._check_commodities(emanuel, inara_request, way)
        save_config(LAST_COMMODITY_FILE, self.com_data)
        self.tree.update_tree(self.com_data["last"])

    def _check_pos(self):
        try:
            pos_code = [i for i, x in enumerate(self.plot_route_from_csv.keys()) if self.ship_pos == x][0]
            for i, (_, data) in enumerate(self.plot_route_from_csv.items()):
                if i <= pos_code:
                    data['done'] = 1
                else:
                    data['done'] = 0
            self.continous_path = True
            self.last_system = dc(self.ship_pos)
            self.remaining = sum([int(x['data'][-1]) for x in self.plot_route_from_csv.values() if x['done'] == 0])
            del pos_code
        except IndexError:
            self._validation_route()

    def _validation_route(self):
        try:
            resolve = [i for i, x in enumerate(self.plot_route_from_csv.values()) if x['done'] == 1][-1]
        except IndexError:
            resolve = -1
        for i, (_, data) in enumerate(self.plot_route_from_csv.items()):
            if i <= resolve:
                data['done'] = 1
        self.continous_path = False
        self.last_system = dc(self.ship_pos)
        self.remaining = sum([int(x['data'][-1]) for x in self.plot_route_from_csv.values() if x['done'] == 0])
        del resolve

    def _pipe_loop(self):

        while True:
            if self.settings['use_local_database'] and self.processed == 0:
                self.processed = 1
                self.process = Process(target=Dswedrftgyhuji,
                                       args=(self.child_pipe, self.settings['stored_data'], self.galactic_maps))
                self.process.start()
                threading.Thread(target=self._proccess_side_loop).start()
            if self.processed:
                break
            if self.close_thread:
                break
            time.sleep(0.5)

    def run(self):
        """
        Start all threads
        """
        if os.path.exists(CONFIG_JSON_FILE):
            self.settings = _load_config(CONFIG_JSON_FILE)
            for item, values in self.settings['stored_data'].items():
                values['loaded'] = "No"
        else:
            save_config(CONFIG_JSON_FILE, self.settings)
        if os.path.exists(LAST_COMMODITY_FILE):
            self.com_data = _load_config(LAST_COMMODITY_FILE)
        else:
            save_config(LAST_COMMODITY_FILE, self.com_data)
        if os.path.exists(BOOKMARKS_JSON_FILE):
            self.bookmarks = _load_config(BOOKMARKS_JSON_FILE)
        else:
            save_config(BOOKMARKS_JSON_FILE, self.bookmarks)
        if os.path.exists(INARA):
            self.inara_comm = _load_config(INARA)
        else:
            self.inara_comm = others.refresh_inara_comm()
        if os.path.exists(JSON_CCH):
            self.cch_route = _load_config(JSON_CCH)
        else:
            self.cch_route = dc(standard_highway)
            save_config(JSON_CCH, self.cch_route)
        self._once_pipe_loop.start()
        self._keyboard_thread.start()
        self._log_thread.start()
        if os.path.exists(self.settings['json_path']):
            self._read_json()
        else:
            self._read_csv()
        self._compare_thread.start()
        self._define_next_system()
        self._gui()


if __name__ == '__main__':
    freeze_support()
    plot_route = PlotPyperClip()
    plot_route.run()
