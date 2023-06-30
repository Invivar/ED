"""
At the beginning it was just a smart copypaste addon for route plotter csv.
Now, I like it and add some features in free time.
Not everything works, some lags exists, soo.. yeah.
TODO:
    - Extended configuration file
    - save from request
    - MySQL requests
    - Pinned Locations with short Notes (I have no idea what I have saved in the tabs in the game)
    - connected or not
    - login client ect.
"""
import os, re, threading
from tkinter import TclError
from pynput.keyboard import Listener
import time, json
from json.decoder import JSONDecodeError
import pyperclip
from win32gui import GetWindowText, GetForegroundWindow
from copy import deepcopy as dc
import requests, gc
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
from side_functions_and_gui.others import help, smart_gui
import mysql.connector, password

windll.shcore.SetProcessDpiAwareness(1)
windll.user32.ShowWindow(windll.kernel32.GetConsoleWindow(), 6)
gc.set_threshold(1, 10, 10)


class SettingWidget(ttk.Frame):
    def __init__(self, parent, text, option):
        print(parent, text, option)
        super().__init__(parent)
        self.boolvar = tk.BooleanVar()
        self.select = ttk.Checkbutton(self, text=text, variable=self.boolvar,
                                      command=lambda: self._setvar(option))
        self.boolvar.set(value=plot_route.settings[option])
        self.select.pack(label_set)
        self.pack(fill='x')

    def _setvar(self, opt):
        plot_route.settings[opt] = self.boolvar.get()
        plot_route.send_settings = True
        pass


class ShortCuts(tk.Frame):
    def __init__(self, parent, text, option, shortcuts):
        super().__init__(parent)

        ttk.Label(self, text=text, justify='left', width=25).pack(side='left')
        e1 = tk.Label(self, text=shortcuts[option], highlightbackground='grey', highlightthickness=1,
                      width=10, anchor='e', bg='white')
        e1.bind('<Motion>', lambda e: self._on_motion(e, 1))
        e1.bind('<Button-1>', lambda e: self._set_clicked(e, 1))
        e1.bind('<Double-1>', lambda e: self._set_clicked(e, 2))
        e1.bind('<Leave>', lambda e: self._on_motion(e, 0))
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
                """CHECKPOINT - CONNECT RESULTS TO CONFIG"""

    def _set_clicked(self, event, mode):
        if mode == 1:
            event.widget.clicked = True
            event.widget.focus_set()
            event.widget.configure(highlightbackground='#6433FF')
        elif mode == 2:
            event.widget.configure(bg='#FCFFB7', text='<BindKey>', anchor='center')
            event.widget.grab_set()
            event.widget.selected = True

    def _on_motion(self, event, _in):
        if _in:
            if not event.widget.clicked:
                event.widget.configure(highlightbackground='black')
            else:
                event.widget.configure(highlightbackground='#6433FF')
        else:
            event.widget.configure(highlightbackground='grey')
            event.widget.clicked = False


class PartSettingFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        SettingWidget(self, text='Use local database (json)', option='use_local_database')
        SettingWidget(self, text='Close after double click location', option='close_clipping')
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
        self.f2 = ttk.Frame(self.f1)
        self.f2.pack(fill='x', side='right')
        self.entry = ttk.Entry(self.f2, width=50)
        self.entry.bind('<KeyRelease>', lambda e: self.request_from(e))
        self.entry.bind('<Escape>', lambda e: self.listbox.place_forget())
        try:
            self.entry.insert(0, self.reference.replace('+', ' '))
        except TclError:
            pass
        self.entry.pack(entry_set)
        self.listbox = tk.Listbox(parent, relief='flat', width=200, height=100)
        self.scroll = ttk.Scrollbar(self.listbox, command=self.listbox.yview)
        self.listbox.configure(yscrollcommand=self.scroll.set)
        self.listbox.bind('<Return>', lambda e: self._check_selection(e))
        self.listbox.bind('<Double-Button-1>', lambda e: self._check_selection(e))
        self.listbox.bind('<Escape>', lambda e: self.listbox.place_forget())

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


class PlotPyperClip:

    def __init__(self):

        self.parent_pipe, self.child_pipe = Pipe()

        self.ship_pos_regrex = re.compile(r'^\{.*}\s*System:"(?P<current_pos>.*)"\s*StarPos:.*', re.I)
        self.cmdr_regrex = re.compile(r'^.*UID=\d+\s*name=(?P<name>.*)', re.I)

        self._log_thread = threading.Thread(target=self._background_loop)
        self._keyboard_thread = threading.Thread(target=self._run_listener)
        self._compare_thread = threading.Thread(target=self._pos_to_csv_loop)
        self._once_pipe_loop = threading.Thread(target=self._pipe_loop)

        self.header = ["System Name", "Distance To Arrival", "Distance Remaining", "Neutron Star", "Jumps"]
        self.checked_systems = []
        self.interests = [1, 1, 0, 1, 0, 0, 0, 0, 1]

        self.newest_log_file = ''
        self.log_content = ''
        self.next_system = ''
        self.port = ''
        self.last_system = ''
        self.current_k = ''
        self.com_data = {'way': 'selling',
                         'what': 'platinum',
                         'ref': 'omicron+capricorni+b',
                         'last': {}}
        self.link = fr'http://edlegacy.iloveitmore.com.au/?action=' \
                    fr'{self.com_data["way"]}&commodity={self.com_data["what"]}&reference={self.com_data["ref"]}'

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

        self.processed = 0

        self.galactic_maps = {}
        self.zbior = {}
        self.drogie = {}
        self.plot_route_from_csv = {}
        self.settings = {'log_path': '',
                         'csv_path': '',
                         'json_path': '',
                         'shortcuts': {'setting': 'Key.f2',
                                       'next': 'Key.f3',
                                       'shop': 'Key.f4',
                                       'exit': 'Key.f10'},
                         'use_local_database': False,
                         'close_clipping': False}

    def _close_all(self):
        self.close_thread = True
        if self.key_manager is not None:
            self.key_manager.stop()
        # self.cursor.close()
        # self.sql.close()
        smart_gui(cmdr=self.cmdr)
        exit()

    def _proccess_side_loop(self):
        while True:
            if self.process.is_alive():
                try:
                    self.galactic_maps = self.parent_pipe.recv()
                except BrokenPipeError:
                    break
                except EOFError:
                    break
            if self.galactic_maps is not None:
                print('MAPS LOADED FROM PIPE')
                break

    def _background_loop(self):
        print('LOG LOOP STARTED')
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

    def _read_log(self):  #
        if os.path.exists(self.settings['log_path']):
            log_file = os.listdir(self.settings['log_path'])
            self.newest_log_file = os.path.normpath(os.path.join(self.settings['log_path'], log_file[-1]))
            with open(self.newest_log_file, 'r') as read_manager:
                self.log_content = read_manager.readlines()
                self.log_content.reverse()
                read_manager.close()

    def _parse_ship_position(self):  #
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

    def _check_pressed(self, *args):
        if str(args[0]) == self.settings['shortcuts']['setting'] and not self.gui_started:
            self.wake_gui = True
        if str(args[0]) == self.settings['shortcuts']['next']:
            self._short_presentation()
        if str(args[0]) == self.settings['shortcuts']['shop'] and not self.gui_started:
            self.check_commodity = True
        if str(args[0]) == self.settings['shortcuts']['exit'] and not self.gui_started:
            self._close_all()

    def _req(self, i, zbior, element, full_request=True):
        if self.interests[i] or full_request:
            if i + 1 != len(zbior):
                if i == 3:
                    return int(element.text)
                else:
                    return str(element.text).strip()
            else:
                return int(str(time.time()).split('.')[0]) - int(element.attrs['data-sort'])
        else:
            return False

    def _check_commodities(self):
        del self.com_data["last"]
        self.com_data["last"] = {}
        try:
            self.page_content = requests.get(self.link, headers=headers).content
        except Exception as e:
            print(e)
            self.commodity_error = True
            return False
        soup = BeautifulSoup(self.page_content, 'html.parser')
        tablica = soup.select('tbody')
        for markets in tablica[0].contents:
            # noinspection PyUnresolvedReferences
            coto = markets.contents
            lokalna_tablica = [self._req(i, coto, x) for i, x in enumerate(coto) if self._req(i, coto, x)]
            self.com_data["last"][lokalna_tablica[3]] = lokalna_tablica
        reorganizacja = sorted(self.com_data["last"].keys())
        reorganizacja.reverse()
        for price in reorganizacja[:5]:
            self.drogie[self.com_data["last"][price][3]] = self.com_data["last"][price]
        reorganizacja = sorted(self.drogie.keys())
        self.port = self.drogie[reorganizacja[0]]
        pyperclip.copy(self.port[0])
        self.open_commodity = True

    def _short_presentation(self):
        self._define_next_system()
        if self.next_system in self.plot_route_from_csv:
            smart_gui(system=self.next_system, d_data=self.plot_route_from_csv[self.next_system],
                      jumps=self.remaining, mode=2)
        else:
            smart_gui(mode=3)

    def _read_json(self):
        with open(self.settings['json_path']) as json_manager:
            self.plot_route_from_csv = json.load(json_manager)
            json_manager.close()
        print("JSON LOADED")

    def _save_json(self):
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
                if self.ship_pos in self.plot_route_from_csv.keys() and self.ship_pos not in self.checked_systems:
                    self.comparision_founded = True
                elif self.ship_pos in self.plot_route_from_csv.keys():
                    self.monitoring_route = True
                elif self.ship_pos not in self.plot_route_from_csv.keys() and self.ship_pos != self.last_system:
                    self.validate_route = False
            if self.close_thread:
                break
            time.sleep(0.5)

    def _define_next_system(self):

        for system, values in self.plot_route_from_csv.items():
            if values['done'] == 0:
                self.next_system = system
                print(f'NEW SYSTEM DEFINED - {system}')
                break
            else:
                self.next_system = system
        pyperclip.copy(self.next_system)

    def _load_config(self, path):
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

    def _save_config(self, path, data):
        with open(path, 'w') as json_manager:
            json.dump(data, json_manager, indent=2)
            json_manager.close()
        print('NEW CONFIGURATION SAVED')

    def _ready(self):
        self.settings['log_path'] = self.f1.e1.get()
        self.settings['csv_path'] = self.f2.e1.get()
        self.settings['json_path'] = self.f3.e1.get()
        self._read_csv()
        self._save_json()
        self._save_config(CONFIG_JSON_FILE, self.settings)
        self.root.destroy()

    def _delete(self):
        self.settings['csv_path'] = r''
        self.settings['json_path'] = r''
        self.f2.e1.delete(0, 'end')
        self.f3.e1.delete(0, 'end')
        self._read_csv()
        self._save_config(CONFIG_JSON_FILE, self.settings)

    # noinspection PyAttributeOutsideInit
    def _gui(self):
        self.gui_started = True
        self.root = tk.Tk()
        self.root.iconbitmap(r'favicon.ico')
        self.root.attributes('-topmost', 1)
        self.root.title('Smart ED Legacy')
        self.root.resizable(False, False)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(padx=10, fill='both')

        self.ntbkf_1 = ttk.Frame(self.notebook)
        self.f1 = CombinedMenu(self.ntbkf_1, 'Select Log Folder', 1, self.settings['log_path'])
        self.f1.pack()
        self.f2 = CombinedMenu(self.ntbkf_1, 'Select CSV File', 2, self.settings['csv_path'])
        self.f2.pack()
        self.f3 = CombinedMenu(self.ntbkf_1, 'Select JSON  Neutron Route', 3, self.settings['json_path'])
        self.f3.pack()
        ttk.Separator(self.ntbkf_1, orient='horizontal').pack(fill='x', padx=5, pady=2)
        self.settings_gui = PartSettingFrame(self.ntbkf_1)
        self.settings_gui.pack(fill='x')
        self.ntbkf_1.pack(fill='x')

        self.ntbkf_2 = ttk.Frame(self.notebook)
        self.e1 = CombinedEntry(self.ntbkf_2, self.com_data["ref"], 'Select Start System')
        self.e1.pack(fill='x')
        self.c1 = CombinedCombobox(self.ntbkf_2, what, 'Action', self.com_data["way"])
        self.c1.pack(fill='x')
        self.c2 = CombinedCombobox(self.ntbkf_2, products_list, 'Product', self.com_data["what"])
        self.f5 = ttk.Frame(self.ntbkf_2)
        self.f5.pack(fill='both')
        self.button = ttk.Button(self.f5, text='Check Best Price (Legacy)', command=self._set_commodity)
        self.button.pack(padx=5, pady=3, side='right')
        self.tree = CommodityTree(self.ntbkf_2, self.com_data["last"], self.settings['close_clipping'], self.root)
        self.tree.pack(fill='both')
        self.ntbkf_2.pack()

        self.ntbkf_3 = ttk.Frame(self.notebook)
        ttk.Label(self.root, text=f"Current Ship Position: {self.ship_pos}", justify='left').pack(fill='x', padx=10,
                                                                                                  ipady=5)
        ttk.Label(self.ntbkf_3, text=f"Next System: {self.next_system}", justify='left').pack(fill='x', padx=10,
                                                                                              ipady=5)
        ttk.Label(self.ntbkf_3, text=f"Approx Jumps: {self.remaining}", justify='left').pack(fill='x', padx=10, ipady=5)
        self.f6 = PlotTree(self.ntbkf_3, self.plot_route_from_csv, self.settings['close_clipping'], self.root)
        self.f6.pack(fill='both')
        self.ntbkf_3.pack()

        self.ntbkf_4 = ttk.Frame(self.notebook)
        self.ntbkf_4.pack()

        self.ntbkf_5 = ttk.Frame(self.notebook)
        self.shortcut_frame = CombinedFrame(self.ntbkf_5)
        self.shortcut_frame.pack(fill='both')
        self.ntbkf_5.pack()

        self.notebook.add(self.ntbkf_1, text='Settings')
        self.notebook.add(self.ntbkf_2, text='Commodity')
        self.notebook.add(self.ntbkf_3, text='Current Travel')
        self.notebook.add(self.ntbkf_4, text='Bookmarks')
        self.notebook.add(self.ntbkf_5, text='Usefull Sites')

        self.f4 = ttk.Frame(self.root)
        self.f4.pack(fill='both')
        self.b1 = ttk.Button(self.f4, text='OK', command=self._ready)
        self.b1.pack(padx=5, pady=5, side='right')
        self.b2 = ttk.Button(self.f4, text='Finish JSON & CSV', command=self._delete)
        self.b2.pack(padx=5, pady=5, side='right')
        self.b3 = ttk.Button(self.f4, text='Help', command=help)
        self.b3.pack(padx=5, pady=5, side='left')
        self.root.mainloop()
        self.gui_started = False

    def _set_commodity(self):
        self.com_data["way"] = self.c1.combo.get()
        self.com_data["what"] = self.c2.combo.get()
        if len(self.e1.entry.get()) > 0:
            self.com_data["ref"] = self.e1.entry.get().replace(' ', '+')
        self.link = fr'http://edlegacy.iloveitmore.com.au/?action=' \
                    fr'{self.com_data["way"]}&commodity={self.com_data["what"]}&reference={self.com_data["ref"]}'
        self._check_commodities()
        self._save_config(LAST_COMMODITY_FILE, self.com_data)
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
        try:
            self.sql = mysql.connector.connect(host='localhost',
                                               user='root',
                                               password=password.my_pass)
            self.cursor = self.sql.cursor(buffered=True)
        except Exception as e:
            self.sql = None
            self.cursor = None
            print(e)
        while True:
            if self.settings['use_local_database'] and self.processed == 0:
                self.processed = 1
                self.process = Process(target=Dswedrftgyhuji, args=(self.child_pipe,))  # Frustration
                self.process.start()
                threading.Thread(target=self._proccess_side_loop).start()
            if self.processed:
                break
            time.sleep(0.5)

    def _main_loop(self):
        print("MAIN LOOP STARTED")
        self.remaining = sum([int(x['data'][-1]) for x in self.plot_route_from_csv.values() if x['done'] == 0])
        while True:
            self.window_locker = (GetWindowText(GetForegroundWindow()))
            if 'Elite - Dangerous (CLIENT)' in self.window_locker:
                self.run_script = True
            else:
                self.run_script = True
            if self.comparision_founded:
                self.comparision_founded = False
                self.checked_systems.append(self.ship_pos)
                self.plot_route_from_csv[self.ship_pos]['done'] = 1
                self.remaining = sum([int(x['data'][-1]) for x in self.plot_route_from_csv.values() if x['done'] == 0])
                self._short_presentation()
                self._save_json()
            if self.wake_gui or self.start_up:
                self.start_up = False
                self.wake_gui = False
                self.run_script = False
                self._gui()
            if self.monitoring_route:
                self.monitoring_route = False
                self._check_pos()
            if self.open_commodity:
                self.open_commodity = False
                smart_gui(commodity=self.port, mode=1)
            if self.commodity_error:
                self.commodity_error = False
                smart_gui(mode=4)
            if self.check_commodity:
                self.check_commodity = False
                self._check_commodities()
            if self.close_thread:
                break

            time.sleep(0.5)

    def run(self):
        """
        Start all threads
        """
        if os.path.exists(CONFIG_JSON_FILE):
            self.settings = self._load_config(CONFIG_JSON_FILE)
        else:
            self._save_config(CONFIG_JSON_FILE, self.settings)
        if os.path.exists(LAST_COMMODITY_FILE):
            self.com_data = self._load_config(LAST_COMMODITY_FILE)
        else:
            self._save_config(LAST_COMMODITY_FILE, self.com_data)
        self._once_pipe_loop.start()
        self._keyboard_thread.start()
        self._log_thread.start()
        if os.path.exists(self.settings['json_path']):
            self._read_json()
        else:
            self._read_csv()
        self._compare_thread.start()
        self._define_next_system()
        self._main_loop()


if __name__ == '__main__':
    freeze_support()
    plot_route = PlotPyperClip()
    plot_route.run()
