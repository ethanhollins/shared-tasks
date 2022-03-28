import uuid
import DBManager as db
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

class User(object):

	def __init__(self, email, credentials=None):
		self.email = email

		if credentials:
			self.credentials = credentials
		else:
			self.credentials = self._getUser(email)

		self.groups = self._getGroups(email)

		self.tasks_service = build('tasks', 'v1', credentials=self.credentials)
		self.calendar_service = build('calendar', 'v3', credentials=self.credentials)

	def _getUser(self, email):
		return db.getUserCredentials(email)

	def _getGroups(self, email):
		return db.getUserGroups(email)

	def createGroup(self, tasklist_id, users):
		if self.groups:
			for group in self.groups:
				if tasklist_id == self.groups[group][tasklist_id]:
					return

		group_id = uuid.uuid4().hex
		self.groups[group_id] = {'tasklist_id': tasklist_id}
		db.updateUserGroups(self.groups)

		new_group = {'id': group_id, 'users': users} 
		db.updateGroup(new_group)

	def addToGroup(self, group_id):
		group = db.getGroupById(group_id)
		group['users'][self.email] = {}

		db.updateGroup(group)

	def updateCredentials(self, credentials):
		self.credentials = credentials
		return db.updateUser(self.email, credentials)

	def getTasks(self, tasklist_id):
		return self.tasks_service.tasks().list(tasklist=tasklist_id).execute()

	def createTask(self, tasklist, title):
		task = {
			'title': title
		}

		result = service.tasks().insert(tasklist=tasklist, body=task).execute()

	def completeTask(self, tasklist, task_id):
		task = self.tasks_service.tasks().get(tasklist=tasklist, task=task_id).execute()
		task['status'] = 'completed'

		result = self.tasks_service.tasks().update(tasklist=tasklist, task=task_id, body=task).execute()

	def getTasksLists(self):
		return self.tasks_service.tasklists().list().execute()

	def createTaskList(self, title):
		tasklist = {
			'title': title
		}

		return self.tasks_service.tasklists().insert(body=tasklist).execute()

	def getCalendarLists(self):
		calendar_list = self.calendar_service.calendarList().list().execute()

		calendar = self.calendar_service.calendars().get(calendarId='primary').execute()
		# print(calendar)

		settings = self.calendar_service.settings().list().execute()
		# print(settings)

		events = self.calendar_service.events().list(calendarId='primary').execute()
		print(events)

		for i in calendar_list['items']:
			if 'summary' in i:
				pass
				# print(i['summary'])
			if 'id' in i:
				# print(i['id'])
				# print(self.calendar_service.calendars().get(calendarId=i['id']).execute())

				events = self.calendar_service.events().list(calendarId=i['id']).execute()
				print(events)
				print('-------------')
				pass


		return self.calendar_service.calendarList().list().execute()
