from datetime import datetime
import os.path
import sys
import dotenv

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar','https://www.googleapis.com/auth/sqlservice.admin']

#
def authorize(name):
    global service, creds, CALID

    dotenv.load_dotenv()
    CALID = eval(os.environ.get('CALID'))[name]

    creds = service_account.Credentials.from_service_account_file("credentials.json", scopes=SCOPES)
    service = build('calendar', 'v3', credentials=creds)


def add_event(courseID,s,e,location):
    start = datetime.strptime(s, "%d.%m.%Y %H:%M")
    start = start.isoformat()
    end = datetime.strptime(e, "%d.%m.%Y %H:%M")
    end = end.isoformat()
    event = { 'summary': courseID,'location':location, 'start':{'dateTime': start,'timeZone':'Europe/Berlin'},'end':{'dateTime':end,'timeZone':'Europe/Berlin'}}

    event_result = service.events().insert(calendarId=CALID, body=event).execute()
    return event_result

def add_to_calendar(data):
        name = data["name"]
        courseID = data["courseID"]
        start = data["start"]
        end = data["end"]
        location = data["location"]

        authorize(name)

        add_event(courseID,start,end,location)

# if __name__ == '__main__':
#     add_to_calendar()
