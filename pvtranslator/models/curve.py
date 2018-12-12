from google.appengine.ext import db
from pvtranslator.models.campaign import Campaign


class Curve(db.Model):

    id = db.IntegerProperty
    hour = db.StringProperty
    v_values = db.ListProperty(float)
    i_values = db.ListProperty(float)
    p_values = db.ListProperty(float)
    campaign = db.ReferenceProperty(Campaign, collection_name='curves')

    def __repr__(self):
        return "Curve(hour='%s')" % self.hour

