"""
At the beginning it was just a smart copypaste addon for route plotter csv.
Now, I like it and add some features in free time.
Not everything works, some lags exists, soo.. yeah.
TODO:
    - Extended configuration file
    - MySQL requests
    - Pinned Locations with short Notes (I have no idea what I have saved in the tabs in the game)
    - who knows
    - connected or not
    - login client ect.
"""
import os
import tkinter as tk
import webbrowser
from tkinter import ttk
import re
import threading

from pynput.keyboard import Key, Listener
import time
import json
from tkinter import filedialog
import pyperclip
from win32gui import GetWindowText, GetForegroundWindow
from tkinter import TclError
import math
from copy import deepcopy as dc
import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageTk
from ctypes import windll
import gc

windll.shcore.SetProcessDpiAwareness(1)
windll.user32.ShowWindow(windll.kernel32.GetConsoleWindow(), 6)
gc.set_threshold(1, 10, 10)

# import mysql.connector
# import password

info = '''F2 - SETTINGS
F3 - INFO AT THE TOP + COPY DESTINATION
F4 - ROUTE PROGRESS + COPY SELECTED DESTINATION
F5 - COMMODITY + COPY DESTINATION
F6 - SET COMMODITY
F10 - CLOSE APP


LOGS:
ALL LOGS MOSTLY ARE STORED IN: D:\SteamLibrary\steamapps\common\Elite Dangerous\Products\elite-dangerous-64\Logs
IF NOT PLEASE SELECT YOUR DESTINATION PATH   !!!

CSV:
PLEASE VISIT: https://www.spansh.co.uk/plotter/, FILL REQUIRED FIELDS AND DOWNLOAD CSV FILE

JSON:
AUTOMATICALLY CREATES A PATH, IF YOU WANT TO SAVE MULTIPLE PROGRESS, CREATE UNIQUE NAMES'''
products_list = ["advancedcatalysers",
                 "advancedmedicines",
                 "agriculturalmedicines",
                 "agronomictreatment",
                 "alexandrite",
                 "algae",
                 "aluminium",
                 "animalmeat",
                 "animalmonitors",
                 "aquaponicsystems",
                 "articulationmotors",
                 "atmosphericextractors",
                 "autofabricators",
                 "basicmedicines",
                 "basicnarcotics",
                 "battleweapons",
                 "bauxite",
                 "beer",
                 "benitoite",
                 "bertrandite",
                 "beryllium",
                 "bioreducinglichen",
                 "biowaste",
                 "bismuth",
                 "bootlegliquor",
                 "bromellite",
                 "buildingfabricators",
                 "ceramiccomposites",
                 "chemicalwaste",
                 "clothing",
                 "cmmcomposite",
                 "cobalt",
                 "coffee",
                 "coltan",
                 "combatstabilisers",
                 "computercomponents",
                 "conductivefabrics",
                 "consumertechnology",
                 "coolinghoses",
                 "copper",
                 "cropharvesters",
                 "cryolite",
                 "damagedescapepod",
                 "diagnosticsensor",
                 "domesticappliances",
                 "emergencypowercells",
                 "evacuationshelter",
                 "exhaustmanifold",
                 "explosives",
                 "fish",
                 "foodcartridges",
                 "fruitandvegetables",
                 "gallite",
                 "gallium",
                 "geologicalequipment",
                 "gold",
                 "goslarite",
                 "grain",
                 "grandidierite",
                 "hazardousenvironmentsuits",
                 "heatsinkinterlink",
                 "heliostaticfurnaces",
                 "hnshockmount",
                 "hostage",
                 "hydrogenfuel",
                 "hydrogenperoxide",
                 "imperialslaves",
                 "indite",
                 "indium",
                 "insulatingmembrane",
                 "iondistributor",
                 "jadeite",
                 "landmines",
                 "lanthanum",
                 "leather",
                 "lepidolite",
                 "liquidoxygen",
                 "liquor",
                 "lithium",
                 "lithiumhydroxide",
                 "lowtemperaturediamond",
                 "magneticemittercoil",
                 "marinesupplies",
                 "medicaldiagnosticequipment",
                 "metaalloys",
                 "methaneclathrate",
                 "methanolmonohydratecrystals",
                 "microcontrollers",
                 "militarygradefabrics",
                 "mineralextractors",
                 "mineraloil",
                 "modularterminals",
                 "moissanite",
                 "monazite",
                 "musgravite",
                 "mutomimager",
                 "nanobreakers",
                 "naturalfabrics",
                 "neofabricinsulation",
                 "nerveagents",
                 "nonlethalweapons",
                 "occupiedcryopod",
                 "onionheadc",
                 "opal",
                 "osmium",
                 "painite",
                 "palladium",
                 "performanceenhancers",
                 "personaleffects",
                 "personalweapons",
                 "pesticides",
                 "platinum",
                 "polymers",
                 "powerconverter",
                 "powergenerators",
                 "powergridassembly",
                 "powertransferconduits",
                 "praseodymium",
                 "progenitorcells",
                 "pyrophyllite",
                 "radiationbaffle",
                 "reactivearmour",
                 "reinforcedmountingplate",
                 "resonatingseparators",
                 "rhodplumsite",
                 "robotics",
                 "rutile",
                 "samarium",
                 "scrap",
                 "semiconductors",
                 "serendibite",
                 "silver",
                 "skimercomponents",
                 "slaves",
                 "structuralregulators",
                 "superconductors",
                 "surfacestabilisers",
                 "survivalequipment",
                 "syntheticfabrics",
                 "syntheticmeat",
                 "syntheticreagents",
                 "taaffeite",
                 "tantalum",
                 "tea",
                 "telemetrysuite",
                 "terrainenrichmentsystems",
                 "thallium",
                 "thermalcoolingunits",
                 "thorium",
                 "titanium",
                 "tobacco",
                 "tritium",
                 "uraninite",
                 "uranium",
                 "usscargoblackbox",
                 "usscargorareartwork",
                 "water",
                 "waterpurifiers",
                 "wine",
                 "wreckagecomponents",
                 ]


def _help():
    if not os.path.exists('info.txt'):
        with open('info.txt', 'w') as txt_manager:
            txt_manager.write(info)
            txt_manager.close()
    os.startfile('info.txt')


def smart_gui(commodity='', cmdr='', system='', d_data='', jumps='', mode=0):
    """
    Triggered automatically or manually
    TODO:
        - more configurable
    :param mode: with mode is trigerred
    :param cmdr: Your name CMDR
    :param commodity: Information about selected station for traiding
    :param d_data: information about traveled and remaining distance in PlotRoute mode
    :param system: destination system in PlotRoute mode
    :param jumps: info from csv
    """
    if mode == 0:
        my_text = f'GOODBYE, CMDR. {cmdr}'
    elif mode == 1 and isinstance(commodity, list):
        my_text = f'{commodity[0]} - {commodity[1]} - {commodity[2]} Cr.'
    elif mode == 2 and isinstance(d_data, dict):
        distance = math.ceil(float(d_data["data"][0]))
        remaining = math.ceil(float(d_data["data"][1]))
        my_text = f'{system} | DISTANCE - {distance} Ly | REMAINING - {remaining} Ly | APPROX JUMPS - {jumps}'
    elif mode == 3:
        my_text = f'SYSTEM NOT DEFINED, SELECT NEW CSV ROUTE.'
    else:
        my_text = f'CONNECTION ERROR.'
    root = tk.Tk()
    root.overrideredirect(True)
    root.configure(bg='#0f090f')
    root.wm_attributes("-transparentcolor", "#0f090f")
    root.geometry('%dx%d+%d+%d' % (root.winfo_screenwidth(), root.winfo_screenwidth(), 0, 0))
    root.wm_attributes("-topmost", 1)
    root.wm_attributes("-alpha", 0.9)
    tk.Label(root, text=my_text, font='Arial 18 bold', bg='#030305', fg='#f5af38').pack(fill='both', ipady=10)
    root.after(3000, root.destroy)
    root.mainloop()


def _selected_item_action(event, widget):
    try:
        item = event.widget.selection()[0]
        pyperclip.copy(item)
        widget.configure(text=f'Selected Destination: {item}')
    except IndexError:
        pass


label_set = {'side': 'left', 'padx': 10, 'pady': 3}
widget_set = {'side': 'right', 'fill': 'x', 'ipady': 1, 'ipadx': 100, 'padx': 5}
entry_set = {'fill': 'x', 'ipady': 1, 'ipadx': 100, 'padx': 5}
sites = {'Inara': {'link': 'https://inara.cz/elite/news/',
                   'desc': 'THIS WEBSITE IS NOT AN OFFICIAL TOOL FOR THE GAME ELITE: DANGEROUS AND IS NOT '
                           'AFFILIATED WITH FRONTIER DEVELOPMENTS. ALL INFORMATION PROVIDED IS BASED ON '
                           'PUBLICLY AVAILABLE INFORMATION AND MAY NOT BE ENTIRELY ACCURATE.',
                   'image': r'logo\inaralogo.png'},
         'Roguey': {'link': 'https://roguey.co.uk/',
                    'desc': 'Welcome to help section, in here you will find information, guides and more on '
                            'Elite & Dangerous.',
                    'image': r'logo\rogueylogo.png'},
         'CMDR Tollbox': {'link': 'https://cmdrs-toolbox.com/',
                          'desc': 'This site was created to help both new and old players in Elite Dangerous. '
                                  'The site was created by Down To Earth Astronomy.',
                          'image': r'logo\cmdrtoolbox.png'},
         'Spansh - Plotter': {'link': 'https://www.spansh.co.uk/plotter/',
                              'desc': 'This page will allow you to plot between two different star systems. '
                                      'The result will show you every time you need to go to the galaxy map '
                                      'in order to plot a new route '
                                      '(for instance when you are at a neutron star)',
                              'image': r'logo\spanch.png'},
         'ED Legacy (I love it more)': {'link': 'http://edlegacy.iloveitmore.com.au/',
                                        'desc': ' If you are selling, you want a high Sell Price '
                                                'with a high Demand, if you are buying, you want a low Buy '
                                                'Price and a high Supply.',
                                        'image': r'logo\edlegacy.png'},
         'Elite Dangerous Star Map': {'link': 'https://www.edsm.net',
                                      'desc': 'EDSM (Elite Dangerous Star Map) was at first a community effort '
                                              'to store and calculate systems coordinates around the Elite: '
                                              'Dangerous galaxy.It is now the main API used by dozens of '
                                              'software and websites to find systems, coordinates, information '
                                              '(governement, allegiance, faction...) and celestial bodies '
                                              '(types, materials...).',
                                      'image': 'logo\edsmlogo.png'},
         'Coriolis': {'link': 'https://coriolis.io/',
                      'desc': 'Coriolis is a ship bulider for Elite: Dangrous.',
                      'image': 'logo\coriolislogo.png'}
         }


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
        elif event.widget.image == 2:
            if os.path.exists(self.e1.get()):
                self.selected_csv = self.e1.get()
        elif event.widget.image == 3:
            if os.path.exists(self.e1.get()):
                self.selected_route = self.e1.get()

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


class CombinedCombobox(tk.Frame):
    def __init__(self, parent, lista, tekst, current):
        super().__init__(parent)
        f1 = ttk.Frame(parent)
        f1.pack(fill='x')
        ttk.Label(f1, text=tekst, justify='left').pack(label_set)
        self.combo = ttk.Combobox(f1, values=lista, state='readonly', width=50)
        self.combo.set(current)
        self.combo.pack(widget_set)


class CombinedEntry(tk.Frame):

    def __init__(self, parent, ship, text):
        super().__init__(parent)
        self.parent = parent
        self.galactic_maps = {}
        self.ship_pos = ship
        self.f1 = ttk.Frame(parent)
        self.f1.pack(fill='x')
        ttk.Label(self.f1, text=text, justify='left').pack(label_set)
        self.f2 = ttk.Frame(self.f1)
        self.f2.pack(fill='x', side='right')
        self.entry = ttk.Entry(self.f2, width=50)
        self.entry.bind('<KeyRelease>', lambda e: self._request_mysql(e))
        self.entry.bind('<Escape>', lambda e: self.listbox.place_forget())
        try:
            self.entry.insert(0, self.ship_pos)
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

    def _request_mysql(self, event):
        if str(event.keysym) != 'Escape':
            text = event.widget.get()
            command = f"SELECT name FROM ed.powerplay WHERE name REGEXP '^{text}'"
            if len(text) >= 1:
                # plot_route.cursor.execute(command)
                # self.galactic_maps = plot_route.cursor.fetchall()
                for i, item in enumerate(self.galactic_maps):
                    try:
                        # noinspection PyTypeChecker
                        self.galactic_maps[i] = item[0]
                    except Exception as e:
                        print(e)
                if self.galactic_maps is not None:
                    self._check_database()
            else:
                self.galactic_maps = plot_route.galactic_maps
                self._check_database()

    def _check_database(self):
        if len(self.galactic_maps) > 0:
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
            tk.Label(frame, text=link['desc'], justify='left', wraplength=480).pack(side='left', fill='both')
            load_image = Image.open(link['image'])
            load_image.thumbnail((100, 100))
            __image = ImageTk.PhotoImage(load_image)
            img = tk.Label(frame, image=__image)
            img.image = __image
            img.pack(side='right', pady=2)
            img.data = link['link']
            img.bind('<Button-1>', lambda e: _open_website(e, 1))
            ttk.Separator(self, orient='horizontal').pack(fill='x', padx=5)


class SettingWidget(ttk.Frame):
    def __init__(self, parent, text, option):
        super().__init__(parent)
        self.option = option
        self.boolvar = tk.BooleanVar()
        self.select = ttk.Checkbutton(self, text=text, variable=self.boolvar,
                                      command=lambda: self._setvar())
        self.boolvar.set(value=self.option)
        self.select.pack(label_set)
        self.pack(fill='x')

    def _setvar(self):
        self.option = self.boolvar.get()
        pass


class ShortCuts(ttk.Frame):
    def __init__(self, parent, text, option, shortcuts):
        super().__init__(parent)
        ttk.Label(self, text=text, justify='left', width=25).pack(side='left')
        e1 = tk.Label(self, text=shortcuts[option], highlightbackground='grey', highlightthickness=1,
                      width=10, anchor='e', bg='white')
        e1.bind('<Motion>', lambda e: self._on_motion(e, 1))
        e1.bind('<Button-1>', lambda e: self._set_clicked(e, 1))
        e1.bind('<Double-1>', lambda e: self._set_clicked(e, 2))
        e1.bind('<Leave>', lambda e: self._on_motion(e, 0))
        e1.bind('<Key>', lambda e: self._validate(e))
        e1.pack(side='left')
        e1.clicked = False
        e1.selected = False
        self.shortcuts = shortcuts
        self.option = option
        self.pack(fill='x', padx=10, pady=2)

    def _validate(self, event):
        if event.widget.selected:
            key = str(event.keysym).upper()
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
        SettingWidget(self, text='Use local database (json)', option=plot_route.use_local_database)
        ttk.Separator(self, orient='horizontal').pack(fill='x', padx=5, pady=2)
        ShortCuts(self, text='Open Smart ED', shortcuts=plot_route.shortcuts, option='setting')
        ShortCuts(self, text='Copy Next PyPlotter', shortcuts=plot_route.shortcuts, option='next')
        ShortCuts(self, text='Copy Best Commodities', shortcuts=plot_route.shortcuts, option='shop')
        ShortCuts(self, text='Exit App', shortcuts=plot_route.shortcuts, option='exit')


class PlotPyperClip:

    def __init__(self):
        self.log_path = r''
        self.csv_path = r''
        self.json_path = r''
        self.cmdr = None
        self.ship_pos_regrex = re.compile(r'^\{.*}\s*System:"(?P<current_pos>.*)"\s*StarPos:.*', re.I)
        self.cmdr_regrex = re.compile(r'^.*UID=\d+\s*name=(?P<name>.*)', re.I)
        self._log_thread = threading.Thread(target=self._background_loop)
        self._keyboard_thread = threading.Thread(target=self._run_listener)
        self._compare_thread = threading.Thread(target=self._pos_to_csv_loop)
        self.header = ["System Name", "Distance To Arrival", "Distance Remaining", "Neutron Star", "Jumps"]
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
                                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        self.plot_route_from_csv = {}
        self.checked_systems = []
        self.interests = [1, 1, 0, 1, 0, 0, 0, 0, 1]
        self.shortcuts = {'setting': 'F2',
                          'next': 'F3',
                          'shop': 'F4',
                          'exit': 'F10'}
        self.ship_pos = None
        self.comparision_founded = False
        self.newest_log_file = ''
        self.log_content = ''
        self.next_system = ''
        self.wake_gui = False
        self.monitoring_route = False
        self.validate_route = False
        self.continous_path = False
        self.last_system = ''
        self.run_script = False
        self.remaining = None
        self.close_thread = False
        self.key_manager = None
        self.use_local_database = True
        self.zbior = {}
        self.drogie = {}
        self.open_commodity = False
        self.commodity_error = False
        self.check_commodity = False
        self.port = ''
        self.galactic_maps = {}
        self.galactic_maps_list = []
        self.what = ['selling', 'buying']
        self.sell_or_buy = 'selling'
        self.commodity = 'platinum'
        self.reference = 'omicron+capricorni+b'
        self.link = fr'http://edlegacy.iloveitmore.com.au/?action=' \
                    fr'{self.sell_or_buy}&commodity={self.commodity}&reference={self.reference}'
        # self.sql = mysql.connector.connect(host='localhost',
        #                                    user='root',
        #                                    password=password.my_pass)
        # self.cursor = self.sql.cursor(buffered=True)

    def _close_all(self):
        self.close_thread = True
        if self.key_manager is not None:
            self.key_manager.stop()
        # self.cursor.close()
        # self.sql.close()
        smart_gui(cmdr=self.cmdr)
        exit()

    def _before_startup(self):
        print('START UP')
        r = False
        if not os.path.exists(r'config.json'):
            print('CONFIG FILE REQUEST')
            self._gui()
            r = True
        else:
            self._load_config()
        if not r:
            self._gui()

    def _background_loop(self):
        print('LOG LOOP STARTED')
        while True:
            if self.run_script:
                self._read_log()
                self._parse_ship_position()
            if self.close_thread:
                break
            time.sleep(0.5)

    def _read_log(self):  #
        if os.path.exists(self.log_path):
            log_file = os.listdir(self.log_path)
            self.newest_log_file = os.path.normpath(os.path.join(self.log_path, log_file[-1]))
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
        with Listener(on_press=self._check_pressed) as self.key_manager:
            self.key_manager.join()

    def _check_pressed(self, *args):
        """TODO:
            - when gui opened prevent this actions"""
        if args[0] == Key.f2:
            self.wake_gui = True
        if args[0] == Key.f3:
            self._short_presentation()
        if args[0] == Key.f4:
            self.check_commodity = True
        if args[0] == Key.f10:
            self._close_all()

    def _req(self, i, zbior, element):
        if self.interests[i]:
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
        try:
            self.page_content = requests.get(self.link, headers=self.headers).content
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
            self.zbior[lokalna_tablica[2]] = lokalna_tablica
        reorganizacja = sorted(self.zbior.keys())
        reorganizacja.reverse()
        for price in reorganizacja[:5]:
            self.drogie[self.zbior[price][3]] = self.zbior[price]
        reorganizacja = sorted(self.drogie.keys())
        self.port = self.drogie[reorganizacja[0]]
        pyperclip.copy(self.port[0])
        self.open_commodity = True
        pass

    def _short_presentation(self):
        self._define_next_system()
        if self.next_system in self.plot_route_from_csv:
            smart_gui(system=self.next_system, d_data=self.plot_route_from_csv[self.next_system],
                      jumps=self.remaining, mode=2)
        else:
            smart_gui(mode=3)

    def _read_json(self):
        with open(self.json_path) as json_manager:
            self.plot_route_from_csv = json.load(json_manager)
            json_manager.close()
        print("JSON LOADED")

    def _save_json(self):
        correct_name = False
        if self.json_path == '':
            name = f"{os.path.splitext(os.path.basename(self.csv_path))[0]}.json"
            self.json_path = name
            correct_name = True
        elif not os.path.isfile(self.json_path):
            name = f"{os.path.splitext(os.path.basename(self.csv_path))[0]}.json"
            self.json_path = name
            correct_name = True
        elif os.path.isfile(self.json_path):
            correct_name = True
        if correct_name and self.json_path != '.json':
            with open(self.json_path, 'w') as json_manager:
                json.dump(self.plot_route_from_csv, json_manager, indent=2)
                json_manager.close()
                print(f'PROGRESS SAVED')
        else:
            self.json_path = ''
            print(f'PROGRESS NOT SAVED, PLS CHECK PATH')

    def _read_csv(self, force=False):
        csv_name = os.path.splitext(os.path.basename(self.csv_path))[0]
        json_name = os.path.splitext(os.path.basename(self.json_path))[0]
        if csv_name != json_name or force:
            del self.plot_route_from_csv
            self.plot_route_from_csv = {}
            print('SEARCH CSV')
            if os.path.exists(self.csv_path):
                print(f'FOUNDED CSV {self.csv_path}')
                with open(self.csv_path) as csv_manager:
                    csv_plot = csv_manager.readlines()
                    csv_plot = csv_plot[2:]
                    csv_manager.close()

                for line in csv_plot:
                    s_line = line.strip().replace('"', '').split(',')
                    self.plot_route_from_csv[s_line[0]] = {'data': s_line[1:], 'done': 0}
                print('PLOT ROUTE COPIED')
            else:
                if os.path.exists(self.json_path):
                    self._read_json()
                    print('ACTIVE PROGRESS FOUNDED')
        else:
            if os.path.exists(self.json_path):
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

    def _load_config(self):
        with open('config.json') as json_manager:
            pack = json.load(json_manager)
            self.log_path = pack[0]
            self.csv_path = pack[1]
            self.json_path = pack[2]
        print('CONFIG FILE LOADED')
        print(f'CURRENT SETUP:\n\t-LOG\t{self.log_path}\n\t-CSV\t{self.csv_path}\n\t-JSON\t{self.json_path}')

    def _save_config(self):
        pack = [self.log_path, self.csv_path, self.json_path]
        with open('config.json', 'w') as json_manager:
            json.dump(pack, json_manager, indent=2)
            json_manager.close()
        print('NEW CONFIGURATION SAVED')

    def _ready(self):
        self.log_path = self.f1.e1.get()
        self.csv_path = self.f2.e1.get()
        self.json_path = self.f3.e1.get()
        self._read_csv()
        self._save_json()
        self._save_config()
        self.root.destroy()
        print(f'CURRENT SETUP:\n\t-LOG\t{self.log_path}\n\t-CSV\t{self.csv_path}\n\t-JSON\t{self.json_path}')

    def _delete(self):
        self.csv_path = r''
        self.json_path = r''
        self.f2.e1.delete(0, 'end')
        self.f3.e1.delete(0, 'end')
        self._read_csv()
        self._save_config()

    # noinspection PyAttributeOutsideInit
    def _gui(self):
        self.root = tk.Tk()
        self.root.iconbitmap(r'favicon.ico')
        self.root.attributes('-topmost', 1)
        self.root.title('Smart ED Legacy')
        self.root.resizable(False, False)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(padx=10, fill='both')

        self.ntbkf_1 = ttk.Frame(self.notebook)
        self.f1 = CombinedMenu(self.ntbkf_1, 'Select Log Folder', 1, self.log_path)
        self.f1.pack()
        self.f2 = CombinedMenu(self.ntbkf_1, 'Select CSV File', 2, self.csv_path)
        self.f2.pack()
        self.f3 = CombinedMenu(self.ntbkf_1, 'Select JSON  Neutron Route', 3, self.json_path)
        self.f3.pack()
        ttk.Separator(self.ntbkf_1, orient='horizontal').pack(fill='x', padx=5, pady=2)
        self.settings_gui = PartSettingFrame(self.ntbkf_1)
        self.settings_gui.pack(fill='x')
        self.ntbkf_1.pack(fill='x')

        self.ntbkf_2 = ttk.Frame(self.notebook)
        self.e1 = CombinedEntry(self.ntbkf_2, self.ship_pos, 'Select Start System')
        self.e1.pack(fill='x')
        self.c1 = CombinedCombobox(self.ntbkf_2, self.what, 'Action', self.sell_or_buy)
        self.c1.pack(fill='x')
        self.c2 = CombinedCombobox(self.ntbkf_2, products_list, 'Product', self.commodity)
        self.f5 = ttk.Frame(self.ntbkf_2)
        self.f5.pack(fill='both')
        self.button = ttk.Button(self.f5, text='Check Best Price (Legacy)', command=self._set_commodity)
        self.button.pack(padx=5, pady=3, side='right')
        self.ntbkf_2.pack()

        self.ntbkf_3 = ttk.Frame(self.notebook)
        ttk.Label(self.root, text=f"Current Ship Position: {self.ship_pos}", justify='left').pack(fill='x', padx=10,
                                                                                                  ipady=5)
        ttk.Label(self.ntbkf_3, text=f"Next System: {self.next_system}", justify='left').pack(fill='x', padx=10,
                                                                                              ipady=5)
        ttk.Label(self.ntbkf_3, text=f"Approx Jumps: {self.remaining}", justify='left').pack(fill='x', padx=10, ipady=5)
        label1 = ttk.Label(self.ntbkf_3, text='Selected Destination:', justify='left')
        label1.pack(fill='x', padx=10, ipady=5)
        columns = {0: 'No', 1: 'System Name', 2: 'Distance', 3: 'Remaining', 4: 'Jumps Required', 5: 'System Visited'}
        column_size = [30, 200, 120, 100, 100]
        row_no = [x for x, _ in columns.items()]
        treeview = ttk.Treeview(self.ntbkf_3, show='tree headings', columns=str(row_no), style="Mystyle.Treeview")
        treeview.pack(side='left', fill='both', padx=1, pady=5)
        verscrlbar = ttk.Scrollbar(self.ntbkf_3, orient="vertical", command=treeview.yview)
        verscrlbar.pack(side='left', fill='y', padx=1, pady=5)
        treeview.configure(height=20, yscrollcommand=verscrlbar.set)
        treeview.column('#0', width=0)
        [treeview.heading(x, text=y, anchor='w') for x, y in columns.items()]
        [treeview.column(i, width=x, anchor='w') for i, x in enumerate(column_size)]
        treeview.bind('<ButtonRelease-1>', lambda g: _selected_item_action(g, label1))
        for i, (parent, values) in enumerate(self.plot_route_from_csv.items()):
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
        self.b3 = ttk.Button(self.f4, text='Help', command=_help)
        self.b3.pack(padx=5, pady=5, side='left')
        self.root.mainloop()

    def _set_commodity(self):
        self.sell_or_buy = self.c1.combo.get()
        self.commodity = self.c2.combo.get()
        if len(self.e1.entry.get()) > 0:
            self.reference = self.e1.entry.get().replace(' ', '+')
        self.link = fr'http://edlegacy.iloveitmore.com.au/?action=' \
                    fr'{self.sell_or_buy}&commodity={self.commodity}&reference={self.reference}'

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
            if self.wake_gui:
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

    def _load_maps(self):
        with open(r'powerPlay.json') as maps:
            self.galactic_maps_list = json.load(maps)
            self.galactic_maps = [x['name'] for x in self.galactic_maps_list]
            del self.galactic_maps_list
            maps.close()

    def _load_galactic_maps(self):
        threading.Thread(target=self._load_maps).start()

    def run(self):
        """
        Start all threads
        """
        self._load_galactic_maps()  # this one need to be replaced with MySQL
        self._before_startup()
        self._log_thread.start()
        self._keyboard_thread.start()
        if os.path.exists(self.json_path):
            self._read_json()
        else:
            self._read_csv()
        self._compare_thread.start()
        self._define_next_system()
        self._main_loop()


if __name__ == '__main__':
    plot_route = PlotPyperClip()
    plot_route.run()
