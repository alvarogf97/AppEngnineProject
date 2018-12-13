from google.appengine.ext import db
from pvtranslator.models.entities.user import User


class Module(db.Model):
    id = db.IntegerProperty
    name = db.StringProperty
    user_id = db.ReferenceProperty(User, collection_name='modules')

    def __repr__(self):
        return "Module(name='%s')" % self.name

