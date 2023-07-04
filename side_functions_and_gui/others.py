import os, math, pyperclip
import tkinter as tk
from settings.internal_data import info
import re
import requests
from bs4 import BeautifulSoup
import json


def help_():
    if not os.path.exists('info.txt'):
        with open('info.txt', 'w') as txt_manager:
            txt_manager.write(info)
            txt_manager.close()
    os.startfile('info.txt')


def smart_gui(commodity='', cmdr='', system='', d_data='', jumps='', mode=0):
    """
    Triggered automatically or manually
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
        my_text = f'{commodity[0]} - {commodity[1]} - {commodity[3]} Cr.'
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


def sel_item_action(event, widget, fast_close, root, double):
    try:
        item = event.widget.selection()[0]
        master_data = event.widget.master.plot[item]  # lol
        pyperclip.copy(master_data[0])
        if fast_close and double:
            event.widget.bind('<Double-1>', 'break')
            root.after(100, root.destroy)  # simple root.destroy() causes some strange warnings in childs
            return
        widget.configure(text=f'Selected Destination: {master_data[0]}')
    except IndexError:
        pass


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
