import requests,json,tkinter,logging
from requests.auth import HTTPBasicAuth
f = open("classes.json")
classes = json.load(f)
f.close()
def cansync(clas):
    return classes[clas]["enabled"]
def sb(clas):
    s = cansync(clas)
    if s:
        return tkinter.ACTIVE
    return tkinter.DISABLED
def sync(clas,cd:dict):
    logging.log(15,"[sync.py]<SYNC⎇> sync started...")
    c = {}
    for k,v in cd.items():
        if v:
            logging.log(5,f"[sync.py]<SYNC⎇> {str(v)} H")
            c[k] = "H"
        else:
            logging.log(5,f"[sync.py]<SYNC⎇> {str(v)} NH")
            c[k] = "NH"
    logging.log(15,f"[sync.py]<SYNC⎇> posting...")
    r = requests.post(
        "https://aatenddb.badgeminer2.repl.co/add?debug=t",
        json=c,
        auth=HTTPBasicAuth(classes[clas]["tbl"], classes[clas]["key"])
        )
    try:
        r.raise_for_status()
        logging.log(35,f"[sync.py]<SYNC⎇> done")
    except requests.HTTPError as e:
        logging.critical(f"[sync.py]<SYNC⎇> requests.HTTPError {str(e)}")