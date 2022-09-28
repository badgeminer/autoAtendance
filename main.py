import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb
import json,sys
import requests

ver = "0.0.1"
upd = False
with requests.get(
        "https://raw.githubusercontent.com/badgeminer/autoAtendance/main/Ver"
) as v:
    if ver != v.text:
        upd = True
        mb.showinfo(
            "new version!",
            f"there is a new version available!\n you are on V{ver}\n V{v.text} is available"
        )
stud = json.load(open("usrs.json"))["usrs"]

studLs = list(stud.values())
studLs.sort()


class log(tk.Frame):

    def __init__(self, master):
        super().__init__(master)
        self.pack()
        if upd:
          self.upd = tk.Button(text="Update", command=self.upd,activebackground="red",background="red")
          self.upd.pack(side="top")
        self.entrythingy = tk.Entry()
        self.entrythingy.pack()

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
        self.lableNH = tk.Label(text="<- Not Here\n\nHere ->")
        self.resetB = tk.Button(text="reset", command=self.reset,activeforeground="red")
        self.resetB.pack(side="top")
        I = 0
        for i in studLs:
            self.notHere.insert(I, i)
            I += 1
        self.notHere.pack(side='left')
        self.scroll = tk.Scrollbar()
        self.scroll.pack(side='left', fill='both')
        self.lableNH.pack(side="left")
        self.scrollH = tk.Scrollbar()
        self.scrollH.pack(side='right', fill='both')
        self.Here = tk.Listbox()
        self.Here.pack(side='left')
        self.notHere.config(yscrollcommand=self.scroll.set)
        self.scroll.config(command=self.notHere.yview)
        self.Here.config(yscrollcommand=self.scrollH.set)
        self.scrollH.config(command=self.Here.yview)
        self.Here.bind('<Double-1>', self.move_st_nH)
        self.notHere.bind('<Double-1>', self.move_st_H)

    def move_st_nH(self, event):
        entrys = self.Here.get(0, 50)
        place = self.Here.get(self.Here.curselection())
        self.Here.delete(entrys.index(place))
        self.notHere.insert(studLs.index(place), place)

    def move_st_H(self, event):
        entrys = self.notHere.get(0, 50)
        place = self.notHere.get(self.notHere.curselection())
        self.notHere.delete(entrys.index(place))
        self.Here.insert(studLs.index(place), place)

    def print_contents(self, event):
        entrys = self.notHere.get(0, 50)

        if self.contents.get() in stud.keys():
            try:
                print(f"{self.contents.get()}-{stud[self.contents.get()]}")

                self.notHere.delete(entrys.index(stud[self.contents.get()]))
                self.Here.insert(studLs.index(stud[self.contents.get()]),
                                 stud[self.contents.get()])
            except:
                print(f"{self.contents.get()}")
        else:
            print(f"{self.contents.get()}")
        self.contents.set("")

    def reset(self):
        self.Here.delete(0, 50)
        self.notHere.delete(0, 50)
        I = 0
        for i in studLs:
            self.notHere.insert(I, i)
            I += 1
    def upd(self):
      f = open("main.py",mode="w")
      c = requests.get("https://raw.githubusercontent.com/badgeminer/autoAtendance/main/main.py")
      f.write(c.text)
      f.close()
      sys.exit()


root = tk.Tk()
myapp = log(root)
myapp.mainloop()
