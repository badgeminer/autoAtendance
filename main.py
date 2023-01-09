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
import tkinter.ttk as ttk
import json, sys
import colorama
from termcolor import colored
import configparser
import logging
import coloredlogs
import vercheck as updr
from tkinter.simpledialog import askstring
#from ctypes import windll
import platform
import gc
import verboselogs


import gs
import argparse
import traceback




#inits
colorama.init(autoreset=True)

upd = False
argv = sys.argv[1:]

config = configparser.ConfigParser()
config.read('cfgs.ini')

verboselogs.install()
logging.basicConfig(format="%(asctime)s [%(levelname)s]: %(message)s", level=1,filename=config['logging']['file'])

coloredlogs.install(level=5,fmt="%(asctime)s [%(levelname)s]: %(message)s",filename=config['logging']['file'])

logging.debug("[main.py]starting system")



ver = config['DEFAULT']['version']
logging.log(15,"[main.py]using version v"+ver)

updr.chunks = int(config["DEFAULT"]['downloadChunkSize'])
updr.branch = config["UPDATE"]['verBranch']
if config["sheets"].getboolean('enabled'):
  gs.init(config["sheets"]["id"])

#cmdline args
logging.log(5,"[main.py]loading command-line arguments")
clas = "usrs"
parser = argparse.ArgumentParser()
parser.add_argument("--useclass",
                      default="usrs",
                      help="the class to use")

args = parser.parse_args()
clas = args.useclass
logging.log(25,f"[main.py]using class {clas}")
clases = []
for i in json.load(open("usrs.json")).keys():
    clases.append(i)
#init students
try:
    stud = json.load(open("usrs.json"))[clas]
except BaseException as e:
    logging.critical(f"[main.py]Invalid class:{clas}")
    logging.critical(f"[main.py]{traceback.format_exc()}")
    logging.error("[main.py]shuting down...")
    logging.log(5,"[main.py]cleaned up "+str(gc.collect())+" objects")
    logging.error("[main.py]crashed with exit code -5")
    sys.exit(-5)
studLs = list(stud.values())
studLs.sort()
studs = dict.fromkeys(studLs, False)

logging.debug("[main.py]loaded class")

#cofigs

logging.log(5,"[main.py]reading configs")

dcs = int(config['DEFAULT']['downloadChunkSize'])
max = int(config['ATTENDANCE']['maxStud'])
sync = config['sheets'].getboolean('enabled')
safetoclose = not config['DEFAULT'].getboolean('closeprot')
cpsw = config['DEFAULT']['closepsw']

logging.debug("[main.py] configs read")

logging.log(15,"[main.py]checking for updates")

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


def close(*args,**kwargs):
    
    if safetoclose:
        root.destroy()
    else:
        psw = askstring("enter the pasword to close", "enter the pasword to close auto attendance")
        if psw == cpsw:
            root.destroy()
        else:
            tk.messagebox.showerror("invalid psw","the psw entered is invalid")
            logging.warning("[main.py]invalid close pasword")



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
        self.title_txt = "Auto Attendance V"+ver
        if upd:
            self.title_txt = self.title_txt +"⎇"
        elif not config['UPDATE'].getboolean('checkForUpd'):
            self.title_txt = self.title_txt +"⌁"
        self.set_title(self.title_txt)

        self.close_button = MyButton(self, text='x', command=close)
        #self.minimize_button = MyButton(self, text='-', command=self.on_minimize,afg=BUTTON_min_FOREGROUND_HOVER,abg=BUTTON_min_BACKGROUND_HOVER)
        self.other_button = MyButton(self, text='?', command=self.on_other)
                         
        self.grid(column=0, row=0, sticky='ew',columnspan=4)
        self.title_label.grid(column=0, row=0,columnspan=4)
        self.close_button.grid(column=7, row=0,sticky='ew')
        #self.minimize_button.grid(column=6, row=0,sticky='w')
        self.other_button.grid(column=5, row=0,sticky="w")

        self.bind("<ButtonPress-1>", self.on_press)
        self.bind("<ButtonRelease-1>", self.on_release)
        self.bind("<B1-Motion>", self.on_move)
        
    def set_title(self, title):
        self.title = title
        self.title_label['text'] = title
        
    def on_press(self, event):
        self.xwin = event.x
        self.ywin = event.y
        self.set_title(self.title_txt+" - ... I'm moving! ...")
        self['bg'] = 'green'
        self.title_label['bg'] = TITLE_BACKGROUND_HOVER

    def on_release(self, event):
        self.set_title(self.title_txt)
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
class window(tk.Frame):
    
    #setup window
    def __init__(self, master):
        super().__init__(master)
        self.style = ttk.Style().configure("TNotebook", foreground="white",background='#3d3d3d')

        #configure grid rows and columns
        self.rowconfigure(0, weight=2)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=2)
        self.rowconfigure(3, weight=2)
        self.rowconfigure(6, weight=5)
        self.columnconfigure(1, weight=1)

        #add tabs
        self.tabs = ttk.Notebook()
        self.tabs.grid(column=0,columnspan=6,row=1,sticky="ew")
        self.tbz = {}
        #self.tabs.add(self.tb1,text="test")
        for c in clases:
            self.tbz[c] = ttk.Frame(self.tabs)
            self.tabs.add(self.tbz[c],text=c)

        #if there is a update add the update btn
        if upd:
            self.upd = tk.Button(text="Update",
                                 command=updr.upd,
                                 activebackground="red",
                                 background="red")
            self.upd.grid(column=0, row=3, columnspan=4)

        #setup entry box
        self.entrythingy = tk.Entry(foreground="white",background='#3d3d3d')

        # tk vars
        self.contents = tk.StringVar()

        #setup input box
        self.contents.set("")
        self.entrythingy["textvariable"] = self.contents
        self.entrythingy.bind('<Key-Return>', self.print_contents)

        #setup listboxes
        self.notHere = tk.Listbox(foreground="white",background='#3d3d3d')
        self.Here = tk.Listbox(foreground="white",background='#3d3d3d')
        #self.notHere = tk.Treeview()
        #self.Here = tk.Treeview()

        #setup scroll bars
        self.scroll = tk.Scrollbar()
        self.scrollH = tk.Scrollbar()
      
        #setup labels
        self.lableNH = tk.Label(text="Not Here",foreground="white",background='#3d3d3d')
        self.lableH = tk.Label(text="Here",foreground="white",background='#3d3d3d')

        #setup btns
        #self.resetB = tk.Button(text="reset", command=self.reset, activeforeground="red")
        #self.syncb = tk.Button(text="sync", command=self.sync, activeforeground="blue")
        self.resetB = tk.Button(text="reset", command=self.reset,activeforeground="red",foreground="white",background='#3d3d3d',activebackground='#3d3d3d')
        self.syncb = tk.Button(text="sync", command=self.sync,foreground="white",activeforeground="blue",background='#3d3d3d',activebackground='#3d3d3d')

        #add reset button to grid
        self.resetB.grid(column=2, row=3)

        #add sync
        self.syncb.grid(column=0, row=3)

        #add entry box to grid
        self.entrythingy.grid(column=0, row=2, columnspan=4)
      
        #add studs to lists
        I = 0
        for i in studLs:
            self.notHere.insert(I, i)
            I += 1

        #add labels to grid
        self.lableNH.grid(column=0, row=4)
        self.lableH.grid(column=2, row=4)

        #add scroll bars to grid
        self.scroll.grid(column=1, row=5, sticky="ns")
        self.scrollH.grid(column=3, row=5, sticky="ns")

        #add lists to grid
        self.notHere.grid(column=0, row=5)
        self.Here.grid(column=2, row=5)

        #other
        if not sync:
            self.syncb['state'] = tk.DISABLED

        #event bindings
        self.notHere.config(yscrollcommand=self.scroll.set)
        self.scroll.config(command=self.notHere.yview)
        self.Here.config(yscrollcommand=self.scrollH.set)
        self.scrollH.config(command=self.Here.yview)

        self.Here.bind('<Double-1>', self.move_st_nH)
        self.notHere.bind('<Double-1>', self.move_st_H)
        self.tabs.bind('<<NotebookTabChanged>>',self.tab)

    #######bindings#######


    #move ppl to not here
    def move_st_nH(self, event):
        try:
            entrys = self.Here.get(0, max)
            place = self.Here.get(self.Here.curselection())
            logging.log(15,f"[main.py]{place} Here -> NotHere")

            self.Here.delete(entrys.index(place))
            self.notHere.insert(studLs.index(place), place)
            studs[place] = False
        except tk.TclError as e:
            logging.error(f"[main.py]usrMoveErr: {str(e)}")

    #move ppl to here
    def move_st_H(self, event):
        try:
            entrys = self.notHere.get(0, max)
            place = self.notHere.get(self.notHere.curselection())

            logging.log(15,f"[main.py]{place} NotHere -> Here")

            self.notHere.delete(entrys.index(place))
            self.Here.insert(studLs.index(place), place)
            studs[place] = True
        except tk.TclError as e:
            logging.error(f"[main.py]usrMoveErr: {str(e)}")

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
                logging.log(15,f"[main.py]{self.contents.get()}:{stud[self.contents.get()]} NotHere -> Here")
            except Exception as e:
                logging.warning(f"[main.py]problem with moving student: {str(e)}")
        else:
            logging.warning(f"[main.py]Not found:{self.contents.get()}")
        self.contents.set("")

    #reset btn
    #moves all students back to not here
    def reset(self):
        self.Here.delete(0, max)
        self.notHere.delete(0, max)
        logging.log(15,f"[main.py]<*> Here -> NotHere")

        I = 0
        for i in studLs:
            logging.log(5,f"[main.py]moving {str(i)} to id_{str(I)}")
            self.notHere.insert(I, i)
            I += 1
            studs[i] = False

    def sync(self):
      if sync:
        gs.build_sheet(studs)
    def tab(self,event):
        global studs,stud,studLs
        if safetoclose:
            pass
        else:
            psw = askstring("enter the pasword", "enter the pasword")
            if psw == cpsw:
                pass
            else:
                tk.messagebox.showerror("invalid psw","the psw entered is invalid")
                logging.warning("[main.py]invalid pasword")
                return None
        del studLs
        del stud
        del studs
        clas = self.tabs.tab(self.tabs.select(), "text")
        try:
            stud = json.load(open("usrs.json"))[clas]
            if "38302008" in stud.keys():
                stud["38302008"] = stud["38302008"]+"⌁"
        except BaseException as e:
            logging.critical(f"[main.py]Invalid class:{clas}")
            logging.critical(f"[main.py]{traceback.format_exc()}")
            logging.error("[main.py]shuting down...")
            logging.log(5,"[main.py]cleaned up "+str(gc.collect())+" objects")
            logging.error("[main.py]crashed with exit code -5")
            sys.exit(-5)
        studLs = list(stud.values())
        studLs.sort()
        studs = dict.fromkeys(studLs, False)
        self.reset()
        logging.log(15,"[main.py] swaped classes")
      



logging.log(15,"[main.py] loading window")
#run the app
root = tk.Tk()
logging.log(5,"[main.py] root init")

logging.log(5,"[main.py] root configs")
root.overrideredirect(True)
root.attributes("-topmost", True)
logging.log(5,"[main.py] title bar init")
title_bar = MyTitleBar(root) 
logging.log(5,"[main.py] init window size")
if platform.system() == "Windows":
  root.geometry('285x290')
else:
  root.geometry('355x290')
root.configure(background='#3d3d3d')
logging.log(5,"[main.py] contents init")
myapp = window(root)
myapp.master.title(f"Auto Attendance V{ver}")
try:
  logging.log(5,"[main.py] run main loop")
  myapp.mainloop()
except Exception as e:
  logging.fatal(str(e))
  logging.critical(f"[main.py]{traceback.format_exc()}")
logging.info("[main.py]shuting down...")
logging.log(5,"[main.py]cleaned up "+str(gc.collect())+" objects")
logging.log(35,"[main.py]done")