from flask import Flask, request, abort
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView  
# from models import db, User, Role, Post
from datetime import datetime
import time


app = Flask(__name__)

# app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
# admin = Admin(app, name='messenger', template_mode='bootstrap3')
# admin.add_view(ModelView(User, db.session))
# admin.add_view(ModelView(Post, db.session))

# theese two messages are for test purposes
messages = [
    {
        'name': 'Jack',
        'text': 'Привет всем, я Jack',
        'time': 1614887855.3456457,
    },
    {
        'name': 'Mary',
        'text': 'Привет Jack, я - Mary',
        'time': 1614887857.3456457,
    }
]


@app.route('/')
def main():
    return 'Messenger'


@app.route('/status')
def status():
	return {
		'Status': True, 
		'Name': 'My_messenger', 
		'Current time': datetime.now().strftime('%d.%b %H:%M:%S'),
		'Total messages count': str(len(messages)),
		'Unique active users count': str(len(set([i['name'] for i in messages])))
		}

@app.route('/send', methods=['POST'])
def send_message():
	data = request.json
	if not isinstance(data, dict):
		return abort(400)
	name  = data.get('name')
	text = data.get('text')
	
	if not isinstance(name, str) or len(name) == 0:
		return abort(400)
	if not isinstance(text, str) or len(text) == 0 or len(text) > 1000:
		return abort(400)

	message = {
		'name': name,
		'text': text,
		'time': time.time()
	}
	messages.append(message)
	
	return {'ok': True}

@app.route('/messages')
def get_messages():
	try:
		after = float(request.args['after'])
	except:
		return abort(400)
	response = []
	for message in messages:
		if message['time'] > after:
			response.append(message)
	return {'messages': response[:50]}



	
# app.run(host='0.0.0.0', port=4567)
app.run()


