from flask import Flask, redirect, url_for, session, render_template
from pvtranslator.models.auth import google, get_user

app = Flask(__name__)
app.debug = True
app.secret_key = 'development'


@app.route('/')
def index():
    user = get_user()
    if user:
        return render_template("index.html",msg=user)
    else:
        return render_template("index.html", msg="I dont know who are you!")


@app.route('/login')
def login():
    callback = url_for('authorized', _external=True)
    return google.authorize(callback=callback)


@app.route('/oauth2callback')
@google.authorized_handler
def authorized(resp):
    access_token = resp['access_token']
    session['access_token'] = access_token, ''
    return redirect(url_for('index'))


@google.tokengetter
def get_access_token():
    return session.get('access_token')