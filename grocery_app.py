#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 24 20:17:24 2020

@author: daveandmarinda
"""
import numpy as np
import csv
from guizero import App, Box, Text, TextBox, PushButton

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
    list_in_order = []
    d_str = ""
    for i in items:
        if int(item_d[i].val.value) > 0:
            if int(item_d[i].val.value) > 1:
                list_in_order.append(str(i + ' (' + item_d[i].val.value + ')'))
                d_str += str(i + ' (' + item_d[i].val.value + ')\n')
            else:
                list_in_order.append(i)
                d_str += str(i + "\n")
    list_display.value = d_str
    return list_in_order

def save_list():
    list_in_order = update_list()
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

app = App()

title_box = Box(app, width="fill", align="top", border=True)
Text(title_box, text="title")

buttons_box = Box(app, width="fill", align="bottom", border=True)
PushButton(buttons_box, text="Save List", command=save_list, align="left")

list_box = Box(app, height="fill", align="right", border=True)
list_display = TextBox(list_box, multiline=True, scrollbar=True, height="fill",
                       width=20, align="left", text="")

content_box = Box(app, align="top", layout="grid", width="fill", border=True)

items = ['Fruit',
         'Lettuce',
         'Carrots',
         'Bagels',
         'Bread',
         'Buns',
         'Raisins',
         'Crackers',
         'Graham Crackers',
         'Tortilla Chips',
         'Mild Salsa',
         'Medium Salsa',
         'Hummus',
         'Cheese Sticks',
         'Pretzels',
         'Popcorn',
         'Flour',
         'Sugar',
         'Brown Sugar',
         'Milk',
         'Frozen Pizza']

item_d = dict()
r = 0
c = 0
c_cnt = 0
sorted_items = sorted(items)
for i in sorted_items:
    item_d.update({i: item(content_box, r, c, i, 0)})
    r += 1
    c_cnt += 1
    if np.mod(c_cnt, 15) == 0:
        c += 4
        c_cnt = 0
        r = 0


app.display()
