from flask import Flask, render_template, Response, redirect, url_for
flask_app = Flask('flaskapp')

###########################################
# URL routes
###########################################
# Doesn't seem relevant anymore. Needs work.
# @flask_app.route('/columns.html')
# def columns_page():
#     return render_template('columns.html', page='Columns')


@flask_app.route('/blog.html')
def blog_page():
    return render_template('blog.html', page='Blog')


@flask_app.route('/contact.html')
def contact_page():
    return render_template('contact.html', page='Contact')


@flask_app.route('/')
@flask_app.route('/home.html')
def home_page():
    return render_template('home.html', page='Home')


# Looks pretty bad. Consider adding later.
# @flask_app.route('/about.html')
# def about_page():
#     return render_template('about.html')


@flask_app.route('/resume.html')
def resume_page():
    return render_template('resume.html', page='Resume')


@flask_app.route('/hello')
def hello_world():
    return Response(
        'Hello world!\n',
        mimetype='text/plain'
    )


app = flask_app.wsgi_app
