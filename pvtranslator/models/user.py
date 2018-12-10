from google.appengine.ext import db


class User(db.Model):
    id = db.StringProperty()

    def __repr__(self):
        return "User id: %s " % self.id
