from __future__ import print_function


from googleapiclient.discovery import build

from google.oauth2 import service_account

def init(id):
  global SPREADSHEET_ID,SCOPES,SERVICE_ACCOUNT_FILE,credentials
  SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
  SERVICE_ACCOUNT_FILE = 'keys.json'

  credentials = None
  credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
  SPREADSHEET_ID = id


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

def write():
    service = build('sheets', 'v4', credentials=credentials)

    # Call the Sheets API
    sheet = service.spreadsheets()
    request = sheet.values().append(
        spreadsheetId=SPREADSHEET_ID,
        range="data!a2",
        valueInputOption="USER_ENTERED",
        insertDataOption="INSERT_ROWS",
        body={
            "values":[
                ["e"]
            ]
        }
    )
    response = request.execute()

def build_sheet(studs):
  pass #TODO: make this


if __name__ == '__main__':
    #read()
    write()