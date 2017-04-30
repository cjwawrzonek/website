from flask import Flask, render_template
from flask import Response
flask_app = Flask('flaskapp')

@flask_app.route('/')
@flask_app.route('/index.html')
def home_page():
    return render_template('index.html')

@flask_app.route('/hello')
def hello_world():
    return Response(
        'Hello world from Flask!\n',
        mimetype='text/plain'
    )

app = flask_app.wsgi_app