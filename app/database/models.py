from sqlalchemy.sql.schema import ForeignKey
from .. import db


class Player(db.Model):
    """Data model for individual players"""

    __tablename__ = "player"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    gender = db.Column(db.String(6), nullable=True)
    jersey_number = db.Column(db.Integer, nullable=False)
    position = db.Column(db.String(7), nullable=True)
    team_id = db.Column(db.Integer, ForeignKey("team.id"))

    def __repr__(self):
        return "<Player {}>".format(self.name)


class Team(db.Model):
    """Data model for registered teams"""

    __tablename__ = "team"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    location = db.Column(db.String(64), nullable=False)
    division = db.Column(db.String(7), nullable=False)
    level = db.Column(db.String(20), nullable=False)
    players = db.relationship("Player", backref="team")

    def __repr__(self):
        return "<Team {}>".format(self.name)

