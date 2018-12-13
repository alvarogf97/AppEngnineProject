from google.appengine.ext import db
from pvtranslator.models.user import User
from pvtranslator.models.auth import get_user


class Module(db.Model):
    name = db.StringProperty
    user = db.ReferenceProperty(User, collection_name='modules')

    def has_permits(self):
        user = get_user()
        if user is not None and self.user.id == user.id:
            return True
        else:
            return False

    @staticmethod
    def create_module(nombre):
        return Module.get_or_insert(key_name=nombre, name=nombre, user=get_user())

    @staticmethod
    def delete_module(module):
        db.delete(module)

    @staticmethod
    def edit_module(module):
        module.put()

    def __repr__(self):
        return "Module(name='%s')" % self.name
