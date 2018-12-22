from google.appengine.ext import db
from pvtranslator.models.entities.module import Module
from pvtranslator.models.entities.user import User


class Campaign(db.Model):
    name = db.StringProperty()
    date = db.DateProperty()
    module = db.ReferenceProperty(Module, collection_name='campaigns')
    user = db.ReferenceProperty(User)

    def has_permits(self):
        from pvtranslator.models.utils.auth import get_user
        user = get_user()
        if user is not None and (self.user.id == user.id or self.module.user.id == user.id):
            return True
        return False

    def __repr__(self):
        return "<Campaign(name='" + str(self.name) + "', date='" + str(self.date) + "')>"
