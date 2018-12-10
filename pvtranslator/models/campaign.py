from main import db


class Campaign(db.Model):
    __tablename__ = 'campaign'
    __namespace__ = 'pvtranslator'

    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(32), unique=True, nullable=False)
    date = db.Column('date', db.Date, nullable=False)
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'))

    def __repr__(self):
        return "<Campaign(name='" + str(self.name) + "', date='" + str(self.date) + "')>"
