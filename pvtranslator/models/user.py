from main import db


class User(db.Model):
    __tablename__ = "user"
    id = db.Column('id', db.String(30), primary_key=True)
    modules = db.relationship('Module', backref='user', lazy=True)

    def __repr__(self):
        return "User id: %s " % self.id
