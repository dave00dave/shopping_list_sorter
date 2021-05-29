#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 24 20:17:24 2020

Copyright 2020-2021 David S. Ochs. All Rights Reserved

"""
import numpy as np
import csv
from guizero import App, Box, Text, TextBox, PushButton
import os
import smtplib, ssl
import pickle
from pathlib import Path

class item:
    def __init__(self, label, entry):
        self.quant = 0
        self.disp_text = label
        self.user_entry = entry
        self.user_list = []
        self.user_del_list = []  # use a list to handle deleting custom items
                                 # when updating the list so they're not
                                 # treated like user-appended custom items
                                 # and left at the end of the list
        self.val = None
        self.text = None
        self.entry = None
        self.plus = None
        self.minus = None

    def add_entry_button(self, box, row, col):
        self.text = Text(box, grid=[col+0, row], text=self.disp_text,
                    align="right", size=text_size)
        self.text.bg = 'white'
        self.entry = PushButton(box, grid=[col+1, row], text="Del",
                                command=self.remove_custom_entry, align="left",
                                width=entry_width, padx=0, pady=6)
        self.entry = PushButton(box, grid=[col+3, row], text="Add",
                                command=self.get_custom_entry, align="left",
                                width=entry_width, padx=0, pady=6)

    def add_to_screen(self, box, row, col):
        self.text = Text(box, grid=[col+0, row], text=self.disp_text,
                    align="right", size=text_size)
        self.text.bg = 'white'
        self.plus = PushButton(box, grid=[col+3, row], text="+",
                               command=self.add_1, align="left", width=pm_width,
                               padx=0, pady=6)
        self.plus.bg = 'white'
        self.val = Text(box, grid=[col+2, row], text=str(self.quant), width=2,
                           align="left")
        self.val.bg = 'white'
        self.minus = PushButton(box, grid=[col+1, row], text="-",
                                command=self.sub_1, align="left", width=pm_width,
                                padx=0, pady=6)
        self.minus.bg = 'white'

    def add_1(self):
        self.quant += 1
        if self.val:
            self.val.value = str(self.quant)
        update_list()

    def sub_1(self):
        if self.quant - 1 >= 0:
            self.quant -= 1
        else:
            self.quant = 0
        self.val.value = self.quant
        update_list()

    def get_custom_entry(self):
        cus_entry = app.question("Enter Item", "Item Name")
        if cus_entry is not None:
            self.quant += 1
            self.user_list.append(cus_entry)
            update_list()

    def remove_custom_entry(self):
        if self.quant > 0:
            cus_entry = app.question("Enter Item", "Item Name")
            if cus_entry is not None:
                if cus_entry in self.user_list:
                    self.user_del_list.append(cus_entry)
                    update_list()
                else:
                    app.warn("Warning", "Item not found (check capitalization)")

def save_cfg_item(cfg_item, value):
    if os.path.exists(CFG_FILENAME):
        with open(CFG_FILENAME, 'rb') as infile:
            cfg = pickle.load(infile)
        if cfg_item in cfg.keys():
            cfg[cfg_item] = value
        else:
            cfg.update({cfg_item: value})
    else:
        cfg = dict()
        cfg.update({cfg_item: value})
    with open(CFG_FILENAME, 'wb') as outfile:
        pickle.dump(cfg, outfile, pickle.HIGHEST_PROTOCOL)

def load_cfg_item(cfg_item):
    retval = None
    if os.path.exists(CFG_FILENAME):
        with open(CFG_FILENAME, 'rb') as infile:
            cfg = pickle.load(infile)
        if cfg_item in cfg.keys():
            retval = cfg[cfg_item]
    return retval

def check_without_number(item, store_items):
    """Remove (#) from an entry and check if the resulting string is in the store's global item list """
    retVal = ''
    if item[-2].isnumeric():
        x = [j for j in range(len(item)) if item.startswith('(', j)]
        if x:
            if item[:(x[-1]-1)] in store_items:
                retVal = item[:(x[-1]-1)]
    return retVal

def update_list():
    disp_list = list_display.value.splitlines()
    disp_list = [x.replace('\t', '') for x in disp_list]
    disp_list = [x.replace('\t', '') for x in list_display.value.splitlines()]
    custom_items = np.setdiff1d(disp_list, g_items)
    if custom_items[0] == '':
        custom_items = np.delete(custom_items, 0)

    # create a list of the user-specific items that have been added so we can
    # check for ?'s against it
    tmp_l = [x for x in item_d if 'ENTRY' in x]
    user_entry_list = []
    for i in tmp_l:
        user_entry_list.extend(item_d[i].user_list)

    # find items that have ? at the end; they will be flagged as custom by the first check
    # note those items that are in g_items so they can have ? added back later
    add_q = []
    for i in custom_items:
        if i[-1] == '?':
            tmp_item = check_without_number(i[:-1], g_items)
            if (i[:-1] in g_items) or (i[:-1] in user_entry_list):
                custom_items = custom_items[custom_items != i]
                add_q.append(i[:-1])
            elif tmp_item:
                # this catches items in the store list that have
                # more than 1 added, and a ? at the end
                custom_items = custom_items[custom_items != i]
                add_q.append(tmp_item)

    # find items that have (#); they will be flagged as custom by the first check
    for i in custom_items:
        tmp_item = check_without_number(i, g_items)
        if tmp_item:
            custom_items = custom_items[custom_items != i] # remove this
                                                           # item from the list
    tmp_list = []
    d_str = ""
    for i in g_items:
        if item_d[i].quant > 0:
            if item_d[i].user_entry:
                for d in item_d[i].user_del_list:
                    item_d[i].quant -= 1
                    item_d[i].user_list.remove(d)
                    custom_items = custom_items[custom_items != d] # don't consider this a custom item
                item_d[i].user_del_list.clear()
                for k in item_d[i].user_list:
                    if k in add_q:
                        d_str += str(k) + "?\n"
                    else:
                        d_str += str(k + "\n")
                    custom_items = custom_items[custom_items != k] # don't consider this a custom item
            else:
                if item_d[i].quant > 1:
                    tmp_list.append(str(i + ' (' + str(item_d[i].quant) + ')'))
                    if str(i) in add_q:
                        d_str += str(i + ' (' + str(item_d[i].quant) + ')?\n')
                    else:
                        d_str += str(i + ' (' + str(item_d[i].quant) + ')\n')
                elif str(i) in add_q:
                    d_str += str(i) + "?\n"
                else:
                    tmp_list.append(i)
                    d_str += str(i + "\n")
    for i in custom_items:
        d_str += str(i + "\n")
    list_display.value = d_str

def write_list_to_file(filename):
    str_list = []
    tmp = ''
    # format the whole list as a string to save in a csv
    for i in range(0, len(list_display.value)):
        if list_display.value[i] != '\n':
            tmp += list_display.value[i]
        else:
            if tmp:
                str_list.append(tmp)
            tmp = ''
    with open(filename, mode='w') as write_file:
        file_writer = csv.writer(write_file, delimiter=',')
        for i in str_list:
            file_writer.writerow([i])

        # write the user-defined custom items to the end of the file
        for k, v in item_d.items():
            if k.split()[-1] == ENTRY_KEY:
                tmp = k + ":" + ".".join(v.user_list)
                file_writer.writerow([tmp])

def save_list_as():
    global save_name_old
    update_list()
    save_name = app.select_file(title = "Select File", save = True, filetypes=[["CSV files", ".csv"]])
    if save_name:
        try:
            tmp = save_name.split('.')
            if tmp[-1] != 'csv':
                filename = tmp[0] + '.csv'
            else:
                filename = save_name
        except:
            filename = save_name + '.csv'
            pass
        write_list_to_file(filename)
        save_name_old = save_name
        save_cfg_item(AUTOLOAD_CFG_KEY, save_name_old)
        dispname = Path(save_name_old).resolve().stem
        title_box.value = dispname

def save_list():
    global save_name_old
    if save_name_old:
        write_list_to_file(save_name_old)
        save_cfg_item(AUTOLOAD_CFG_KEY, save_name_old)
        dispname = Path(save_name_old).resolve().stem
        title_box.value = dispname
    else:
        save_list_as()

def load_list_ask():
    lf = app.select_file(title="Select Saved List", folder=".",
                                filetypes=[["CSV files", ".csv"]])
    load_list(lf)

def load_list(load_file):
    global save_name_old
    if load_file != '' and os.path.exists(load_file):
        clear_list()
        loaded_d = dict()
        cus_entry_d = dict()
        add_q = []
        with open(load_file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                q_here = False
                if row[0][-1] == '?':
                    if row[0][-2] == ' ':
                        tmp = row[0][:-2]
                    else:
                        tmp = row[0][:-1]
                    q_here = True  # don't append to add_q here in case of (#)
                else:
                    tmp = row[0]
                if ENTRY_KEY in tmp.split(":")[0]:
                    # handle the special section of the saved list that contains
                    # user-specified items that are sorted (eg. spices)
                    kv = tmp.split(":")
                    k = kv[0]
                    cus_items = kv[-1].split('.')
                    for cus_en in cus_items:
                        if cus_en != '':
                            cus_entry_d.update({cus_en: k})
                else:
                    if tmp[-1] == ')' and (tmp[-2].isnumeric()): # handle items that have (#) in the list
                        c = -2
                        while tmp[c].isnumeric():
                            c -=1
                        tmp_num = int(tmp[(c+1):-1])
                        if tmp[c-1] == ' ': # handle space or not in custom item
                            loaded_d.update({tmp[0:c-1]: tmp_num})
                            if q_here:
                                add_q.append(tmp[0:c-1])
                        else:
                            loaded_d.update({tmp[0:c]: tmp_num})
                            if q_here:
                                add_q.append(tmp[0:c])
                    else:
                        loaded_d.update({tmp: 1})
                        if q_here:
                            add_q.append(tmp)
        for k,v in cus_entry_d.items():
            item_d[v].quant += 1
            item_d[v].user_list.append(k)
            del loaded_d[k]
        c_str = ''
        for k, v in loaded_d.items():
            if k in item_d:
                for q in range(v):
                    item_d[k].add_1() # call add_1 so the quantities by the buttons are updated
                if str(k) in add_q:
                    c_str += str(k) + "?\n"
            else:
                if v > 1:
                    c_str += str(k) + " (" + str(v) + ")"
                else:
                    c_str += str(k)
                if str(k) in add_q:
                    c_str += "?"
                c_str += "\n"
        list_display.value = c_str
        update_list()
        save_name_old = load_file
        save_cfg_item(AUTOLOAD_CFG_KEY, save_name_old)
        dispname = Path(save_name_old).resolve().stem
        title_box.value = dispname

def clear_list():
    for n in item_d.values():
        n.quant = 0
        if hasattr(n,'val'):
            n.val.value = 0
        n.user_list.clear()
        n.user_del_list = []
    list_display.value = ''
    title_box.value = ''
    update_list()

def ask_clear_list():
    if app.yesno("Clear", "Do you want to clear the list?"):
        clear_list()

def new_list():
    global save_name_old
    if app.yesno("Close", "Do you want to save this list before starting a new list?"):
        save_list()
    clear_list()
    save_name_old = None

def load_store(store_file):
    global num_pages, page_no
    ret_val = dict()

    items = []
    with open(store_file, encoding='utf-8-sig') as csv_file:  # handle csv's saved by excel
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            items.append(row[0])

    items = [x.replace('\t', '') for x in items]
    # TODO: handle cases where I load a store with fewer items that were previously loaded
    r = 0
    c = 0
    c_cnt = 0
    sorted_items = sorted(items)
    added = 0
    for i in sorted_items:
        tmp_name = i.split()
        if tmp_name[-1] == ENTRY_KEY:
            ret_val.update({i: item(" ".join(tmp_name[:-1]), True)})
            ret_val[i].add_entry_button(content_boxes[page_no], r, c)
        else:
            ret_val.update({i: item(i, False)})
            ret_val[i].add_to_screen(content_boxes[page_no], r, c)
        r += 1
        c_cnt += 1
        if np.mod(c_cnt, column_limit) == 0:
            c += 4
            c_cnt = 0
            r = 0
        added += 1
        if added >= page_limit and i != sorted_items[-1]:
            content_boxes[page_no].visible = False
            r = 0
            c = 0
            c_cnt = 0
            added = 0
            content_boxes.append(Box(app, align="top", layout="grid",
                                     width="fill", border=False))
            page_no += 1
            content_boxes[page_no].tk.configure(background='white')
    return items, ret_val

def page_change(dir):
    global page_no
    if dir > 0 and page_no < len(content_boxes)-1:
        content_boxes[page_no].visible = False
        page_no += 1
        content_boxes[page_no].visible = True
    elif dir < 0 and page_no >= 1:  # backwards
        content_boxes[page_no].visible = False
        page_no -= 1
        content_boxes[page_no].visible = True

def load_store_clear():
    global g_items, item_d
    load_file = app.select_file(title="Select Store", folder=".",
                                filetypes=[["CSV files", ".csv"]])
    if load_file:
        if load_file[-4:]:
            item_d.clear()
            g_items = []
            g_items, item_d = load_store(load_file)
            clear_list()
        else:
            app.error('Incorrect File', 'Incorrect file type selected')

def closing_action():
    if app.yesno("Close", "Do you want to save the list before closing?"):
        save_list()
    app.destroy()

def email_list():
    receiver_email = app.question("Enter Email", "Enter Email Address")
    if receiver_email:
        port = 465  # For SSL
        smtp_server = "smtp.gmail.com"
        subject = "Subject: Your Sorted Shopping List\n"
        body = title_box.value + '\n' + list_display.value
        message = subject + body
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)

if __name__ =='__main__':
    page_limit = 40
    column_limit = 20
    last_item = 0
    text_size = 16
    save_name_old = ''
    pm_width = 1
    entry_width = 1
    ENTRY_KEY = "ENTRY"
    AUTOLOAD_CFG_KEY = "AUTOLOAD"
    CFG_FILENAME = ".cfg.pkl"
    app = App(title="Grocery List Sorter", height=1200, width=920,
            bgcolor='white')

    buttons_box = Box(app, width="fill", align="bottom", border=True)
    PushButton(buttons_box, text="Save", command=save_list, align="left")
    PushButton(buttons_box, text="Save As", command=save_list_as, align="left")
    PushButton(buttons_box, text="New List", command=new_list, align="left")
    PushButton(buttons_box, text="Load List", command=load_list_ask, align="left")
    PushButton(buttons_box, text="Load Store", command=load_store_clear, align="left")
    # PushButton(buttons_box, text="Clear List", command=ask_clear_list, align="left")
    PushButton(buttons_box, text="Next Page", command=page_change, args = [1], align="right")
    PushButton(buttons_box, text="Previous Page", command=page_change, args = [-1], align="right")

    title_box = Box(app, height="10", align="top", border=False)
    list_box = Box(app, height="fill", align="right", border=True)
    # self.text = Text(box, grid=[col+0, row], text=self.disp_text,
                # align="right", size=text_size)
    title_box = Text(title_box, align="left", text="")
    title_box.text_size = text_size
    list_display = TextBox(list_box, multiline=True, scrollbar=True, height="fill",
                        width=26, align="left", text="")
    list_display.text_size = text_size

    content_boxes = []
    content_boxes.append(Box(app, align="top", layout="grid", width="fill", border=False))
    content_boxes[0].tk.configure(background='white')
    page_no = 0

    default_store = 'stores/Lawrence_Aldi.csv'
    g_items, item_d = load_store(default_store)
    while page_no > 0:
        page_change(-1)
    app.when_closed = closing_action

    auto_load = load_cfg_item(AUTOLOAD_CFG_KEY)
    if auto_load is not None:
        load_list(auto_load)

    # Set up email service
    if os.path.exists('credentials.txt'):
        with open('credentials.txt', 'r') as f:
            sender_email = f.readline()
            password = f.readline()
        sender_email = sender_email[:-1]
        password = password[:-1]

        # Add a send email button
        PushButton(buttons_box, text="Email List", command=email_list, align="left")
    app.display()
