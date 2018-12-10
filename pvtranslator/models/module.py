from main import db


class Module(db.Model):
    __tablename__ = 'module'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(32), unique=True, nullable=False)
    campaigns = db.relationship("Campaign", backref="module", lazy=True)
    user_id = db.Column(db.String(21), db.ForeignKey('user.id'))

    def __repr__(self):
        return "Module(name='%s')" % self.name
