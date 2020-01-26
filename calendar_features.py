# calendar_features.py - conuhacks 2020 - 1/25/2020 - maxtheaxe
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import datetime
from dateutil.parser import *

# retrieve_calendar() takes creds as arg, retrieves calendar for the week 
# and returns it as list of dicts (each is one event)
def retrieve_calendar():
	service = build('calendar', 'v3', credentials=creds)
	# Call the Calendar API using today's date, retrieve next week
	now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
	week_later = (datetime.datetime.utcnow() + 
		datetime.timedelta(days=7)).isoformat() + 'Z' # adds 7 days to current date
	print('Retrieving events for the next week...')
	events_result = service.events().list(calendarId='primary', timeMin=now,
										timeMax=week_later, maxResults=200,
										singleEvents=True, orderBy='startTime').execute()
	events = events_result.get('items', [])
	if not events: # no upcoming events within next week
		print('No upcoming events found within the next week.')
	return events # returns list of events (each is a dict)

# parse_time() takes in unformatted time string (from gcal api) and returns datetime obj
def parse_time(time_string):
	return parse(time_string) # dateutil parses RFC 3339 string to datetime obj

# upgrade_calendar() given event list, converts all string dates to datetime objs, so it 
# doesn't need to be done repeatedly; would've rather done calendar and date classes
def upgrade_calendar(event_list):
	for event in event_list: # for each event in the list
		# set starting time to datetime obj
		event['start']['dateTime'] = parse_time(event['start']['dateTime']) # start time
		# set ending time to datetime obj
		event['end']['dateTime'] = parse_time(event['end']['dateTime']) # end time
	return event_list # return "upgraded" event list

# compare_day() compares the day of two datetime objects; returns boolean truth
def compare_day(day_a, day_b):
	return ( day_a.date() == day_b.date() ) # compares dates ONLY, not time

# target_day() returns list of events for target day, given a list of days and target
# default value for wanted_day is today
def target_day(event_list, wanted_day = datetime.datetime.utcnow()):
	refined_event_list = [] # final list for events
	for event in event_list: # for each event in the list
		start = event['start'].get('dateTime', event['start'].get('date')) # start time
		end = event['end'].get('dateTime', event['end'].get('date')) # end time
		if (compare_day(start, end)): # skip multi-day events
			print ("Multi-day event, skipping")
			continue # move to next event
		if (compare_day(start, wanted_day)): # if the wanted day is the same as event
			refined_event_list.append(event) # add current event to event list
	return refined_event_list # return the new list of events (from only target day)

# compare_calendars() given two lists of events, returns availability (time w/o overlap)
def compare_calendars(schedule_a, schedule_b):
	return