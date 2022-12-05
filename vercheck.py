import requests,logging,sys,json

branch = "RELEASE"
chunks = 100

def check(branch:str,cver:str) -> bool:  
  """_summary_

  Args:
      branch (str): branch to check
      cver (str): curent version

  Returns:
      bool: update available
  """
  try:
    with requests.get(f"https://raw.githubusercontent.com/badgeminer/autoAtendance/{branch}/Ver") as v:
        v.raise_for_status()
        if cver != v.text.replace("\n",""):
            return True
        return False
  except requests.HTTPError as e:
      logging.error(f"cant retreive latest version {str(e)}")


def upd():
  try:
    r = requests.get("https://raw.githubusercontent.com/badgeminer/autoAtendance/RELEASE/files.json")
    r.raise_for_status()
    files = json.loads(r.text)["reqs"]
    r.close()
    for file in files:
      f = open(file+"u", 'wb')
      r = requests.get(f"https://raw.githubusercontent.com/badgeminer/autoAtendance/{branch}/{file}")
      r = requests.get("https://raw.githubusercontent.com/badgeminer/autoAtendance/"+br+"/"+file)
      r.raise_for_status()
      for chunk in r.iter_content(chunk_size=int(chunks)): 
        if chunk: # filter out keep-alive new chunks
              f.write(chunk)
      f.close()
      r.close()  
      print('done, ready for restart', "green")
      sys.exit()
  except Exception as e:
        logging.fatal(f"InstallError: {str(e)}, reinstall might be required")
        sys.exit(137707)
