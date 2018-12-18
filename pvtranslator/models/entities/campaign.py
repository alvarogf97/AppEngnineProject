from google.appengine.ext import db
from pvtranslator.models.utils.auth import get_user
from pvtranslator.models.entities.module import Module
from pvtranslator.models.entities.user import User
from pvtranslator.models.utils import auth


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
    def create_campaign(name, date, module):
        user = auth.get_user()
        if user:
            return Campaign.get_or_insert(key_name=name + "_" + module.name,
                                          name=name, date=date, module=module, user=get_user())
        else:
            return None

    @staticmethod
    def delete_campaign(campaign):
        if campaign.has_permits:
            db.delete(campaign)

    @staticmethod
    def edit_campaign(campaign):
        if campaign.has_permits:
            campaign.put()

    def __repr__(self):
        return "<Campaign(name='" + str(self.name) + "', date='" + str(self.date) + "')>"
