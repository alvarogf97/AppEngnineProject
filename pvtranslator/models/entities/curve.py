from google.appengine.ext import db
from pvtranslator.models.entities.campaign import Campaign
from pvtranslator.models.utils import auth


class Curve(db.Model):
    hour = db.StringProperty()
    v_values = db.ListProperty(float)
    i_values = db.ListProperty(float)
    p_values = db.ListProperty(float)
    campaign = db.ReferenceProperty(Campaign, collection_name='curves')

    def has_permits(self):
        user = auth.get_user()
        if user is not None and self.campaign.user.id == user.id or self.campaign.module.user_id.id == user.id:
            return True
        return False

    @staticmethod
    def create_curve(hour, v_values, i_values, p_values, campaign):
        return Curve.get_or_insert(key_name=hour + "_" + campaign.name + "_" + campaign.module.name, hour=hour,
                                   v_values=v_values, i_values=i_values, p_values=p_values, campaign=campaign)

    @staticmethod
    def delete_curve(curve):
        db.delete(curve)

    @staticmethod
    def edit_curve(curve):
        curve.put()

    def __repr__(self):
        return "<Curve(hour='" + str(self.hour) + "', campaign='" + str(self.campaign) + "', module='" + \
               str(self.campaign.module) + "')>"
