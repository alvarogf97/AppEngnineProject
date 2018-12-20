from google.appengine.ext import db
from pvtranslator.models.entities.campaign import Campaign
from pvtranslator.models.entities.curve import Curve
from pvtranslator.models.entities.module import Module
from pvtranslator.models.entities.user import User


def create_user(_id, email, name):
    user = User.get_or_insert(key_name=_id, id=_id, email=email, name=name)
    return user


def create_module(name):
    from pvtranslator.models.utils.auth import get_user
    user = get_user()
    if user:
        db_module = Module.get_by_key_name(key_names=name)
        if db_module:
            return None
        else:
            module = Module(key_name=name, name=name, user=user)
            module.put()
            return module
    else:
        return None


def delete_module(module):
    if module.has_permits:
        db.delete(module)


def edit_module(module):
    if module.has_permits:
        module.put()


def create_campaign(name, date, module):
    from pvtranslator.models.utils.auth import get_user
    user = get_user()
    if user:
        db_campaign = Campaign.get_by_key_name(key_names=name + "_" + module.name)
        if db_campaign:
            return None
        else:
            campaign = Campaign(key_name=name + "_" + module.name,
                                name=name, date=date, module=module, user=get_user())
            campaign.put()
            return campaign
    else:
        return None


def delete_campaign(campaign):
    if campaign.has_permits:
        db.delete(campaign)


def edit_campaign(campaign):
    if campaign.has_permits:
        campaign.put()


def create_curve(hour, v_values, i_values, p_values, campaign):
    return Curve.get_or_insert(key_name=hour + "_" + campaign.name + "_" + campaign.module.name, hour=hour,
                               v_values=v_values, i_values=i_values, p_values=p_values, campaign=campaign)


def delete_curve(curve):
    if curve.campaign.has_permits():
        db.delete(curve)


def edit_curve(curve):
    if curve.campaign.has_permits():
        curve.put()
