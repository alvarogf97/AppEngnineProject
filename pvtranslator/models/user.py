from google.appengine.ext import db


class User(db.Model):
    id = db.StringProperty()
    email = db.EmailProperty()
    name = db.StringProperty()

    def __repr__(self):
        return "User: %s " % self.email

    @staticmethod
    def search_by_id(user_id):
        users = User.all()
        users.filter("id =",user_id)
        result_list = []
        for user in users.run(limit=1):
            result_list.append(user)
        return result_list
