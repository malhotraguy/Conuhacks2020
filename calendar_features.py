# calendar_features.py - conuhacks 2020 - 1/25/2020 - maxtheaxe
from __future__ import print_function
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import datetime
from dateutil.parser import *
import pickle
import os.path
import sys

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

# get_creds() basic creds grabber for testing, only supports one user
def get_creds(user_id = ''):
	creds = None
	# The file token.pickle stores the user's access and refresh tokens, and is
	# created automatically when the authorization flow completes for the first
	# time.
	token_name = "token-" + user_id + ".pickle"
	if os.path.exists(token_name):
		with open(token_name, 'rb') as token:
			creds = pickle.load(token)
	# If there are no (valid) credentials available, let the user log in.
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file(
				'credentials.json', SCOPES)
			creds = flow.run_local_server(port=0)
		# Save the credentials for the next run
		with open(token_name, 'wb') as token:
			pickle.dump(creds, token)
	return creds # return creds for later usage

# retrieve_calendar() takes creds as arg, retrieves calendar for the week 
# and returns it as list of dicts (each is one event)
def retrieve_calendar(creds):
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
	# returns list of events (each is a dict); upgrades dates to datetime objs
	return upgrade_calendar(events)

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
		if not (compare_day(start, end)): # skip multi-day events
			print ("Multi-day event, skipping")
			continue # move to next event
		if (compare_day(start, wanted_day)): # if the wanted day is the same as event
			refined_event_list.append(event) # add current event to event list
	return refined_event_list # return the new list of events (from only target day)

# compare_calendars() given two lists of events, returns availability (time w/o overlap)
# **considering 7 am the earliest possible volunteer time**
# list_a (1st arg) is charity calendar, uses given events as openings
# list_b (2nd arg) is employee calendar, uses spaces between events as openings
def compare_calendars(event_list_a, event_list_b):
	availability_times = [] # list of start and stops for available times to volunteer
	for event_a in event_list_a:
		# set start and end times for event_list_a
		event_a_start = event_a['start'].get('dateTime', event_a['start'].get('date'))
		event_a_end = event_a['end'].get('dateTime', event_a['end'].get('date'))
		# take date from event a obj and set time to 7am as earliest possible start
		# event_b_free_start = event_a_start.replace(minute=00, hour=07, second=00)
		# event_b_counter = 0 # go away, I know there's a better way
		event_b_start = event_a_start.replace(minute=0, hour=7, second=0)
		for event_b in event_list_b:
			availability_event = [] # list for individual availability event
			# set start and end times for event_list_b
			# event_b_start = event_b['start'].get('dateTime', event_b['start'].get('date'))
			# event_b_end = event_b['end'].get('dateTime', event_b['end'].get('date'))
			# # use prev end as start and current start as end, to get space between events
			# if event_b_counter == 0: # if it's the first event_b
			# 	event_b_start = event_b_free_start # use 7am as the first starting time
			# 	event_b_counter += 1 # increment the counter (doesn't even need it again)
			event_b_end = event_b['start'].get('dateTime', event_b['start'].get('date'))
			# flip start and end for b to get opposite (non-event times)
			# compare times to check for overlaps
			if event_a_start > event_b_end: # if the start of event_a after event_b end
				# set next start (stored outside loop) to current end
				event_b_start = event_b['end'].get('dateTime', event_b['end'].get('date'))
				continue # skip to the next event_b, don't bother checking start
			elif event_a_start > event_b_start: # if a starts after b, there is overlap
				availability_event.append(event_a_start) # add the start of the later event
				if event_a_end < event_b_end: # if a ends before b, use the end of a
					availability_event.append(event_a_end) # append to avail period
				else: # otherwise, use the end of b as the end of avail
					availability_event.append(event_b_end) # append to avail period
			elif event_a_end > event_b_start: # there is overlap, a starts first
				availability_event.append(event_b_start) # add the start of the later event
				if event_a_end < event_b_end: # if a ends before b, use the end of a
					availability_event.append(event_a_end) # append to avail period
				else: # otherwise, use the end of b as the end of avail
					availability_event.append(event_b_end) # append to avail period
			else: # event a ends before event b starts, there is no overlap
				# set next start (stored outside loop) to current end
				event_b_start = event_b['end'].get('dateTime', event_b['end'].get('date'))
				continue # skip to the next event b
			if (availability_event[0] != availability_event[1]):
				availability_times.append(availability_event) # append availability period to list
			# set next start (stored outside loop) to current end
			event_b_start = event_b['end'].get('dateTime', event_b['end'].get('date'))
	return availability_times # return list of availability periods

def main(argv):
	print("\n\t---DonateTime Calendar Manager Module---")
	if (len(argv) != 3):
		print("\tIncorrect syntax. Use: python calendar_features <user-id-a> <user-id-b>")
		return
	creds_employee = get_creds(argv[1]) # calls get_creds with userid 1 (cmd line arg)
	creds_charity = get_creds(argv[2]) # calls get_creds with userid 2 (cmd line arg)
	# retrieves calendar with employee creds from earlier
	calendar_employee = retrieve_calendar(creds_employee)
	# retrieves calendar with charity creds from earlier
	calendar_charity = retrieve_calendar(creds_charity)
	# print( "calendar_a:\n", calendar_a )
	# print( "\n\n\ncalendar_b:\n", calendar_b )
	wanted_day = datetime.datetime(2020, 1, 27) # new datetime obj (yr, mnth, day)
	test_day_employee = target_day(calendar_employee, wanted_day) # filter to just wanted_day
	test_day_charity = target_day(calendar_charity, wanted_day) # filter to just wanted_day
	openings = compare_calendars(test_day_charity, test_day_employee) # list of openings
	for open_period in openings:
		print("\nopen period:")
		print("\tstart: ", open_period[0])
		print("\tend: ", open_period[1])

if __name__ == '__main__':
	main(sys.argv)