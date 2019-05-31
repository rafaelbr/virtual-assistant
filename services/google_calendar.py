import datetime
import dateutil.parser
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/calendar.events']

class GoogleCalendarService:

    def __init__(self):
        self.credentials = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                self.credentials = pickle.load(token)

        self.doAuth()

        self.service = build('calendar', 'v3', credentials=self.credentials)

    def doAuth(self):
        if not self.credentials or not self.credentials.valid:
            if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                self.credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                self.credentials = flow.run_local_server()

            with open('token.pickle', 'wb') as token:
                pickle.dump(self.credentials, token)

    def createEvent(self, date, time, name):
        #create iso datetime format
        dt_str = date + ' ' + time
        dt_obj = datetime.datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')
        delta = datetime.timedelta(hours=1)
        dt_final = dt_obj + delta
        data = {
            'summary': name,
            'start': {
                'dateTime': dt_obj.isoformat(),
                'timeZone': 'America/Sao_Paulo'
            },
            'end': {
                'dateTime': dt_final.isoformat(),
                'timeZone': 'America/Sao_Paulo'
            }
        }
        #print(data)
        event = self.service.events().insert(calendarId='primary', body=data).execute()
        return event

    def getEvents(self, date):
        dt_start = date + 'T00:00:00-03:00'
        dt_end = date + 'T23:59:00-03:00'
        events_result = self.service.events().list(calendarId='primary', timeMin=dt_start, timeMax=dt_end,
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        data = {
            'date': date,
            'values': []
        }

        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            date_start = dateutil.parser.parse(start)
            summary = event['summary']
            data['values'].append(date_start.strftime('%H:%M') + " - " + summary)
        print(data)
        return data