import requests
import tkinter.messagebox
import platform
def report(traceback):
    rst = f"{platform.processor()}:{platform.platform()}\non:{platform.machine()}\npython version:{platform.python_version()}\n\n{traceback}"
    r = requests.post("https://crashReporter.badgeminer2.repl.co/aatend",
    rst
    )
    r.raise_for_status()
    tkinter.messagebox.showerror("auto attendance has crashed","auto attendance has crashed\n"+rst)