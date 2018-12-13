import os
from flask import Flask, redirect, url_for, session, render_template, request, flash
from werkzeug.utils import secure_filename
from pvtranslator.models.utils.auth import google, get_user

upload_folder = '/path/to/the/uploads'

app = Flask(__name__)
app.debug = True
app.secret_key = 'development'
app.config['UPLOAD_FOLDER'] = upload_folder


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


@app.route('/upload_campaign', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        from pvtranslator.models.utils.zip_parser import allowed_file
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))