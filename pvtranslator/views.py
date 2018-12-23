from flask import Flask, redirect, url_for, session, render_template, request
from datetime import datetime
from pvtranslator.models.entities.campaign import Campaign
from pvtranslator.models.entities.curve import Curve
from pvtranslator.models.entity_managers import facade
from pvtranslator.models.utils.auth import get_user
from pvtranslator.models.entities.module import Module
from pvtranslator.models.utils.auth import google
from pvtranslator.models.utils.zip_parser import parse_zip

app = Flask(__name__)
app.debug = True
app.secret_key = 'development'


############################################
#             module functions             #
############################################


# template attributes:
#   modules -> required
#   user -> required
#   errors -> not required
@app.route('/', methods=['GET'])
def index():
    errors = request.args.get('errors')
    return render_template('index.html', modules=Module.all(), user=get_user(), errors=errors)


# form attributes:
#   module_key
@app.route('/delete/module/', methods=['POST'])
def delete_module():
    module_key = request.form.get('module_key')
    module = Module.get_by_key_name(key_names=module_key)
    if module:
        facade.delete_module(module)
    return redirect(url_for('index'))


# form attributes:
#   name
@app.route('/create/module/', methods=['POST'])
def create_module():
    name_module = request.form.get('name')
    errors = []
    if name_module:
        if facade.create_module(name_module) is None:
            errors.append('Cannot create module')
    else:
        errors.append('module name cannot be empty')
    return redirect(url_for('index', errors=errors))


# template attributes:
#   module -> required
@app.route('/edit/module/<module_key>', methods=['GET'])
def edit_module(module_key):
    module = Module.get_by_key_name(key_names=module_key)
    if module:
        return render_template('edit_module.html', module=module)


# form attributes:
#   name
#   module_key
@app.route('/save/module/', methods=['POST'])
def save_module():
    name = request.form.get('name')
    module_key = request.form.get('module_key')
    module = Module.get_by_key_name(key_names=module_key)
    module.name = name
    errors = facade.edit_module(module)
    return redirect(url_for('index', errors=errors))


############################################
#            /module functions             #
############################################


############################################
#            campaign functions            #
############################################

# template attributes:
#   campaigns -> required
#   module_key -> required
#   user -> required
#   errors -> not required
@app.route('/<module_key>/campaign/', methods=['GET'])
def index_campaigns(module_key):
    errors = request.args.get('errors')
    module = Module.get_by_key_name(key_names=module_key)
    campaigns = module.campaigns
    user = get_user()
    return render_template('index_campaign.html', campaigns=campaigns, module_key=module_key, user=get_user(), errors=errors)


# form attributes:
#   campaign_key
@app.route('/delete/campaign/', methods=['POST'])
def delete_campaign():
    campaign_key = request.form.get('campaign_key')
    campaign = Campaign.get_by_key_name(key_names=campaign_key)
    module_key = campaign.module.key().name()
    if campaign:
        facade.delete_campaign(campaign)
    return redirect(url_for('index_campaigns', module_key=module_key))


# template attributes:
#   campaign -> required
@app.route('/edit/campaign/<campaign_key>', methods=['GET'])
def edit_campaign(campaign_key):
    campaign = Campaign.get_by_key_name(key_names=campaign_key)
    if campaign:
        return render_template('edit_campaign.html', campaign=campaign)


# form attributes:
#   date
#   campaign_key
#   name
@app.route('/update/campaign/', methods=['POST'])
def save_campaign():
    date = request.form.get('date')
    name = request.form.get('name')
    campaign_key = request.form.get('campaign_key')
    campaign = Campaign.get_by_key_name(key_names=campaign_key)
    format_date = datetime.strptime(date, '%Y-%m-%d').date()
    campaign.date = format_date
    campaign.name = name
    errors = facade.edit_campaign(campaign)
    return redirect(url_for('index_campaigns', module_key=campaign.module.key().name(), errors=errors))


# form attributes:
#   date
#   name
#   key_module
@app.route('/create/campaign', methods=['POST'])
def save_new_campaign():
    errors = []
    name = request.form.get('name')
    date = request.form.get('date')
    key_module = request.form.get('key_module')
    module = Module.get_by_key_name(key_names=key_module)
    format_date = datetime.strptime(date, '%Y-%m-%d').date()
    if facade.create_campaign(name, format_date, module) is None:
        errors.append('Cannot create campaign')
    return redirect(url_for('index_campaigns', module_key=key_module, errors=errors))


# template attributes:
#   key_module -> required
#   errors -> not required
@app.route('/create/campaign/<key_module>', methods=['GET'])
def create_campaign(key_module):
    return render_template('create_campaign.html', key_module=key_module)


# form attributes:
#   file_campaigns
#   module_key
@app.route('/upload_campaign', methods=['POST'])
def upload_campaign():
    uploaded_file = request.files.get('file_campaigns')
    module_key = request.form.get('module_key')
    code, errors = parse_zip(uploaded_file, module_key)
    return redirect(url_for('index_campaigns', module_key=module_key, errors=errors))


############################################
#           /campaign functions            #
############################################


############################################
#              curve functions             #
############################################

@app.route('/module/campaign/curve/<curve_key>', methods=['GET'])
def draw_curve(curve_key):
    curve = Curve.get_by_key_name(key_names=curve_key)
    iv = [['Voltage', 'Intensity']]
    pv = [['Voltage', 'Potential']]
    for i in range(0, len(curve.i_values)):
        iv.append([curve.v_values[i], curve.i_values[i]])
        pv.append([curve.v_values[i], curve.p_values[i]])
    return render_template('grafica.html', iv=iv, pv=pv)


@app.route('/module/campaign/curves/<campaign_key>', methods=['GET'])
def show_curves(campaign_key):
    user = get_user()
    campaign = Campaign.get_by_key_name(campaign_key)
    return render_template('curves.html', campaign=campaign)


@app.route('/delete/curve/', methods=['POST'])
def delete_curve():
    campaign_key = request.form.get('campaign_key')
    facade.delete_curve(Curve.get_by_key_name(request.form.get('curve_key')))
    return redirect(url_for('show_curves', campaign_key=campaign_key))


############################################
#             /curve functions             #
############################################


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
