import boto3
import decimal
import json
from botocore.exceptions import ClientError
from google.oauth2.credentials import Credentials

dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2')
user_table = dynamodb.Table('Productivity-users')
groups_table = dynamodb.Table('Productivity-groups')

class DecimalEncoder(json.JSONEncoder):
	def default(self, o):
		if isinstance(o, decimal.Decimal):
			if abs(o) % 1 > 0:
				return float(o)
			else:
				return int(o)
		return super(DecimalEncoder, self).default(o)

def getUser(email):
	try:
		response = user_table.get_item(
				Key = {
					'email' : email
				}
			)
	except ClientError as e:
		print("Could not find email:", str(email))
		# print(e.response['Error']['Message'])
		response = None

	return response

def getUserCredentials(email):
	row = getUser(email)

	if row:
		item = row['Item']
		user_info = json.dumps(item, indent=4, cls=DecimalEncoder)
		credentials = json.loads(user_info)['credentials']
		token = credentials['user_token']
		refresh_token = credentials['refresh_token']
		token_uri = credentials['token_uri']

		return Credentials(
			token, 
			refresh_token=refresh_token, 
			token_uri=token_uri, 
			client_id='93007198174-9r3f7qjfr6p78nvd1l0hcp6b4gnfpeqd.apps.googleusercontent.com', 
			client_secret='YJXkhnmdgBx8yDp3Jt9dAXlc'
		)

	else:
		raise Exception()

def updateUser(email, credentials):
	update_dict = {
				'credentials' : {
					'user_token' : credentials.token,
					'refresh_token' : credentials.refresh_token,
					'token_uri' : credentials.token_uri
				}
			}	

	try:
		for key in update_dict:
			response = user_table.update_item(
							Key = {
								'email' : email
							},
							UpdateExpression = "set "+key+"=:i",
							ExpressionAttributeValues = {
								':i' : update_dict[key]
							}
						)
	except ClientError as e:
		print(e.response['Error']['Message'])

def getUserGroups(email):
	row = getUser(email)
	if row:
		item = row['Item']
		info = json.dumps(item, indent=4, cls=DecimalEncoder)
		if 'groups' in json.loads(info):
			groups = json.loads(info)['groups']
			return groups

	return None

def updateUserGroups(groups):
	try:
		response = user_table.update_item(
						Key = {
							'email' : email
						},
						UpdateExpression = "set groups=:i",
						ExpressionAttributeValues = {
							':i' : groups
						}
					)
		return True
	except ClientError as e:
		print(e.response['Error']['Message'])
		return False

def getGroupById(group_id):
	try:
		response = groups_table.get_item(
				Key = {
					'id' : group_id
				}
			)
	except ClientError as e:
		print(e.response['Error']['Message'])
		response = None

	if response:
		item = response['Item']
		info = json.dumps(item, indent=4, cls=DecimalEncoder)
		return json.loads(info)

	return None

def updateGroup(group):
	update_dict = {
		'group_name': group.name,
		'group_users': group.users,
		'group_tasks': group.tasks,
		'task_items': group.task_items
	}

	for key in update_dict:
		try:
			response = groups_table.update_item(
							Key = {
								'id' : group.group_id
							},
							UpdateExpression = "set "+key+"=:i",
							ExpressionAttributeValues = {
								':i' : update_dict[key]
							}
						)
		except ClientError as e:
			print(e.response['Error']['Message'])
