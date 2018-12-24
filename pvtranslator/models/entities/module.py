from google.appengine.ext import db
from pvtranslator.models.entities.user import User


class Module(db.Model):
    name = db.StringProperty()
    user = db.ReferenceProperty(User, collection_name='modules')

    def has_permits(self, user):
        if user is not None and self.user.id == user.id:
            return True
        else:
            return False

    def __repr__(self):
        return "Module(name='%s')" % self.name
