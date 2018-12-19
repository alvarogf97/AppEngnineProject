from flask import Flask, redirect, url_for, session, render_template, request
from pvtranslator.models.utils.auth import get_user
from pvtranslator.models.entities.module import Module
from pvtranslator.models.utils.auth import google
from pvtranslator.models.utils.zip_parser import parse_zip

app = Flask(__name__)
app.debug = True
app.secret_key = 'development'


@app.route('/')
def index():
    user = get_user()
    modulos = Module.all()
    if user:
        return render_template('index.html', modulos=modulos, usuario=user)
    else:
        return render_template('index.html', modulos=modulos, usuario=user)

@app.route('/upload_campaign', methods=['POST'])
def upload_campaign():
    uploaded_file = request.files.get('file_campaigns')
    module_key = request.form.get('module_key')
    code, errors = parse_zip(uploaded_file, module_key)
    return render_template('index.html', msg=code, errors=errors)


############################################
#              login functions             #
############################################

@app.route('/login')
def login():
    callback = url_for('authorized', _external=True)
    return google.authorize(callback=callback)


@app.route('/logout')
def logout():
    session.pop('access_token', None)
    return redirect(url_for('index'))


@app.route('/oauth2callback')
@google.authorized_handler
def authorized(resp):
    access_token = resp['access_token']
    session['access_token'] = access_token, ''
    return redirect(url_for('index'))


@google.tokengetter
def get_access_token():
    return session.get('access_token')

############################################
#             /login functions             #
############################################
