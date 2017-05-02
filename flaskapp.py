from flask import Flask, render_template
from flask import Response
flask_app = Flask('flaskapp')

###########################################
# URL routes
###########################################
@flask_app.route('/columns.html')
def columns_page():
    return render_template('columns.html')


@flask_app.route('/contact.html')
def contact_page():
    return render_template('contact.html')


@flask_app.route('/')
@flask_app.route('/home.html')
def home_page():
    return render_template('home.html')


@flask_app.route('/about.html')
def about_page():
    return render_template('about.html')


@flask_app.route('/resume.html')
def resume_page():
    return render_template('resume.html')



@flask_app.route('/hello')
def hello_world():
    return Response(
        'Hello world!\n',
        mimetype='text/plain'
    )

app = flask_app.wsgi_app