#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 24 20:17:24 2020

@author: daveandmarinda
"""
import numpy as np
from guizero import App, Box, Text, TextBox, PushButton
from collections import OrderedDict

class item:
    def __init__(self, box, row, col, label, def_val):
        self.text = Text(box, grid=[col+0, row], text=label, align="right")
        self.plus = PushButton(box, grid=[col+1, row], text="+",
                               command=self.add_1, align="left")
        self.val = TextBox(box, grid=[col+2, row], text=str(def_val), width=2,
                           align="left")
        self.minus = PushButton(box, grid=[col+3, row], text="-",
                                command=self.sub_1, align="left")
    def add_1(self):
        val = int(self.val.value)
        self.val.value = str(val+1)
    def sub_1(self):
        val = int(self.val.value)
        if val - 1 >= 0:
            self.val.value = str(val-1)
        else:
            self.val.value = 0



app = App()

title_box = Box(app, width="fill", align="top", border=True)
Text(title_box, text="title")

buttons_box = Box(app, width="fill", align="bottom", border=True)
Text(buttons_box, text="buttons")

options_box = Box(app, height="fill", align="right", border=True)
Text(options_box, text="options")

content_box = Box(app, align="top", layout="grid", width="fill", border=True)

items = ['fruit',
         'lettuce',
         'carrots',
         'bagels',
         'bread',
         'buns',
         'raisins',
         'crackers',
         'graham crackers',
         'tortilla chips',
         'mild salsa',
         'medium salsa',
         'hummus',
         'cheese sticks',
         'pretzels',
         'popcorn',
         'flour',
         'sugar',
         'brown sugar',
         'milk',
         'frozen pizza']


item_d = OrderedDict()
r = 0
c = 0
c_cnt = 0
for i in items:
    item_d.update({i: item(content_box, r, c, i, 0)})
    r += 1
    c_cnt += 1
    if np.mod(c_cnt, 10) == 0:
        c += 4
        c_cnt = 0
        r = 0


app.display()
