from flask import Flask, redirect, url_for, session, render_template, request
from pvtranslator.models.entities.campaign import Campaign
from pvtranslator.models.entity_managers import facade
from pvtranslator.models.utils.auth import get_user
from pvtranslator.models.entities.module import Module
from pvtranslator.models.utils.auth import google
from pvtranslator.models.utils.zip_parser import parse_zip

app = Flask(__name__)
app.debug = True
app.secret_key = 'development'


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', modules=Module.all(), user=get_user())


@app.route('/module/<module_key>', methods=['GET'])
def view_module(module_key):
    module = Module.get_by_key_name(key_names=module_key)
    campaigns = module.campaigns
    return render_template('viewModule.html', campaigns=campaigns, module_key=module_key)


@app.route('/delete_module/<module_key>', methods=['GET'])
def delete_module(module_key):
    module = Module.get_by_key_name(key_names=module_key)
    if module:
        facade.delete_module(module)
    return redirect(url_for('index'))


@app.route('/create_module', methods=['POST'])
def create_module():
    name_module = request.form.get('name')
    facade.create_module(name_module)
    return redirect(url_for('index'))


@app.route('/edit_module/<module_key>', methods=['GET'])
def edit_module(module_key):
    module = Module.get_by_key_name(key_names=module_key)
    if module:
        return render_template('editModule.html', module=module)


@app.route('/save_module', methods=['POST'])
def save_module():
    from pvtranslator.models.entities.user import User
    name = request.form.get('name')
    user_name = request.form.get('user')
    module = Module.get_by_key_name(key_names=name)
    user = User.all()
    user.filter('email =', user_name)
    # Esta mal
    if module and user:
        module.user = user
        module.put()
    return redirect(url_for('index'))


@app.route('/delete_campaign/<campaign_key>', methods=['GET'])
def delete_campaign(campaign_key):
    campaign = Campaign.get_by_key_name(key_names=campaign_key)
    name = campaign.module.name
    if campaign:
        facade.delete_module(campaign)
    return redirect(url_for('view_module', module_key=name))


@app.route('/edit_campaign/<campaign_key>', methods=['GET'])
def edit_campaign(campaign_key):
    campaign = Campaign.get_by_key_name(key_names=campaign_key)
    if campaign:
        return render_template('editCampaign.html', campaign=campaign)


@app.route('/save_campaign/', methods=['POST'])
def save_campaign():
    name = request.form.get('name')
    date = request.form.get('date')
    moduleName = request.form.get('module')
    userName = request.form.get('user')
    #Seguir con esto
    return redirect(url_for('index'))


@app.route('/upload_campaign', methods=['POST'])
def upload_campaign():
    uploaded_file = request.files.get('file_campaigns')
    module_key = request.form.get('module_key')
    code, errors = parse_zip(uploaded_file, module_key)
    return redirect(url_for('view_module', module_key=module_key))


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
