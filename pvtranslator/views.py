from flask import Flask, render_template
from pvtranslator.models.db_helper import gen_connection_string

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = gen_connection_string()


@app.route('/')
def index():
    msg = "hello world :)"
    return render_template('index.html', msg=msg)