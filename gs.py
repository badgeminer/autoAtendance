# Auto Attendance
# google sheets intergration library

# imports
from __future__ import print_function 

import datetime
import logging

from google.oauth2 import service_account
from googleapiclient.discovery import build

#define functions

#init
def init(id):
  """sets up the google sheets api connection

    Args:
        id (spreadsheet id): used to pick google sheet
  """
  global SPREADSHEET_ID,SCOPES,SERVICE_ACCOUNT_FILE,credentials
  SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
  SERVICE_ACCOUNT_FILE = 'keys.json'

  credentials = None
  credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
  SPREADSHEET_ID = id

#UNUSED: read sheet
def read():
    service = build('sheets', 'v4', credentials=credentials)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                    range="data!a1:z300", majorDimension="COLUMNS").execute()
    values = result.get('values', [])

    if __name__ == '__main__':
        print(values)
    else:
        return values

#write to sheet
def write(built:dict):
    """appends built data to google sheet

    Args:
        built (dict): built google sheet data from build_sheet()
    """
    service = build('sheets', 'v4', credentials=credentials)

    # Call the Sheets API
    sheet = service.spreadsheets()
    request = sheet.values().append(
        spreadsheetId=SPREADSHEET_ID,
        range="data!A2:AE",
        valueInputOption="USER_ENTERED",
        insertDataOption="INSERT_ROWS",
        body=built
    )
    try:
        response = request.execute()
    except BaseException as e:
        logging.critical(str(e))

#build sheet row and write
def build_sheet(studs: dict()):
    """builds data into google sheet format and writes it

    Args:
        studs (dict): student data here / not here data from auto attendance
    """
    body={
            "values":[
                [str(datetime.date.today()),],
            ],
        }
    stds = list(studs.keys())
    stds.sort()
    for s in stds:
        body["values"][0].append(str(studs[s]))
    write(body)


#UNUSED: tests
if __name__ == '__main__':
    pass