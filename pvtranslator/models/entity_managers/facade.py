from google.appengine.ext import db
from pvtranslator.models.entities.campaign import Campaign
from pvtranslator.models.entities.curve import Curve
from pvtranslator.models.entities.module import Module
from pvtranslator.models.entities.user import User


def exists_module(module):
    key_name = module.name
    return Module.get_by_key_name(key_names=key_name) is not None


def exists_campaign(campaign):
    key_name = campaign.name + "_" + campaign.module.name
    return Campaign.get_by_key_name(key_names=key_name) is not None


def create_user(_id, email, name):
    user = User.get_or_insert(key_name=_id, id=_id, email=email, name=name)
    return user


def create_module(name):
    from pvtranslator.models.utils.auth import get_user
    user = get_user()
    if user:
        module = Module(key_name=name, name=name, user=user)
        if not exists_module(module):
            return module.put()
        else:
            return None
    else:
        return None


def delete_module(module):
    if module.has_permits:
        for campaign in module.campaigns:
            delete_campaign(campaign)
        db.delete(module)


def edit_module(module):
    errors = []
    if module.has_permits and not exists_module(module):
        campaigns = module.campaigns
        name = module.name
        new = create_module(name=name)
        for campaign in campaigns:
            campaign.module = new
            campaign.put()
        delete_module(module)
    else:
        errors.append('Cannot update module')
    return errors


def create_campaign(name, date, module):
    from pvtranslator.models.utils.auth import get_user
    user = get_user()
    if user:
        campaign = Campaign(key_name=name + "_" + module.name,
                            name=name, date=date, module=module, user=get_user())
        if not exists_campaign(campaign):
            campaign.put()
            campaign.put()
            return campaign
        else:
            return None
    else:
        return None


def delete_campaign(campaign):
    if campaign.has_permits:
        for curve in campaign.curves:
            delete_curve(curve)
        db.delete(campaign)


def edit_campaign(campaign):
    errors = []
    if campaign.has_permits and not exists_campaign(campaign):
        curves = campaign.curves
        name = campaign.name
        date = campaign.date
        module = campaign.module
        new = create_campaign(name=name, date=date, module=module)
        for curve in curves:
            curve.campaign = new
            curve.put()
        delete_campaign(campaign)
    else:
        errors.append('Cannot update campaign')
    return errors


def create_curve(hour, v_values, i_values, p_values, campaign):
    return Curve.get_or_insert(key_name=hour + "_" + campaign.name + "_" + campaign.module.name, hour=hour,
                               v_values=v_values, i_values=i_values, p_values=p_values, campaign=campaign)


def delete_curve(curve):
    if curve.campaign.has_permits():
        db.delete(curve)


def edit_curve(curve):
    if curve.campaign.has_permits():
        curve.put()
