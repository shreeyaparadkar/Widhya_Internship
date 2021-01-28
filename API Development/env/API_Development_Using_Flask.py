#importing required packages

from flask import Flask, jsonify, abort, make_response, request, url_for
from flask_httpauth import HTTPBasicAuth

#app installation

app = Flask(__name__)

#security

auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
	if username == 'admin':
		return 'admin@123'
	return None

@auth.error_handler
def unauthorized():
	return make_response(jsonify({'error': 'Unauthorized access'}), 403)

#task dictionaries

tasks = [
	{
		'id': 1,
		'title': u'Buy Clothes',
		'description': u'Shirt, Jeans, T-Shirt, Top, Leggings',
		'done': False
	},
	{
		'id': 2,
		'title': u'Learn Music',
		'description': u'Need to identify a good Music tutorial on the web'
		'done': False
	}
]

#functions

def make_public_task(task):
	new_task = {}
	for field in task:
		if field =='id':
			new_task['uri'] = url_for('get_task', task_id = task['id'], _external = True)
		else:
			new_task[field] = task[field]
	return new_task

#routing
#using get method

@app.route('/', methods = ['GET'])
@auth.login_required
def get_tasks():
	return jsonify({'tasks': [make_public_task(task) for task  in tasks]})

@app.route('/<int: task_id>', methods = ['GET'])
def get_task(task_id):
	task = [task for task in tasks if task['id'] == task_id]
	if len(task) == 0:
		abort(404)
	return jsonify({'task': task[0]})

#error handler

app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'Not found'}), 404)

#using post method

@app.route('/', methods = ['POST'])
def create_task():
	if not request.json or not 'title' in  request.json:
		abort(400)
	task = {
		'id': tasks[-1]['id']+1,
		'title': request.json['title'],
		'description': request.json.get('description', ""),
		'done': False
	}
	tasks.append(task)
	return jsonify({'task': task}), 201

#for updating task using put method
@app.route('//<int: task_id>', methods = ['PUT'])
def update_task(task_id):
	task = [task for task in tasks if task['id'] == task_id]
	if len(task) == 0:
		abort(404)
	if not request.json:
		abort(400)
	if 'title' in request.json and type(request.json['title']) != unicode:
		abort(400)
	if 'description' in request.json and type(request.json['description']) is not unicode:
		abort(400)
	if 'done' in request.json and type(request.json['done']) is not bool:
		abort(400)
	task[0]['title'] = request.json.get('title', task[0]['title'])
	task[0]['description'] = request.json.get('description', task[0]['description'])
	task[0]['done'] = request.json.get('done', task[0][done])
	return jsonify({'task': task[0]})

#using delete method
@app.route('/<int: task_id>', methods = ['DELETE'])
def delete_task(task_id):
	task = [task for task in tasks if task['id'] == task_id]
	if len(task) == 0:
		abort(404)
	tasks.remove(task[0])
	return jsonify({'result': True})

if __name__ == '__main__':
	app.run(debug = True)