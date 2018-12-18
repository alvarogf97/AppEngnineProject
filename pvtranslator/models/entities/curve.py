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

    def __repr__(self):
        return "<Curve(hour='" + str(self.hour) + "', campaign='" + str(self.campaign) + "', module='" + \
               str(self.campaign.module) + "')>"
