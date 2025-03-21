import datetime
from django.utils.timezone import make_aware
from icalendar import Calendar, Event as ICalEvent

def generate_google_calendar_link(event):
    """Generates a Google Calendar link for an event."""
    start_time = make_aware(event.start_datetime).strftime("%Y%m%dT%H%M%SZ")
    end_time = make_aware(event.end_datetime).strftime("%Y%m%dT%H%M%SZ")
    
    google_calendar_link = (
        f"https://www.google.com/calendar/render?action=TEMPLATE"
        f"&text={event.name}&dates={start_time}/{end_time}"
        f"&details={event.description}&location={event.location}"
    )
    return google_calendar_link

def generate_ics_event(event):
    """Generates an .ics file for Outlook/Apple Calendar."""
    cal = Calendar()
    cal_event = ICalEvent()
    
    cal_event.add('summary', event.name)
    cal_event.add('dtstart', event.start_datetime)
    cal_event.add('dtend', event.end_datetime)
    cal_event.add('location', event.location)
    cal_event.add('description', event.description)
    
    cal.add_component(cal_event)
    return cal.to_ical()
