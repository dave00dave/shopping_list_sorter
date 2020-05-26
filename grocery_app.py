#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 24 20:17:24 2020

@author: daveandmarinda
"""

from guizero import App, Box, Text, TextBox, PushButton
from collections import OrderedDict

class item:
    def __init__(self, box, order, label, def_val):
        self.text = Text(box, grid=[0, order], text=label, align="left")
        self.plus = PushButton(box, grid=[1, order], text="+",
                               command=self.add_1, align="left")
        self.val = TextBox(box, grid=[2, order], text=str(def_val), align="left")
        self.minus = PushButton(box, grid=[3, order], text="-",
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
Text(content_box, grid=[0,0], text="content")

# form_box = Box(content_box, layout="grid", width="fill", align="left", border=True)
# Text(form_box, grid=[0,0], text="form", align="right")
# Text(form_box, grid=[0,1], text="label", align="left")
# TextBox(form_box, grid=[1,1], text="data", width="fill")

# def add_1():
#     val = int(bread_val.value)
#     bread_val.value = str(val+1)
#
# def sub_1():
#     val = int(bread_val.value)
#     bread_val.value = str(val-1)

items = ['bread', 'milk', 'pizza']

# boxes = []
# boxes.append(Box(content_box, layout="grid", width="fill", align="left", border=True))
# Text(bread_box, grid=[0,0], text="Bread", align="left")
# plus = PushButton(bread_box, grid=[1,0], text="+", command=add_1, align="left")
# bread_val = TextBox(bread_box, grid=[2,0], text="0", align="left")
# minus = PushButton(bread_box, grid=[3,0], text="-", command=sub_1, align="left")

item_d = OrderedDict()
n=1
for i in items:
    item_d.update({i: item(content_box, n, i, 0)})
    n+=1


app.display()
