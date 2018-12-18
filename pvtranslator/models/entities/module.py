from google.appengine.ext import db
from pvtranslator.models.entities.user import User
from pvtranslator.models.utils.auth import get_user


class Module(db.Model):
    name = db.StringProperty()
    user = db.ReferenceProperty(User, collection_name='modules')

    def has_permits(self):
        user = get_user()
        if user is not None and self.user.id == user.id:
            return True
        else:
            return False

    @staticmethod
    def create_module(name):
        user = get_user()
        if user:
            return Module.get_or_insert(key_name=name, name=name, user=user)
        else:
            return None

    @staticmethod
    def delete_module(module):
        if module.has_permits:
            db.delete(module)

    @staticmethod
    def edit_module(module):
        if module.has_permits:
            module.put()

    def __repr__(self):
        return "Module(name='%s')" % self.name
