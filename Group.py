import Constants
import DBManager as db
from enum import Enum

class TaskAction(Enum):
	ADD = 0
	REMOVE = 1
	COMPLETE = 2
	UPDATE = 3

class Group(object):

	def __init__(self, findUser, group_id):
		self.findUser = findUser
		self.group_id = group_id
		self._getProperties()

	def _getProperties(self):
		result = db.getGroupById(self.group_id)
		self.name = result['group_name']
		self.users = result['group_users']
		self.tasks = result['group_tasks']
		self.task_items = result['task_items']

	def _getTaskItems(self):
		return ['task_items']

	def runTasks(self):
		for t in self.tasks:
			if t == Constants.SHARE_ALL_TASKS:
				self.shareTasks()

	def shareTasks(self):

		user_tasks = {}
		group_tasklist = None

		for user in self.users:
			user_obj = self.findUser(user)
			user_tasks[user_obj.email] = None
			taskslists = user_obj.getTasksLists()

			for tasklist in taskslists['items']:
				if tasklist['title'] == self.name:

					group_tasklist = tasklist

					tasks = user_obj.getTasks(tasklist['id'])

					task_items = []
					if 'items' in tasks:
						task_items = tasks['items']

					user_tasks[user_obj.email] = task_items


		for user in user_tasks:
			if user_tasks[user] == None:
				user_obj = self.findUser(user)
				group_tasklist = user_obj.createTaskList(self.name)
				user_tasks[user] = []

		print(user_tasks['ethanjohol@gmail.com'])

		actions = []

		for user in user_tasks:
			user_tasks = user_tasks[user]

			user_tasks_titles = [i['title'] for i in user_tasks]
			print(user_tasks_titles)

			group_tasks_titles = [i['title'] for i in self.task_items]
			print(group_tasks_titles)

			added = list(set(user_tasks_titles) - set(group_tasks_titles))
			subtracted = list(set(group_tasks_titles) - set(user_tasks_titles))

			for add in added:
				for task in user_tasks:
					if task['title'] == add:
						task = task

				action_found = False
				for action in actions:
					if action['action'] == TaskAction.ADD and action['task']['title'] == task['title']:
						action['emails'].append(user)
						action_found = True

				if not action_found:
					actions.append({'action': TaskAction.ADD, 'emails': [user], 'task': task})				

			for sub in subtracted:
				for task in group_tasks_titles:
					if task['title'] == sub:
						task = task

				action_found = False
				for action in actions:
					if action['action'] == TaskAction.ADD and action['task']['title'] == task['title']:
						action['emails'].append(user)
						action_found = True

				if not action_found:
					actions.append({'action': TaskAction.COMPLETE, 'emails': [user], 'task': task})
				

		print(actions)
		for action in actions:
			for user in self.users:
				if not user in action['emails']:
					user_obj = self.findUser(user)

					if action['action'] == TaskAction.ADD:
						user_obj.createTask(group_tasklist, action['task']['title'])
					elif action['action'] == TaskAction.COMPLETE:
						user_obj.completeTask(group_tasklist, action['task']['id'])#!!
		# for k,v in user_tasks:
		# 	for i,j in user_tasks:
				
		# 		if k == i or set(v) == set(j):
		# 			continue

				


				