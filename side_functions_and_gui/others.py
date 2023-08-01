import os
import math
import pyperclip
import tkinter as tk
from settings.internal_data import info, headers
import re
import requests
from bs4 import BeautifulSoup
import json
from side_functions_and_gui import gui_bridge


def help_():
    if not os.path.exists('info.txt'):
        with open('info.txt', 'w') as txt_manager:
            txt_manager.write(info)
            txt_manager.close()
    os.startfile('info.txt')


class Smart(tk.Toplevel):

    def __init__(self, parent, my_text):
        super().__init__(parent)
        self.overrideredirect(True)
        self.configure(bg='#0f090f')
        self.wm_attributes("-transparentcolor", "#0f090f")
        self.geometry('%dx%d+%d+%d' % (self.winfo_screenwidth(), self.winfo_screenwidth(), 0, 0))
        self.wm_attributes("-topmost", 1)
        self.wm_attributes("-alpha", 0.9)
        tk.Label(self, text=my_text, font='Arial 18 bold', bg='#030305', fg='#f5af38').pack(fill='both', ipady=10)
        self.after(3000, self.destroy)


# noinspection PyTypeChecker
def smart_gui(commodity='', cmdr='', system='', d_data='', jumps='', mode=0, parent=None, way=None):
    """
    Triggered automatically or manually
    :param way: buying or selling
    :param parent: Main UI ancestor... whatever
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
        if way['way'] == 'selling':
            my_text = f'{way["way"]} {way["what"]} | {commodity[0]} - {commodity[1]} - {commodity[3]} Cr.'
        else:
            my_text = f'{way["way"]} {way["what"]} | {commodity[0]} - {commodity[1]} - {commodity[4]} Cr.'
    elif mode == 2 and isinstance(d_data, dict):
        distance = math.ceil(float(d_data["data"][0]))
        remaining = math.ceil(float(d_data["data"][1]))
        my_text = f'{system} | DISTANCE - {distance} Ly | REMAINING - {remaining} Ly | APPROX JUMPS - {jumps}'
    elif mode == 3:
        my_text = f'SYSTEM NOT DEFINED, SELECT NEW CSV ROUTE.'
    elif mode == 4:
        if 'Sol' in way:
            text = d_data["data"][3].replace("\n", "")
        else:
            text = d_data["data"][4].replace("\n", "")
        my_text = f'Direction to: {way} | {system} | REMAINING - {text} Ly'
    else:
        my_text = f'CONNECTION ERROR.'
    if parent is not None:
        Smart(parent, my_text)


def sel_item_action(event, widget, fast_close, root, double):
    try:
        item = event.widget.selection()[0]
        master_data = event.widget.master.plot[item]
        master = r'.!notebook.!frame4.!bookmarktree' in str(event.widget.master)
        if isinstance(master_data, list):
            pyperclip.copy(master_data[0])
            widget.configure(text=f'Selected Destination: {master_data[0]}')
        else:
            pyperclip.copy(item)
            master_data = item
            widget.configure(text=f'Selected Destination: {master_data}')
        if master:
            event.widget.master.b2.configure(state='normal')
            event.widget.master.b3.configure(state='normal')
        if fast_close and double:
            # event.widget.bind('<Double-1>', 'break')
            root.after(100, root.withdraw)
            gui_bridge.gui_started = False
            return
        pass
    except IndexError:
        master = r'.!notebook.!frame4.!bookmarktree' in str(event.widget.master)
        if master:
            event.widget.master.b2.configure(state='disabled')
            event.widget.master.b3.configure(state='disabled')
    except AttributeError:
        item = event.widget.selection()[0]
        pyperclip.copy(item)
        widget.configure(text=f'Selected Destination: {item}')
        if fast_close and double:
            # event.widget.bind('<Double-1>', 'break')
            root.after(100, root.withdraw)
            return


def sizeof_fmt(num, suffix="B"):
    for unit in ["", "M", "G", "T", "P", "E", "Z"]:
        num /= 1024.0
        if abs(num) < 1024.0:
            return f"{num:3.1f} {unit}{suffix}"


def inara_req():
    link = r'https://inara.cz/elite/commodities/?pi1=2&pa1%5B%5D=81&ps1=Sol&pi10=3&pi11=0&pi' \
           r'3=1&pi9=0&pi4=0&pi5=720&pi12=0&pi7=0&pi8=0'

    cont = requests.get(link).content
    regrex = re.compile(r'^.*value="(?P<nr>\d+)"', re.I)
    soup = BeautifulSoup(cont, 'html.parser')
    tablica = soup.find('select', {"name": "pa1[]"})
    zbiory = {}
    for item in tablica.contents:
        s = regrex.match(str(item))
        zbiory[s.groupdict()['nr']] = item.text
    with open(r'data/internal/inara_result.json', 'w') as j:
        json.dump(zbiory, j, indent=2)
        j.close()


def save_config(path, data):
    with open(path, 'w') as json_manager:
        json.dump(data, json_manager, indent=2)
        json_manager.close()


def refresh_inara_comm():
    link = r'https://inara.cz/elite/commodities/?pi1=2&pa1[]=186&ps1=Sol&pi10=3&pi11=0&pi3=1&pi9=0&pi4=0&pi5=720&pi12=0&pi7=0&pi8=0'
    regrex = re.compile(r'value="([^"]+)"', re.I)
    req = requests.get(link, headers).content
    soup = BeautifulSoup(req, 'html.parser')
    itemki = soup.find("select", {"id": "tokenizeitems"})
    item = itemki.contents
    tablica = {}
    for items in item:
        it = regrex.findall(str(items))
        tablica[it[0]] = items.text

    with open('data/internal/inara_result.json', 'w') as sav:
        json.dump(tablica, sav, indent=2)
        sav.close()
    return tablica