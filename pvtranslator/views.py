from flask import render_template, Flask
app = Flask(__name__)


@app.route('/')
def index():
    msg = "hello world :)"
    return render_template('index.html', msg=msg)