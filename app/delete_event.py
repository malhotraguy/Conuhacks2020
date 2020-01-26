# Script to delete events from google calendar
from googleapiclient import errors

from app.cal_setup import get_calendar_service


def main(event_id):
    # Delete the event
    service = get_calendar_service()
    try:
        service.events().delete(
            calendarId='primary',
            eventId=event_id,
        ).execute()
    except errors.HttpError:
        print("Failed to delete event")

    print("Event deleted")


if __name__ == '__main__':
    main(event_id="as7nt7nn5d279gteo550js9jq0")
