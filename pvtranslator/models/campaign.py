from google.appengine.ext import db
from pvtranslator.models.module import Module


class Campaign(db.Model):

    id = db.IntegerProperty
    name = db.StringProperty
    date = db.DateProperty()
    module_id = db.ReferenceProperty(Module, collection_name='campaigns')

    def __repr__(self):
        return "<Campaign(name='" + str(self.name) + "', date='" + str(self.date) + "')>"