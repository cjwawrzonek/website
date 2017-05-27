#####################################################################
# Very basic flask app. Closely follows flaskr code.
#####################################################################
from flask import Flask, render_template, Response, g, redirect, url_for, \
	 flash

import io
import json
import os
import sqlite3

#####################################################################
# Configuration
#####################################################################
db_path = 'data/server.db'
flask_app = Flask('flaskapp')
flask_app.config.update(dict(
    DATABASE=os.path.join(flask_app.root_path, db_path),
    SECRET_KEY='secret-key',
    DEBUG=False
))

#####################################################################
# DB and data functions.
# TODO: Transfer to a Google Cloud PostgreSQL instance
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
	_db_add_post_entries()

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


def _gen_page_context(page):
	"""Generates the templating context for a given page load"""
	context = {}
	context['page'] = page
	return context

def _add_post_context(context, post_id):
	"""Adds the details of a specific post to the template context"""

	db = get_db()
	cur = db.execute('select title, prefix, summary, date from post_summaries where id={}'.format(post_id))
	post = cur.fetchall()

	context['post'] = post[0]

def _add_thumbnails(context):
	"""Adds a list of post/project thumbnails to the page context loaded from the db"""

	if context['page'] == "Projects":
		page_type = 'project'
	else:
		page_type = 'blog'

	db = get_db()
	cur = db.execute('select id, prefix, title, summary, thumbnail_img_url from post_summaries '\
					 'where type = ? order by id desc', [page_type])
	results = cur.fetchall()

	if context['page'] == "Projects":
		context['projects'] = results
	else:
		context['posts'] = results

def _db_add_post_entries():
	"""Adds a list of post summaries to the database"""

	with io.open('data/post_list.json', mode='r', encoding='utf-8') as json_file:    
		post_list = json.load(json_file)

	posts = post_list['posts']

	db = get_db()
	for post in posts:
		if 'thumbnail_img_url' not in post:
			img = 'img/empty.png'
		else:
			img = post['thumbnail_img_url']
		command='insert into post_summaries(type, title, prefix, summary, thumbnail_img_url, date) values(?, ?, ?, ?, ?, ?)'
		db.execute(command, [post['type'], post['title'], post['prefix'], post['summary'], img, post['date']])
	db.commit()

	print "Added post entries to post_summaries table."


#####################################################################
# URL routes
#####################################################################

@flask_app.route('/blog')
def blog_page():
	context = _gen_page_context('Blog')
	_add_thumbnails(context)
	return render_template('blog.html', context=context)


@flask_app.route('/contact')
def contact_page():
	context = _gen_page_context('Contact')
	return render_template('contact.html', context=context)


@flask_app.route('/')
@flask_app.route('/home')
def home_page():
	context = _gen_page_context('Home')
	return render_template('home.html', context=context)


# The URL for generating single posts or projects pages.
@flask_app.route('/post/<int:post_id>')
def post_page(post_id):
	context = _gen_page_context('Post')
	_add_post_context(context, post_id)
	return render_template('post.html', context=context)


@flask_app.route('/projects')
def projects_page():
	flash("test flash")
	context = _gen_page_context('Projects')
	_add_thumbnails(context)
	return render_template('projects.html', context=context)


@flask_app.route('/resume')
def resume_page():
	context = _gen_page_context('Resume')
	return render_template('resume.html', context=context)


@flask_app.route('/hello')
def hello_world():
	return Response(
		'Hello world!\n',
		mimetype='text/plain'
	)


#####################################################################
# Startup functions
#####################################################################
app = flask_app.wsgi_app
with flask_app.app_context():
	init_db()
