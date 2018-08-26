from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
import httplib2

from datetime import datetime, timedelta


class GoogleCalendar:

    LOUNGE_CALENDAR_ID = "jbt1onapg3ffroh27umi9qm4ic@group.calendar.google.com"
    BBQ_CALENDAR_ID = "tjsllo1pojk4tpcp40l8pinseg@group.calendar.google.com"
    ACCOUNT_EMAIL="117593083049-h1pupclppqu21eepcskepfabsu2ghh15@developer.gserviceaccount.com"
    KEY_FILE="key.p12"
    SCOPES=['https://www.googleapis.com/auth/calendar']
    TIMEZONE="America/New_York"

    @staticmethod
    def which_calendar(calendar_name):
        return GoogleCalendar.LOUNGE_CALENDAR_ID if calendar_name is "lounge" else GoogleCalendar.BBQ_CALENDAR_ID

    def __init__(self):
        # login

        credentials = ServiceAccountCredentials.from_p12_keyfile(
                GoogleCalendar.ACCOUNT_EMAIL,
                GoogleCalendar.KEY_FILE,
                scopes=GoogleCalendar.SCOPES
        )
        http = httplib2.Http()

        credentials.authorize(http)

        if not credentials.access_token:
            credentials.refresh(http)

        self.service = build("calendar","v3", http=http)

    def add_event(self, event_title, calendar_id, start, end, timezone=TIMEZONE):

        start = start.isoformat("T")
        end = end.isoformat("T")

        event= {
                "summary" : event_title,
                "start" : {
                    "dateTime" : start,
                    "timeZone" : timezone
                },
                "end" : {
                    "dateTime" : end,
                    "timeZone" : timezone
                }
        }
        
        result = self.service.events().insert(
                calendarId = GoogleCalendar.which_calendar(calendar_id),
                body = event
        ).execute()

        return result.get('id')

    def delete_event(self, calendar_id, event_id):

        self.service.events().delete(
                calendarId = GoogleCalendar.which_calendar(calendar_id),
                eventId = event_id
                ).execute()

    def list_events(self, calendar_id, time_min, time_max):

        time_min = time_min.isoformat("T")
        time_max = time_max.isoformat("T")

        collection = self.service.events().list(
                calendarId = GoogleCalendar.which_calendar(calendar_id),
                timeMin = time_min,
                timeMax = time_max,
                ).execute()

        return collection.get('items')

if __name__ == "__main__":
    calendar = GoogleCalendar()

    test = datetime(2018,8,24,4,0,0)
    one_hour_ago = test - timedelta(hours = 1)
    
    middle = datetime(2018,8,24,3,30,0)
    one_minute = middle + timedelta(minutes = 1)

    result = calendar.add_event("[fake event] test", "lounge", one_hour_ago, test)

    result = [ e.get("id") for e in calendar.list_events("lounge", middle, one_minute)]

    [calendar.delete_event("lounge", id) for id in result]


