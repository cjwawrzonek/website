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
	cur = db.execute('select title, prefix, summary from post_summaries where id={}'.format(post_id))
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

def _db_add_test_entries():
	"""Adds a list of test post summaries to the database for testing purposes"""

	with io.open('data/test_post.txt', mode='r', encoding='utf-8') as test_post:
	    test_text=test_post.read()

	post1 = {'type': 'blog', 'title': 'Insensitivity And The Nature Of Assumptions', 'thumbnail_img_url': 'img/thumbnails/assume.png',
	'summary': 'What are assumptions and when are they useful? Is it insensitive to ever assume something about a person\'s identity?'\
	' A conversation with a coworker prompted me to explore what it means to assume something about a person and when we should think'\
	' twice about it.', 'prefix': 'blog1'}
	post2 = {'type': 'project', 'title': 'Another', 'summary': 'Short summary.', 'thumbnail_img_url': 'img/thumbnails/net.png', 'prefix': 'test'}
	post3 = {'type': 'project', 'title': 'Project Title', 'summary': 'Lorem ipsum dolor sit amet, consectetur'\
													 ' adipiscing elit. Nam viverra euismod odio,'\
													 ' gravida pellentesque urna varius vitae.'\
													 ' Lorem ipsum dolor sit amet, consectetur '\
													 'adipiscing elit. Nam viverra euismod odio,'\
													 ' gravida pellentesque urna varius vitae.', 'prefix': 'test'}
	# post1 = {'title': '2.1', 'summary': 'This is a medium length summary. This should '\
	# 										'appear on multiple lines', 'text': test_text}
	# project5 = {'title': 'A Brief Overview of Representational Similarity Analysis (RSA)',
	# 			'summary': 'Lorem ipsum dolor sit amet, consectetur'\
	# 												 ' adipiscing elit. Nam viverra euismod odio,'\
	# 												 ' gravida pellentesque urna varius vitae.',
	# 												 'thumbnail_img_url': 'img/net.png', 'text': test_text}

	posts = [post1, post2, post3]

	db = get_db()
	for post in posts:
		if 'thumbnail_img_url' not in post:
			img = 'img/empty.png'
		else:
			img = post['thumbnail_img_url']
		command='insert into post_summaries(type, title, prefix, summary, thumbnail_img_url) values(?, ?, ?, ?, ?)'
		db.execute(command, [post['type'], post['title'], post['prefix'], post['summary'], img])
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
