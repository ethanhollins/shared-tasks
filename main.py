from __future__ import print_function
import boto3
import decimal
import json
import time
from botocore.exceptions import ClientError
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from oauth2client.client import flow_from_clientsecrets
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from User import User
from Group import Group
import Constants
import DBManager as db

class DecimalEncoder(json.JSONEncoder):
	def default(self, o):
		if isinstance(o, decimal.Decimal):
			if abs(o) % 1 > 0:
				return float(o)
			else:
				return int(o)
		return super(DecimalEncoder, self).default(o)

# If modifying these scopes, delete the file token.pickle.
SCOPES = [
		'https://www.googleapis.com/auth/tasks', 
		'https://www.googleapis.com/auth/calendar'
	]
CLIENT_SECRETS = 'client_secret_93007198174-4si4vd51gtmc37pbr9tstgcf6enkk0r1.apps.googleusercontent.com.json'

users = []

def main():
	"""Shows basic usage of the Tasks API.
	Prints the title and ID of the first 10 task lists.
	"""
	user_ethan = User('ethanjohol@gmail.com')
	users.append(user_ethan)
	group = Group(findUser, 'f9ff0f95f0094a328255f1dbde563f53')
	# user.updateCredentials(user.credentials)
	group.runTasks()
	# while True:



	# 	time.sleep(5)


def findUser(email):
	for user in users:
		if user.email == email:
			return user

	return None

	# The file token.pickle stores the user's access and refresh tokens, and is
	# created automatically when the authorization flow completes for the first
	# time.
	# if os.path.exists('token.pickle'):
	# 	with open('token.pickle', 'rb') as token:
	# 		creds = pickle.load(token)
	# If there are no (valid) credentials available, let the user log in.
	# if not creds or not creds.valid:
	# 	if creds and creds.expired and creds.refresh_token:
	# 		creds.refresh(Request())
	# 	else:
	# flow = InstalledAppFlow.from_client_secrets_file(
	# 	CLIENT_SECRETS, SCOPES)
	# creds = flow.run_local_server()

	# print(creds.token)
	# print(creds.refresh_token)
	# print(creds.token_uri)
			# flow = flow_from_clientsecrets(CLIENT_SECRETS,
			# 			   scope='https://www.googleapis.com/auth/tasks',
			# 			   redirect_uri='https://localhost:8080/')
			# auth_uri = flow.step1_get_authorize_url()
			# print(auth_uri)

			# creds = flow.step2_exchange('4/7wCd4VZvYFucXePuZU42T_rNelLqE0wD9v-RFKildr6PUqlMZZiv2dLs0JaSf9RRAe8X7xbwAcsxWeIIkV_XMls')
		# Save the credentials for the next run
		# with open('token.pickle', 'wb') as token:
		# 	pickle.dump(creds, token)

	# print(creds.token)
	# service = build('tasks', 'v1', credentials=creds)

	# tasklist = {
	# 	'title': 'New Task List'
	# 	}

	# result = service.tasklists().insert(body=tasklist).execute()
	# print(result['id'])

	# Call the Tasks API

	# tasklists = service.tasklists().list().execute()

	# for tasklist in tasklists['items']:
	# 	print(tasklist['title'])

	# 	tasks = service.tasks().list(tasklist=tasklist['id']).execute()

	# 	if 'items' in tasks:
	# 		for task in tasks['items']:
	# 			print(task)
	# 			print(task['title'])

	# results = service.tasklists().list(maxResults=10).execute()
	# items = results.get('items', [])

	# if not items:
	# 	print('No task lists found.')
	# else:
	# 	print('Task lists:')
	# 	for item in items:
	# 		# print(u'{0} ({1})'.format(item['title'], item['id']))
	# 		print(item['title'] + str(':'))
	# 		tasklist = service.tasklists().get(tasklist=item['id']).execute()

	# 		print(tasklist)

# def getUserCredentials(email):

	# if not creds or not creds.valid:
	# 	if creds and creds.expired and creds.refresh_token:
	# 		creds.refresh(Request())
	# 	else:
	# 		flow = InstalledAppFlow.from_client_secrets_file(
	# 			CLIENT_SECRETS, SCOPES)
	# 		creds = flow.run_local_server()

	# service = build('tasks', 'v1', credentials=creds)

	# tasklists = service.tasklists().list().execute()

	# for tasklist in tasklists['items']:
	# 	print(tasklist['title'])

	# 	tasks = service.tasks().list(tasklist=tasklist['id']).execute()

	# 	if 'items' in tasks:
	# 		for task in tasks['items']:
	# 			print(task)
	# 			print(task['title'])

if __name__ == '__main__':
	main()
	# getUserCredentials('ethanjohol@gmail.com')