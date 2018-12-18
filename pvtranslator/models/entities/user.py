from google.appengine.ext import db


class User(db.Model):
    id = db.StringProperty()
    email = db.EmailProperty()
    name = db.StringProperty()

    def __repr__(self):
        return "<User(id='" + str(self.id) + "', email='" + str(self.email) + "')>"
