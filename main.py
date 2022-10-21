########################
#   Auto Attendance    #
#    By Badgeminer2    #
# a open sorce project #
########################

###################
# ver = version   #
# stud = students #
# upd = update    #
# H = here        #
# NH = not here   #
###################

#imports 
import tkinter as tk
from tkinter import messagebox as mb
import json, sys, os
import requests, colorama
from termcolor import colored
import configparser

#inits
colorama.init(autoreset=True)
upd = False

#init students
stud = json.load(open("usrs.json"))["usrs"]
studLs = list(stud.values())
studLs.sort()
studs = dict.fromkeys(studLs, False)

#cofigs
config = configparser.ConfigParser()
config.read('cfgs.ini')

dcs = int(config['DEFAULT']['downloadChunkSize'])
max = int(config['ATTENDANCE']['maxStud'])

ver = config['DEFAULT']['version']

#update checking
if config['UPDATE'].getboolean('checkForUpd'):
    with requests.get(f"https://raw.githubusercontent.com/badgeminer/autoAtendance/{config['UPDATE']['verBranch']}/Ver") as v:
        if ver != v.text:
            upd = True
            mb.showinfo(
                "new version!",
                f"there is a new version available!\n you are on V{ver}\n V{v.text} is available"
            )

#define the main window
class window(tk.Frame):
    
    #setup window
    def __init__(self, master):
        super().__init__(master)

        #configure grid rows and columns
        self.rowconfigure(0, weight=2)
        self.rowconfigure(1, weight=2)
        self.rowconfigure(4, weight=5)
        self.columnconfigure(1, weight=1)

        #if there is a update add the update btn
        if upd:
            self.upd = tk.Button(text="Update",
                                 command=self.upd,
                                 activebackground="red",
                                 background="red")
            self.upd.grid(column=0, row=1, columnspan=4)

        #setup entry box
        self.entrythingy = tk.Entry()

        # tk vars
        self.contents = tk.StringVar()

        #setup input box
        self.contents.set("")
        self.entrythingy["textvariable"] = self.contents
        self.entrythingy.bind('<Key-Return>', self.print_contents)

        #setup listboxes
        self.notHere = tk.Listbox()
        self.Here = tk.Listbox()

        #setup scroll bars
        self.scroll = tk.Scrollbar()
        self.scrollH = tk.Scrollbar()
      
        #setup labels
        self.lableNH = tk.Label(text="Not Here")
        self.lableH = tk.Label(text="Here")
        self.resetB = tk.Button(text="reset", command=self.reset, activeforeground="red")

        #add reset button to grid
        self.resetB.grid(column=2, row=1)

        #add entry box to grid
        self.entrythingy.grid(column=0, row=0, columnspan=4)
      
        #add studs to lists
        I = 0
        for i in studLs:
            self.notHere.insert(I, i)
            I += 1

        #add labels to grid
        self.lableNH.grid(column=0, row=2)
        self.lableH.grid(column=2, row=2)

        #add scroll bars to grid
        self.scroll.grid(column=1, row=3, sticky="ns")
        self.scrollH.grid(column=3, row=3, sticky="ns")

        #add lists to grid
        self.notHere.grid(column=0, row=3)
        self.Here.grid(column=2, row=3)

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
        except tk.TclError:
            pass

    #move ppl to here
    def move_st_H(self, event):
        try:
            entrys = self.notHere.get(0, max)
            place = self.notHere.get(self.notHere.curselection())

            print(colored(f"{place} NotHere -> Here", "green"))

            self.notHere.delete(entrys.index(place))
            self.Here.insert(studLs.index(place), place)
        except tk.TclError:
            pass

    #scan and move
    #runs on <enter> pressed in input box
    def print_contents(self, event):
        entrys = self.notHere.get(0, max)
        
        #get if student is valid
        if self.contents.get() in stud.keys():
            try:
                print(
                    colored(
                        f"{self.contents.get()}:{stud[self.contents.get()]} NotHere -> Here",
                        "green"))
                self.notHere.delete(entrys.index(stud[self.contents.get()]))
                self.Here.insert(studLs.index(stud[self.contents.get()]),
                                 stud[self.contents.get()])
            except:
                #do nothing this is ok
                pass
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
            self.notHere.insert(I, i)
            I += 1

    #define update service
    def upd(self):
        print(colored('loading updater...', "grey"))
        f = open("main.py", mode="w")

        print(colored('downloading main.py file...', "grey"))
        c = requests.get(
            f"https://raw.githubusercontent.com/badgeminer/autoAtendance/{config['UPDATE']['verBranch']}/main.py"
        )

        print(colored('writing main.py...', "grey"))
        #loop thru main.py download chunks and write to file
        i = 1
        for chunk in c.iter_content(dcs,
                                    decode_unicode=True):
            print(colored(f'writing main chunk {i}...', "grey"))
            f.write(chunk)
            i += 1

        #save file
        print(colored('saving main.py...', "grey"))
        f.close()

        #begin downloading requirements.txt
        print(colored('downloading requirements.txt...', "grey"))
        r = requests.get(
            f"https://raw.githubusercontent.com/badgeminer/autoAtendance/{config['UPDATE']['verBranch']}/requirements.txt"
        )

        print(colored('writing requirements.txt...', "grey"))

        with open("requirements.txt", 'w') as f:
            
            #loop thru requests.txt download chunks and write to file
            i = 0
            for chunk in r.iter_content(dcs,
                                        decode_unicode=True):

                print(colored(f'writing rqs chunk {i}...', "grey"))
                f.write(chunk)
                i += 1

            print(colored('saving reqirements.py', "grey"))

        #install requirements
        print(colored('installing requirements...', "grey"))
        os.system('python -m pip install -r requirements.txt')

        print(colored('done, ready for restart', "green"))
        mb.showinfo("updater", "auto Atendance will now restart")
        sys.exit()


#run the app
root = tk.Tk()
myapp = window(root)
myapp.master.title(f"Auto Attendance V{ver}")
myapp.mainloop()
