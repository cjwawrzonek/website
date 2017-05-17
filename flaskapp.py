#####################################################################
# Very basic flask app. Closely follows flaskr code.
#####################################################################
from flask import Flask, render_template, Response, g, redirect, url_for, \
	 flash

import os
import io
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
    if os.path.isfile(flask_app.config['DATABASE']):
    	print "Using existing database file." 
    else:
    	db = get_db()
    	with flask_app.open_resource('data/schema.sql', mode='r') as f:
    		db.cursor().executescript(f.read())
	        db.commit()
		if flask_app.config['DEBUG'] == True:
			_db_add_test_entries()

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
	cur = db.execute('select title, summary, text from projects where id={}'.format(post_id))
	post = cur.fetchall()

	context['post'] = post[0]

def _add_project_thumbnails(context):
	"""Adds a list of project thumbnails to the page context loaded from the db"""

	db = get_db()
	cur = db.execute('select id, title, summary, thumbnail_img_url from projects order by id desc')
	projects = cur.fetchall()

	context['projects'] = projects

	print projects

def _db_add_test_entries():
	"""Adds a list of fale project thumbnails to the database for testing purposes"""

	with io.open('data/test_post.txt', mode='r', encoding='utf-8') as test_post:
	    test_text=test_post.read()

	project1 = {'title': 'A project', 'summary': 'Here is a brief summary of this project', 'text': test_text}
	project2 = {'title': 'Another', 'summary': 'Short summary.', 'thumbnail_img_url': 'img/thumbnails/net.png', 'text': test_text}
	project3 = {'title': 'Project Title', 'summary': 'Lorem ipsum dolor sit amet, consectetur'\
													 ' adipiscing elit. Nam viverra euismod odio,'\
													 ' gravida pellentesque urna varius vitae.'\
													 ' Lorem ipsum dolor sit amet, consectetur '\
													 'adipiscing elit. Nam viverra euismod odio,'\
													 ' gravida pellentesque urna varius vitae.', 'text': test_text}
	project4 = {'title': '2.1', 'summary': 'This is a medium length summary. This should '\
											'appear on multiple lines', 'text': test_text}
	project5 = {'title': 'A Brief Overview of Representational Similarity Analysis (RSA)',
				'summary': 'Lorem ipsum dolor sit amet, consectetur'\
													 ' adipiscing elit. Nam viverra euismod odio,'\
													 ' gravida pellentesque urna varius vitae.',
													 'thumbnail_img_url': 'img/net.png', 'text': test_text}

	projects = [project1, project2, project3, project4, project5]

	db = get_db()
	for project in projects:
		if 'thumbnail_img_url' not in project:
			img = 'img/empty.png'
		else:
			img = project['thumbnail_img_url']
		command='insert into projects(title, summary, thumbnail_img_url, text) values(?, ?, ?, ?)'
		db.execute(command, [project['title'], project['summary'], img, project['text']])
	db.commit()

	print "Added test entries to projects table."


#####################################################################
# URL routes
#####################################################################
# Looks pretty bad. Consider fixing later.
# @flask_app.route('/about.html')
# def about_page():
#     return render_template('about.html')


# Doesn't seem relevant anymore. Needs work.
# @flask_app.route('/columns.html')
# def columns_page():
#     return render_template('columns.html', page='Columns')


@flask_app.route('/blog')
def blog_page():
	context = _gen_page_context('Blog')
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
	_add_project_thumbnails(context)
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
