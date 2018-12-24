from google.appengine.ext import db
from pvtranslator.models.entities.module import Module
from pvtranslator.models.entities.user import User


class Comment(db.Model):
    text = db.StringProperty()
    module = db.ReferenceProperty(Module, collection_name='comments')
    user = db.ReferenceProperty(User)

    def has_permits(self, user):
        if user is not None:
            if self.user.id == user.id or self.module.user.id == user.id:
                return True
        return False

    def __repr__(self):
        return "<Comment(text='" + self.text + "')>"
