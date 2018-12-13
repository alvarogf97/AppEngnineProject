from google.appengine.ext import db


class User(db.Model):
    id = db.StringProperty()
    email = db.EmailProperty()
    name = db.StringProperty()

    @staticmethod
    def create_user(_id, email, name):
        user = User.get_or_insert(key_name=_id, id=_id, email=email, name=name)
        return user

    def __repr__(self):
        return "<User(id='" + str(self.id) + "', email='" + str(self.email) + "')>"
