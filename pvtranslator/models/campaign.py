import logging
from google.appengine.ext import db
from pvtranslator.models.auth import get_user
from pvtranslator.models.module import Module
from pvtranslator.models.user import User
from pvtranslator.models import auth


class Campaign(db.Model):

    name = db.StringProperty()
    date = db.DateProperty()
    module = db.ReferenceProperty(Module, collection_name='campaigns')
    user = db.ReferenceProperty(User)

    def has_permits(self):
        user = auth.get_user()
        if user is not None and self.user.id == user.id or self.module.user_id.id == user.id:
            return True
        return False

    @staticmethod
    def create_campaign(nombre, fecha, modulo):
        return Campaign.get_or_insert(key_name=nombre+"_"+modulo.name,
                                      name=nombre, date=fecha, module=modulo, user=get_user())

    @staticmethod
    def delete_campaign(campaign):
        db.delete(campaign)

    @staticmethod
    def edit_campaign(campaign):
        campaign.put()

    def __repr__(self):
        return "<Campaign(name='" + str(self.name) + "', date='" + str(self.date) + "')>"
