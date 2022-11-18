########################
#   Auto Attendance    #
#    By Badgeminer2    #
# a open sorce project #
########################
#greifed: 1 time
###################
# ver = version   #
# stud = students #
# upd = update    #
# H = here        #
# NH = not here   #
###################

#imports 
import tkinter as tk
from tkinter import ttk
import json, sys
import colorama
from termcolor import colored
import configparser
import getopt
import logging
import coloredlogs
import vercheck as updr

import gs




#inits
colorama.init(autoreset=True)

upd = False
argv = sys.argv[1:]

config = configparser.ConfigParser()
config.read('cfgs.ini')

logging.basicConfig(format="%(asctime)s [%(levelname)s]: %(message)s", level=logging.DEBUG,filename=config['logging']['file'])
coloredlogs.install(level='DEBUG',fmt="%(asctime)s [%(levelname)s]: %(message)s",filename=config['logging']['file'])

ver = config['DEFAULT']['version']

logging.debug("starting system\n\n\n\n")
updr.chunks = int(config["DEFAULT"]['downloadChunkSize'])
updr.branch = config["UPDATE"]['verBranch']
if config["sheets"].getboolean('enabled'):
  gs.init(config["sheets"]["id"])

#cmdline args
clas = "usrs"
try:
    opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
except getopt.GetoptError:
    print('test.py --class <class>')
    sys.exit(2)
for opt, arg in opts:
    if opt == "--class":
      clas = arg
      
#init students
stud = json.load(open("usrs.json"))[clas]
studLs = list(stud.values())
studLs.sort()
studs = dict.fromkeys(studLs, False)


#cofigs


dcs = int(config['DEFAULT']['downloadChunkSize'])
max = int(config['ATTENDANCE']['maxStud'])
sync = config['sheets'].getboolean('enabled')


#update checking
if config['UPDATE'].getboolean('checkForUpd'):
    upd =updr.check(config["UPDATE"]["verBranch"],ver)

#custom title bar

# title bar colors
TITLE_FOREGROUND = "white"
TITLE_BACKGROUND = "#2c2c2c"
TITLE_BACKGROUND_HOVER = "green"

BUTTON_FOREGROUND = "white"
BUTTON_BACKGROUND = TITLE_BACKGROUND
BUTTON_FOREGROUND_HOVER = BUTTON_FOREGROUND
BUTTON_min_FOREGROUND_HOVER = "white"
BUTTON_min_BACKGROUND_HOVER = 'blue'
BUTTON_BACKGROUND_HOVER = 'red'

# window colors
WINDOW_BACKGROUND = "white"
WINDOW_FOREGROUND = "black"

def darkstyle(root):
    ''' Return a dark style to the window'''
    
    style = ttk.Style(root)
    return style

class MyButton(tk.Button):

    def __init__(self, master, text='x', command=None,afg=BUTTON_FOREGROUND_HOVER,abg=BUTTON_BACKGROUND_HOVER, **kwargs):
        super().__init__(master, bd=0, font="bold", padx=5, pady=2, 
                         fg=BUTTON_FOREGROUND, 
                         bg=BUTTON_BACKGROUND,
                         activebackground=abg,
                         activeforeground=afg, 
                         highlightthickness=0, 
                         text=text,
                         command=command)

        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)

    def on_enter(self, event):
        self['bg'] = BUTTON_BACKGROUND_HOVER

    def on_leave(self, event):
        self['bg'] = BUTTON_BACKGROUND

class MyTitleBar(tk.Frame):

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, relief='raised', bd=1, 
                         bg=TITLE_BACKGROUND,
                         highlightcolor=TITLE_BACKGROUND, 
                         highlightthickness=0)
        self.columnconfigure(4, weight=3)
        self.title_label = tk.Label(self, 
                                    bg=TITLE_BACKGROUND, 
                                    fg=TITLE_FOREGROUND)
                                    
        self.set_title("Auto Attendance V"+ver)

        self.close_button = MyButton(self, text='x', command=master.destroy)
        self.minimize_button = MyButton(self, text='-', command=self.on_minimize,afg=BUTTON_min_FOREGROUND_HOVER,abg=BUTTON_min_BACKGROUND_HOVER)
        self.other_button = MyButton(self, text='?', command=self.on_other)
                         
        self.grid(column=0, row=0, sticky='ew',columnspan=4)
        self.title_label.grid(column=0, row=0,columnspan=4)
        self.close_button.grid(column=7, row=0,sticky='ew')
        self.minimize_button.grid(column=6, row=0,sticky='w')
        self.other_button.grid(column=5, row=0,sticky='w')

        self.bind("<ButtonPress-1>", self.on_press)
        self.bind("<ButtonRelease-1>", self.on_release)
        self.bind("<B1-Motion>", self.on_move)
        
    def set_title(self, title):
        self.title = title
        self.title_label['text'] = title
        
    def on_press(self, event):
        self.xwin = event.x
        self.ywin = event.y
        self.set_title("Auto Attendance V"+ver+" - ... I'm moving! ...")
        self['bg'] = 'green'
        self.title_label['bg'] = TITLE_BACKGROUND_HOVER

    def on_release(self, event):
        self.set_title("Auto Attendance V"+ver)
        self['bg'] = TITLE_BACKGROUND
        self.title_label['bg'] = TITLE_BACKGROUND
        
    def on_move(self, event):
        x = event.x_root - self.xwin
        y = event.y_root - self.ywin
        self.master.geometry(f'+{x}+{y}')
        
    def on_minimize(self):
        print('TODO: minimize')
                
    def on_other(self):
        print('TODO: other')
      
#define the main window
class window(ttk.Frame):
    
    #setup window
    def __init__(self, master):
        super().__init__(master)

        #configure grid rows and columns
        self.rowconfigure(0, weight=2)
        self.rowconfigure(1, weight=2)
        self.rowconfigure(2, weight=2)
        self.rowconfigure(5, weight=5)
        self.columnconfigure(1, weight=1)

        #if there is a update add the update btn
        if upd:
            self.upd = tk.Button(text="Update",
                                 command=updr.upd,
                                 activebackground="red",
                                 background="red")
            self.upd.grid(column=0, row=2, columnspan=4)

        #setup entry box
        self.entrythingy = tk.Entry(foreground="white",background='#3d3d3d')

        # ttk vars
        self.contents = tk.StringVar()

        #setup input box
        self.contents.set("")
        self.entrythingy["textvariable"] = self.contents
        self.entrythingy.bind('<Key-Return>', self.print_contents)

        #setup listboxes
        self.notHere = tk.Listbox(foreground="white",background='#3d3d3d')
        self.Here = tk.Listbox(foreground="white",background='#3d3d3d')
        #self.notHere = ttk.Treeview()
        #self.Here = ttk.Treeview()

        #setup scroll bars
        self.scroll = tk.Scrollbar()
        self.scrollH = tk.Scrollbar()
      
        #setup labels
        self.lableNH = tk.Label(text="Not Here",foreground="white",background='#3d3d3d')
        self.lableH = tk.Label(text="Here",foreground="white",background='#3d3d3d')

        #setup btns
        #self.resetB = ttk.Button(text="reset", command=self.reset, activeforeground="red")
        #self.syncb = ttk.Button(text="sync", command=self.sync, activeforeground="blue")
        self.resetB = tk.Button(text="reset", command=self.reset,activeforeground="red",foreground="white",background='#3d3d3d',activebackground='#3d3d3d')
        self.syncb = tk.Button(text="sync", command=self.sync,foreground="white",activeforeground="blue",background='#3d3d3d',activebackground='#3d3d3d')

        #add reset button to grid
        self.resetB.grid(column=2, row=2)

        #add sync
        self.syncb.grid(column=0, row=2)

        #add entry box to grid
        self.entrythingy.grid(column=0, row=1, columnspan=4)
      
        #add studs to lists
        I = 0
        for i in studLs:
            self.notHere.insert(I, i)
            I += 1

        #add labels to grid
        self.lableNH.grid(column=0, row=3)
        self.lableH.grid(column=2, row=3)

        #add scroll bars to grid
        self.scroll.grid(column=1, row=4, sticky="ns")
        self.scrollH.grid(column=3, row=4, sticky="ns")

        #add lists to grid
        self.notHere.grid(column=0, row=4)
        self.Here.grid(column=2, row=4)

        #event bindings
        self.notHere.config(yscrollcommand=self.scroll.set)
        self.scroll.config(command=self.notHere.yview)
        self.Here.config(yscrollcommand=self.scrollH.set)
        self.scrollH.config(command=self.Here.yview)

        self.Here.bind('<Double-1>', self.move_st_nH)
        self.notHere.bind('<Double-1>', self.move_st_H)

    #######bindings#######

    #move ppl to not here
    def move_st_nH(self, event):
        try:
            entrys = self.Here.get(0, max)
            place = self.Here.get(self.Here.curselection())
            print(colored(f"{place} Here -> NotHere", "red"))

            self.Here.delete(entrys.index(place))
            self.notHere.insert(studLs.index(place), place)
            studs[place] = False
        except ttk.TclError as e:
            logging.warning(f"usrMoveErr: {str(e)}")

    #move ppl to here
    def move_st_H(self, event):
        try:
            entrys = self.notHere.get(0, max)
            place = self.notHere.get(self.notHere.curselection())

            print(colored(f"{place} NotHere -> Here", "green"))

            self.notHere.delete(entrys.index(place))
            self.Here.insert(studLs.index(place), place)
            studs[place] = True
        except ttk.TclError as e:
            logging.warning(f"usrMoveErr: {str(e)}")

    #scan and move
    #runs on <enter> pressed in input box
    def print_contents(self, event):
        entrys = self.notHere.get(0, max)
        
        #get if student is valid
        if self.contents.get() in stud.keys():
            try:
                self.notHere.delete(entrys.index(stud[self.contents.get()]))
                self.Here.insert(studLs.index(stud[self.contents.get()]),
                                 stud[self.contents.get()])
                studs[stud[self.contents.get()]] = True
                print(colored(f"{self.contents.get()}:{stud[self.contents.get()]} NotHere -> Here","green"))
            except Exception as e:
                logging.warning(f"problem with moving student: {str(e)}")
        else:
            print(colored(f"Not found:{self.contents.get()}", "red"))
        self.contents.set("")

    #reset btn
    #moves all students back to not here
    def reset(self):
        self.Here.delete(0, max)
        self.notHere.delete(0, max)
        print(colored("[*] Here -> NotHere", "red"))

        I = 0
        for i in studLs:
            logging.debug(f"moving {str(i)} to id_{str(I)}")
            self.notHere.insert(I, i)
            I += 1
            studs[i] = False

    def sync(self):
      if sync:
        gs.build_sheet(studs)
      



#run the app
root = tk.Tk()
style = darkstyle(root)
root.overrideredirect(True)
title_bar = MyTitleBar(root) 
root.geometry('355x260')
root.configure(background='#3d3d3d')
myapp = window(root)
myapp.master.title(f"Auto Attendance V{ver}")
try:
  myapp.mainloop()
except Exception as e:
  logging.fatal(str(e))
logging.debug("shuting down")