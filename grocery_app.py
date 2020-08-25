#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 24 20:17:24 2020

@author: daveandmarinda
"""
import numpy as np
import csv
from guizero import App, Box, Text, TextBox, PushButton
from tkinter import Scrollbar

class item:
    def __init__(self, box, row, col, label, def_val):
        self.text = Text(box, grid=[col+0, row], text=label, align="right")
        self.plus = PushButton(box, grid=[col+3, row], text="+",
                               command=self.add_1, align="left")
        self.val = TextBox(box, grid=[col+2, row], text=str(def_val), width=2,
                           align="left")
        self.minus = PushButton(box, grid=[col+1, row], text="-",
                                command=self.sub_1, align="left")
    def add_1(self):
        val = int(self.val.value)
        self.val.value = str(val+1)
        update_list()
    def sub_1(self):
        val = int(self.val.value)
        if val - 1 >= 0:
            self.val.value = str(val-1)
        else:
            self.val.value = 0
        update_list()

def update_list():
    global list_in_order
    disp_list = list_display.value.splitlines()
    disp_list = [x.replace('\t', '') for x in disp_list]
    disp_list = [x.replace('\t', '') for x in list_display.value.splitlines()]
    # disp_list = [x.replace("'", '') for x in disp_list]
    # print(list(set(disp_list) - set(g_items)))
    custom_items = np.setdiff1d(disp_list, g_items)
    custom_items = np.delete(custom_items, 0)

    # find items that have (#); they h will be flagged as custom by the first check
    dc = []  # double check list
    for i in custom_items:
        if i[-2].isnumeric():
            x = [j for j in range(len(i)) if i.startswith('(', j)]
            if x:
                print(i, x)
                dc.append(i[:(x[-1]-1)])
                if i[:(x[-1]-1)] in g_items:
                    custom_items = custom_items[custom_items != i]

    tmp_list = []
    d_str = ""
    for i in g_items:
        if int(item_d[i].val.value) > 0:
            if int(item_d[i].val.value) > 1:
                tmp_list.append(str(i + ' (' + item_d[i].val.value + ')'))
                d_str += str(i + ' (' + item_d[i].val.value + ')\n')
            else:
                tmp_list.append(i)
                d_str += str(i + "\n")
    for i in custom_items:
        d_str += str(i + "\n")
    list_display.value = d_str


def save_list():
    update_list()
    save_name = app.question("Save to File", "Enter Name to Save List As")
    try:
        tmp = save_name.split('.')
        if tmp[-1] != 'csv':
            filename = tmp[0] + '.csv'
        else:
            filename = save_name
    except:
        filename = save_name + '.csv'
        pass
    with open(filename, mode='w') as write_file:
        file_writer = csv.writer(write_file, delimiter='v')
        for i in list_in_order:
            file_writer.writerow([i])

def load_list():
    load_file = app.select_file(title="Select Saved List", folder=".",
                                filetypes=[["CSV files", ".csv"]])
    if load_file != '':
        clear_list()
        loaded_d = dict()
        with open(load_file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                tmp = row[0]
                if tmp[-1] == ')':
                    tmp_num = int(tmp[-2])
                    loaded_d.update({tmp[0:-4]: tmp_num})
                else:
                    loaded_d.update({tmp: 1})

        for k, v in loaded_d.items():
            for i, n in item_d.items():
                if k == i:
                    n.val.value = v
                    break
        update_list()

def clear_list():
    for n in item_d.values():
        n.val.value = 0
    list_display.value = ''
    update_list()

def ask_clear_list():
    if app.yesno("Clear", "Do you want to clear the list?"):
        clear_list()

def load_store(store):
    ret_val = dict()
    if store == 'ask':
        load_file = app.select_file(title="Select Store", folder=".",
                                    filetypes=[["CSV files", ".csv"]])
    elif store[-4:]:
        load_file = store
    else:
        app.error('Incorrect File', 'Incorrect file type selected')

    if 'load_file' in locals():
        items = []
        with open(load_file, encoding='utf-8-sig') as csv_file:  # handle csv's saved by excel
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                items.append(row[0])

        items = [x.replace('\t', '') for x in items]
        # TODO: handle cases where I load a store with fewer items that were previously loaded
        r = 0
        c = 0
        c_cnt = 0
        sorted_items = sorted(items)
        for i in sorted_items:
            ret_val.update({i: item(content_box, r, c, i, 0)})
            r += 1
            c_cnt += 1
            if np.mod(c_cnt, 20) == 0:
                c += 4
                c_cnt = 0
                r = 0
    return items, ret_val

def load_store_clear():
    global g_items, item_d
    item_d.clear()
    g_items = []
    g_items, item_d = load_store('ask')
    clear_list()

def page_back():
    a=1

def page_forward():
    a=1


app = App(title="Grocery List Sorter", height=1200, width=1440)

buttons_box = Box(app, width="fill", align="bottom", border=True)
PushButton(buttons_box, text="Save List", command=save_list, align="left")
PushButton(buttons_box, text="Load List", command=load_list, align="left")
PushButton(buttons_box, text="Load Store", command=load_store_clear, align="left")
PushButton(buttons_box, text="Clear List", command=ask_clear_list, align="right")
PushButton(buttons_box, text="Next", command=page_forward, align="right")
PushButton(buttons_box, text="Prev", command=page_back, align="right")

list_box = Box(app, height="fill", align="right", border=True)
list_display = TextBox(list_box, multiline=True, scrollbar=True, height="fill",
                       width=30, align="left", text="")

content_box = Box(app, align="top", layout="grid", width="fill", border=True)

# items = ['Fruit',
#          'Lettuce',
#          'Carrots',
#          'Bagels',
#          'Bread',
#          'Buns',
#          'Raisins',
#          'Crackers',
#          'Graham Crackers',
#          'Tortilla Chips',
#          'Mild Salsa',
#          'Medium Salsa',
#          'Hummus',
#          'Cheese Sticks',
#          'Pretzels',
#          'Popcorn',
#          'Flour',
#          'Sugar',
#          'Brown Sugar',
#          'Milk',
#          'Frozen Pizza']

default_store = 'Lawrence_Aldi.csv'
g_items, item_d = load_store(default_store)
app.display()
