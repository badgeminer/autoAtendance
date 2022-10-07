import tkinter as tk
from tkinter import messagebox as mb
import json,sys,os
import requests,colorama
from termcolor import colored
import configparser

#todo: export to google sheet 

colorama.init(autoreset=True)

config = configparser.ConfigParser()
config.read('cfgs.ini')
max = int(config['ATTENDANCE']['maxStud'])

ver = config['DEFAULT']['version']
upd = False
if config['UPDATE'].getboolean('checkForUpd'):
  with requests.get(config['UPDATE']['verCheckURL']) as v:
    if ver != v.text:
        upd = True
        mb.showinfo("new version!",f"there is a new version available!\n you are on V{ver}\n V{v.text} is available")

stud = json.load(open("usrs.json"))["usrs"]

studLs = list(stud.values())
studLs.sort()


class log(tk.Frame):

    def __init__(self, master):
        super().__init__(master)

        self.rowconfigure(0, weight=2)
        self.rowconfigure(1, weight=2)
        self.rowconfigure(4, weight=5)
        self.columnconfigure(1, weight=1)
        #update button
        if upd:
          self.upd = tk.Button(text="Update", command=self.upd,activebackground="red",background="red")
          self.upd.grid(column=0, row=1)
          
        self.entrythingy = tk.Entry()
        self.entrythingy.grid(column=0, row=0,columnspan = 4)

        # Create the application variable.
        self.contents = tk.StringVar()
        # Set it to some value.
        self.contents.set("")
        # Tell the entry widget to watch this variable.
        self.entrythingy["textvariable"] = self.contents

        # Define a callback for when the user hits return.
        # It prints the current value of the variable.
        self.entrythingy.bind('<Key-Return>', self.print_contents)
      
        self.notHere = tk.Listbox()
        self.lableNH = tk.Label(text="Not Here")
        self.lableH = tk.Label(text="Here")
        self.resetB = tk.Button(text="reset", command=self.reset,activeforeground="red")
        if upd:
          self.resetB.grid(column=2, row=1)
        else:
          self.resetB.grid(column=0, row=1,columnspan = 4)
        I = 0
        for i in studLs:
            self.notHere.insert(I, i)
            I += 1
        self.notHere.grid(column=0, row=3)
      
        self.scroll = tk.Scrollbar()
        self.scroll.grid(column=1, row=3)
      
        self.lableNH.grid(column=0, row=2)
        self.lableH.grid(column=2, row=2)
      
        self.scrollH = tk.Scrollbar()
        self.scrollH.grid(column=3, row=3)
      
        self.Here = tk.Listbox()
        self.Here.grid(column=2, row=3)

      #event bindings
        self.notHere.config(yscrollcommand=self.scroll.set)
        self.scroll.config(command=self.notHere.yview)
        self.Here.config(yscrollcommand=self.scrollH.set)
        self.scrollH.config(command=self.Here.yview)
        self.Here.bind('<Double-1>', self.move_st_nH)
        self.notHere.bind('<Double-1>', self.move_st_H)
    
      #######bindings#######

    #move ppl
    def move_st_nH(self, event):
      try:
        entrys = self.Here.get(0, max)
        place = self.Here.get(self.Here.curselection())
        print(colored(f"{place} Here -> NotHere","red"))
        self.Here.delete(entrys.index(place))
        self.notHere.insert(studLs.index(place), place)
      except tk.TclError:
        pass

    def move_st_H(self, event):
      try:
        entrys = self.notHere.get(0, max)
        place = self.notHere.get(self.notHere.curselection())
        print(colored(f"{place} NotHere -> Here","green"))
        self.notHere.delete(entrys.index(place))
        self.Here.insert(studLs.index(place), place)
      except tk.TclError:
        pass
    #scan and move 
    def print_contents(self, event):
        entrys = self.notHere.get(0, max)

        if self.contents.get() in stud.keys():
            try:
                print(colored(f"{self.contents.get()}:{stud[self.contents.get()]} NotHere -> Here","green")) 
                self.notHere.delete(entrys.index(stud[self.contents.get()]))
                self.Here.insert(studLs.index(stud[self.contents.get()]),
                                 stud[self.contents.get()])
            except:
                print(f"{self.contents.get()}")
        else:
            print(colored(f"Not found:{self.contents.get()}","red"))
        self.contents.set("")
    
    #reset btn
    def reset(self):
        self.Here.delete(0, max)
        self.notHere.delete(0, max)
        print(colored("[*] Here -> NotHere","red"))
        I = 0
        for i in studLs:
            self.notHere.insert(I, i)
            I += 1
    #update service
    def upd(self):
      print(colored('loading updater...',"grey"))
      f = open("main.py",mode="w")
      
      print(colored('downloading main.py file...',"grey"))
      c = requests.get("https://raw.githubusercontent.com/badgeminer/autoAtendance/main/main.py")
      
      print(colored('writing main.py...',"grey"))
      i = 1
      for chunk in c.iter_content(config['DEFAULT']['downloadChunkSize'],decode_unicode=True):
        print(colored(f'writing main chunk {i}...',"grey"))
        f.write(chunk)
        i +=1
        
      print(colored('saving main.py...',"grey"))
      f.close()
      
      print(colored('downloading requirements.txt...',"grey"))
      r = requests.get("https://raw.githubusercontent.com/badgeminer/autoAtendance/main/requirements.txt")
      
      print(colored('writing requirements.txt...',"grey"))
      with open("requirements.txt", 'w') as f:
        i = 0
        for chunk in r.iter_content(config['DEFAULT']['downloadChunkSize'],decode_unicode=True):
          print(colored(f'writing rqs chunk {i}...',"grey"))
          f.write(chunk)
          i+=1
        print(colored('saving reqirements.py',"grey"))
        
      print(colored('installing requirements...',"grey"))
      os.system('pip install -r requirements.txt')
      
      print(colored('done, ready for restart',"green"))
      mb.showinfo("updater","auto Atendance will now restart")
      sys.exit()


#run
root = tk.Tk()
myapp = log(root)
myapp.master.title(f"Auto Attendance V{ver}")
myapp.mainloop()