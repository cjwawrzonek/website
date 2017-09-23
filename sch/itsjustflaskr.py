#####################################################################
# basic flask app
#####################################################################
from flask import Flask, render_template, Response, g, redirect, url_for, \
	 flash, send_file, redirect, jsonify, request, abort

import io
import json
import os
import sqlite3

#####################################################################
# Configuration
#####################################################################
db_path = 'data/server.db'
flask_app = Flask('flaskserver')
flask_app.config.update(dict(
    DATABASE=os.path.join(flask_app.root_path, db_path),
    SECRET_KEY='secret-key',
    DEBUG=False
))

#####################################################################
# DB and data functions.
#####################################################################
def connect_db():
    rv = sqlite3.connect(flask_app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
	db = get_db()
	with flask_app.open_resource('data/schema.sql', mode='r') as f:
		db.cursor().executescript(f.read())
        db.commit()
	add_example_entries()

	print "Initialized sqlite db"


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context."""
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@flask_app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


def add_example_entries():
	"""Adds a list of appt examples to the database"""

	with io.open('data/appt_list.json', mode='r', encoding='utf-8') as json_file:    
		appt_list = json.load(json_file)

	appts = appt_list['appts']

	db = get_db()
	for appt in appts:
		command='insert into appointments(start, end, length, date) values(?, ?, ?, ?)'
		db.execute(command, [appt['start'], appt['end'], appt['length'], appt['date']])
	db.commit()

	print "Added appt entries to appointments table."


def execute(command):
	"""Open a connection, execute the command"""

	db = get_db()
	cur = db.execute(command)
	db.commit()
	return cur.fetchall()

def convert_to_dict(results, fields):
	if '*' in fields:
		fields = ['id', 'start', 'end', 'length', 'date']
	ret = []
	for row in results:
		item = {}
		for i in range(len(fields)): item[fields[i]] = row[i]
		ret.append(item)
	return ret

def get_command(fields, args={}, op='select'):
	command = [op]
	for _ in fields[:-1]: command.append('{},'.format(_))
	command.extend((fields[-1], 'from appointments'))
	if len(args) > 0:
		command.append('where')
		if 'id' in args:
			ids = args.get('id').split(',')
			ids = filter(None, ids)
			for _ in ids[:-1]: command.append('id={} or'.format(_))
			command.append('id={}'.format(ids[-1]))
		if 'order_by' in args:
			command.extend(('order by', args.get('order_by'), 'desc'))

	return ' '.join(command)

def get_insert_command(entries):
	command = ['insert into appointments(']
	numentries = len(entries)
	# assume each entry has the correct (same) number of fields
	for field in entries[0].keys()[:-1]: command.append('{},'.format(field))
	command.extend((str(entries[0].keys()[-1]), ') values'))

	# add a row for each entry
	for entry in entries:
		command.append('(')
		for value in entry.values()[:-1]:
			if isinstance(value, basestring):
				command.append('"{}",'.format(value))
			else:
				command.append('{},'.format(value))
		if isinstance(entry.values()[-1], basestring):		
			command.extend(('"{}"'.format(entry.values()[-1]), '),'))
		else:
			command.extend((str(entry.values()[-1]), '),'))
	# remove trailing comma
	command[-1] = ')'

	return ' '.join(command)

#####################################################################
# UI endpoints
#####################################################################

@flask_app.route('/all')
def contact_page():
	context = {'page': 'All'}
	return render_template('all.html', context=context)


@flask_app.route('/')
@flask_app.route('/home')
def home_page():
	context = {'page': 'Home'}
	return render_template('home.html', context=context)


@flask_app.route('/find')
def simple_page():
	context = {'page': 'Find'}
	return render_template('find.html', context=context)


@flask_app.route('/create')
def projects_page():
	context = {'page': 'Create'}
	return render_template('create.html', context=context)


@flask_app.route('/hello')
def hello_world():
	return Response(
		'Hello world!\n',
		mimetype='text/plain'
	)

#####################################################################
# REST Endpoints
#####################################################################
@flask_app.route('/api/appts', methods=['GET'])
def get_appts():
	fields = request.args.get('fields', None)
	fields = fields.split(',') if fields is not None else ['*']
	fields = filter(None, fields)
	command = get_command(fields, args=request.args)
	rows = execute(command)
	return jsonify(convert_to_dict(rows, fields))

# Create appt
@flask_app.route('/api/appts', methods=['POST'])
def post_appts():
	data = request.get_json(force=True)
	if data is not None or len(data) > 0:
		command = get_insert_command(data)
		result = execute(command)
	return jsonify(result)

# Delete appt
@flask_app.route('/api/appts', methods=['DELETE'])
def delete_appts():
	# not supported yet
	abort(400)
	return jsonify()

@flask_app.route('/api/appts/<int:appt_id>', methods=['GET'])
def get_appt(appt_id):
	fields = request.args.get('fields', None)
	fields = fields.split(',') if fields is not None else ['*']
	fields = filter(None, fields)
	command = get_command(fields, args={'id': '{}'.format(appt_id)})
	rows = execute(command)
	return jsonify(convert_to_dict(rows, fields))

@flask_app.route('/api/appts/<int:appt_id>', methods=['DELETE'])
def delete_appt(appt_id):
	# not supported yet
	abort(400)
	return jsonify()

#####################################################################
# Startup functions
#####################################################################
app = flask_app.wsgi_app
with flask_app.app_context():
	init_db()