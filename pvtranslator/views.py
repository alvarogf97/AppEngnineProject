import datetime
import json
import logging

from flask import Flask, redirect, url_for, session, render_template, request
from google.appengine.ext.db import DateProperty

from pvtranslator.models.entities.campaign import Campaign
from pvtranslator.models.entities.curve import Curve
from pvtranslator.models.entities.module import Module
from pvtranslator.models.entity_managers import facade
from pvtranslator.models.utils.auth import google, get_user
from pvtranslator.models.utils.zip_parser import parse_zip

app = Flask(__name__)
app.debug = True
app.secret_key = 'development'


@app.route('/')
def index():
    user = get_user()
    if user:
        """
        from pvtranslator.models.entity_managers.facade import create_module
        m = create_module(name="Modulo")
        from pvtranslator.models.entity_managers.facade import create_campaign
        c = create_campaign(name="Campanya", module=m, date=datetime.datetime(year=2018,month=1,day=19).date())
        from pvtranslator.models.entity_managers.facade import create_curve
        curva = create_curve(campaign=c, p_values=[1.0,3.0,5.0,7.0,9.0,11.0,13.0,15.0,17.0,19.0,21.0,23.0],
                             i_values=[1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,10.0,11.0,12.0],
                             v_values=[2.0,4.0,6.0,8.0,10.0,12.0,14.0,16.0,18.0,20.0,22.0,24.0],
                             hour="10")
        """

        return render_template('upload.html', module_key='test')
    else:
        return render_template("index.html", msg="I dont know who are you!")


@app.route('/upload_campaign', methods=['POST'])
def upload_campaign():
    uploaded_file = request.files.get('file_campaigns')
    module_key = request.form.get('module_key')
    code, errors = parse_zip(uploaded_file, module_key)
    return render_template('index.html', msg=code, errors=errors)


@app.route('/module/campaign/curve/<curve_key>', methods=['GET'])
def dibujar_curva(curve_key):
    curve = Curve.get_by_key_name(key_names=curve_key)
    iv = [['Voltage', 'Intensity']]
    pv = [['Voltage', 'Potential']]
    for i in range(0, len(curve.i_values)):
        iv.append([curve.v_values[i], curve.i_values[i]])
        pv.append([curve.v_values[i], curve.p_values[i]])
    return render_template('grafica.html', iv=iv, pv=pv)


@app.route('/module/campaign/curves/<campaign_key>', methods=['GET'])
def mostrar_curvas(campaign_key):
    campaign = Campaign.get_by_key_name(campaign_key)
    return render_template('curves.html', campaign=campaign)


@app.route('/module/campaign/curves/delete', methods=['POST'])
def borrar_curva():
    campaign = Campaign.get_by_key_name(request.form.get('campaign_key'))
    facade.delete_curve(Curve.get_by_key_name(request.form.get('curve_key')))
    return render_template('curves.html', campaign=campaign)


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
