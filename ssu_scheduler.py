import requests
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import argparse
from argparse import RawTextHelpFormatter
import datetime
import pickle
import os.path
import json


SCOPES = ['https://www.googleapis.com/auth/calendar']
#TODO: Create faculties dictionary: faculty - full faculty name

def parse_input_arguments():
	#TODO: Add lesson recurrence argument
    parser = argparse.ArgumentParser(
        description='SSU Scheduler for Google Calendar', formatter_class=RawTextHelpFormatter)
    parser.add_argument(
        '-f',
        '--faculty',
        required=True,
        dest='faculty',
        #TODO: add all faculties
        help='Faculty of SSU \n' 
        	'List of faculties: \n'
        	'knt - Факультет компьютерных наук и информационных технологий \n'
        	'mm - Механико-математический факультет \n'
        	'fnp - Факультет нелинейных процессов',
        type=str
        )
    parser.add_argument(
        '-g',
        '--group',
        required=True,
        dest='group',
        help='group number',
        type=int
        )
    return parser.parse_args()

def auth_google():
	creds = None
	if os.path.exists('token.pickle'):
		with open('token.pickle', 'rb') as token:
			creds = pickle.load(token)
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file(
				'client_id.json', SCOPES)
			creds = flow.run_local_server(port=0)
		with open('token.pickle', 'wb') as token:
			pickle.dump(creds, token)
	service = build('calendar', 'v3', credentials=creds)
	return service

def get_nearest_monday(date):
	while date.weekday() != 0:
		date += datetime.timedelta(1)
	return date

def make_event_json(lesson, location, color, start, end):
	event = {
  		'summary': lesson,
  		'location': location,
  		'colorID': color,
  		'start': {
    		'dateTime': start,
    		'timeZone': 'Europe/Samara',
  		},
  		'end': {
    		'dateTime': end,
    		'timeZone': 'Europe/Samara',
  		}

	}
	return event

def prepare_schedule_calendar(calendar_name):
	#TODO: Add faculty name and group number in summary
	calendar_json = {
		'summary': calendar_name,
		'timeZome': 'Europe/Samara'
	}

	page_token = None
	calendar_list = []
	while True:
		calendar_list = service.calendarList().list(pageToken=page_token).execute()
		page_token = calendar_list.get('nextPageToken')
		if not page_token:
			break

	calendar_id = None
	for calendar_list_entry in calendar_list['items']:
		if calendar_list_entry['summary'] == calendar_name:
			calendar_id = calendar_list_entry['id']
			break
	if calendar_id == None:
		schedule_calendar = service.calendars().insert(body=calendar_json).execute()
		calendar_id = schedule_calendar['id']

	event_list = []
	page_token = None
	while True:
		event_list = service.events().list(calendarId=calendar_id, pageToken=page_token).execute()
		page_token = event_list.get('nextPageToken')
		if not page_token:
			break

	for event in event_list['items']:
		if datetime.datetime.strptime(event['start']['dateTime'][:-1], '%Y-%m-%dT%H:%M:%S').date() >= nearest_monday:
			service.events().delete(calendarId=calendar_id, eventId=event['id']).execute()

	return calendar_id


def get_lessons(request_response):
	json_data = json.loads(request_response.text)['lessons']
	week_lessons = []
	for i in range(len(json_data)):
		lesson_name = json_data[i]['name']
		lesson_place = json_data[i]['place']
		lesson_start_time = datetime.datetime.strptime(json_data[i]['lessonTime']['timeStart'], '%H:%M').time()
		lesson_end_time = datetime.datetime.strptime(json_data[i]['lessonTime']['timeFinish'], '%H:%M').time()

		lesson_day_number = json_data[i]['day']['dayNumber']

		lesson_start_datetime = datetime.datetime.combine(nearest_monday + datetime.timedelta(lesson_day_number - 1), lesson_start_time)
		lesson_end_datetime = datetime.datetime.combine(nearest_monday + datetime.timedelta(lesson_day_number - 1), lesson_end_time)

		lesson_start = lesson_start_datetime.strftime('%Y-%m-%dT%H:%M:%S')
		lesson_end = lesson_end_datetime.strftime('%Y-%m-%dT%H:%M:%S')

		if json_data[i]['lessonType'] == 'PRACTICE':
			lesson_color = '#5484ed'
		elif json_data[i]['lessonType'] == 'LECTURE':
			lesson_color = '#dc2127'
		week_lessons.append(make_event_json(lesson_name, lesson_place, lesson_color, lesson_start, lesson_end))
	return week_lessons


if __name__ == '__main__':
	#TODO: Delete schedule for particular group(if exists)
	service = auth_google()

	nearest_monday = get_nearest_monday(datetime.date.today())

	input_args = parse_input_arguments()

	url = 'https://scribabot.tk/api/v1.0/schedule/full/{0}/{1}'.format(input_args.faculty, input_args.group)
	request_response = requests.get(url)
	calendar_name = 'Расписание СГУ'
	week_lessons = get_lessons(request_response)
		
	cal_id = prepare_schedule_calendar(calendar_name)
	#for i in range(len(week_lessons)):
	#	service.events().insert(calendarId=cal_id, body=week_lessons[i]).execute()
		

