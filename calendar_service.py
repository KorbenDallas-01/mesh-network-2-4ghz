import json
import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from config import CALENDAR_SCOPES, GOOGLE_CREDENTIALS_FILE, TOKEN_FILE, TIMEZONE
import os


def get_calendar_service():
    """Sets up and returns a Google Calendar service object."""
    creds = None
    if os.path.exists(TOKEN_FILE):
        try:
            with open(TOKEN_FILE) as f:
                creds = Credentials.from_authorized_user_info(json.loads(f.read()), CALENDAR_SCOPES)
        except Exception as e:
            print(f"Error loading token: {e}")

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(GOOGLE_CREDENTIALS_FILE, CALENDAR_SCOPES)
            creds = flow.run_local_server(port=8080)

        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())

    return build('calendar', 'v3', credentials=creds)


def get_upcoming_events(service, max_results=10):
    """Retrieves upcoming events from the calendar."""
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    events_result = service.events().list(
        calendarId='primary', timeMin=now,
        maxResults=max_results, singleEvents=True,
        orderBy='startTime').execute()
    return events_result.get('items', [])


def create_event(service, summary, start_time, end_time, description=None, location=None):
    """Creates a new calendar event."""
    event = {
        'summary': summary,
        'location': location,
        'description': description,
        'start': {
            'dateTime': start_time,
            'timeZone': TIMEZONE,
        },
        'end': {
            'dateTime': end_time,
            'timeZone': TIMEZONE,
        }
    }
    try:
        return service.events().insert(calendarId='primary', body=event).execute()
    except HttpError as error:
        print(f"An error occurred: {error}")
        return None


def update_event(service, event_id, updates):
    """Updates an existing calendar event."""
    try:
        event = service.events().get(calendarId='primary', eventId=event_id).execute()

        for key, value in updates.items():
            if key in event:
                event[key] = value

        return service.events().update(calendarId='primary', eventId=event_id, body=event).execute()
    except HttpError as error:
        print(f"An error occurred: {error}")
        return None


def find_event_by_description(service, description):
    """Finds an event based on a partial description."""
    # Implementation would go here
    pass