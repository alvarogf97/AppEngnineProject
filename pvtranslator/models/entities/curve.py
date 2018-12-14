from google.appengine.ext import db
from pvtranslator.models.utils.auth import get_user
from pvtranslator.models.entities.campaign import Campaign
from pvtranslator.models.entities.user import User
from pvtranslator.models.utils import auth


class Curve(db.Model):

    hour = db.StringProperty
    v_values = db.ListProperty(float)
    i_values = db.ListProperty(float)
    p_values = db.ListProperty(float)
    campaign = db.ReferenceProperty(Campaign, collection_name='curves')
    user = db.ReferenceProperty(User)

    def has_permits(self):
        user = auth.get_user()
        if user is not None and self.campaign.user.id == user.id or self.campaign.module.user_id.id == user.id:
            return True
        return False

    @staticmethod
    def create_curve(hora, listav, listai, listap, campana):
        if Curve.has_permits():
            return Curve.get_or_insert(key_name=hora+"_"+campana.name+"_"+campana.module.name, hour=hora,
                                       v_values=listav, i_values=listai, p_values=listap, campaign=campana)
        else:
            return None

    @staticmethod
    def delete_curve(curva):
        db.delete(curva)

    @staticmethod
    def edit_curve(curva):
        curva.put()

    def __repr__(self):
        return "<Curve(hour='" + str(self.hour) + "', campaign='" + str(self.campaign) + "', module='" + \
               str(self.campaign.module) +"')>"

