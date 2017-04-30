from flask import Flask
from flask import Response
flask_app = Flask('flaskapp')

@flask_app.route('')
def hello_world():
    return Response(
        'Current under construction. We have top men working on it.\n',
        mimetype='text/plain'
    )

@flask_app.route('/hello')
def hello_world():
    return Response(
        'Hello world from Flask!\n',
        mimetype='text/plain'
    )

app = flask_app.wsgi_app