#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 24 20:17:24 2020

@author: daveandmarinda
"""

from guizero import App, Box, Text, TextBox, PushButton

# class item:
#     def __init__(self, name, position, def_val):
#
app = App()

title_box = Box(app, width="fill", align="top", border=True)
Text(title_box, text="title")

buttons_box = Box(app, width="fill", align="bottom", border=True)
Text(buttons_box, text="buttons")

options_box = Box(app, height="fill", align="right", border=True)
Text(options_box, text="options")

content_box = Box(app, align="top", width="fill", border=True)
Text(content_box, text="content")

# form_box = Box(content_box, layout="grid", width="fill", align="left", border=True)
# Text(form_box, grid=[0,0], text="form", align="right")
# Text(form_box, grid=[0,1], text="label", align="left")
# TextBox(form_box, grid=[1,1], text="data", width="fill")

def add_1():
    val = int(bread_val.value)
    bread_val.value = str(val+1)

def sub_1():
    val = int(bread_val.value)
    bread_val.value = str(val-1)

plusses = []
minuses = []
items = []
boxes = []
boxes.append(Box(content_box, layout="grid", width="fill", align="left", border=True))
Text(bread_box, grid=[0,0], text="Bread", align="left")
plus = PushButton(bread_box, grid=[1,0], text="+", command=add_1, align="left")
bread_val = TextBox(bread_box, grid=[2,0], text="0", align="left")
minus = PushButton(bread_box, grid=[3,0], text="-", command=sub_1, align="left")

app.display()
