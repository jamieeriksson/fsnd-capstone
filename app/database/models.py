from sqlalchemy.sql.schema import ForeignKey
from .. import db


class Player(db.Model):
    """Data model for individual players"""

    __tablename__ = "player"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    gender = db.Column(db.String(6), nullable=False)
    jersey_number = db.Column(db.Integer, nullable=False)
    position = db.Column(db.String(7), nullable=False)
    team_id = db.Column(db.Integer, ForeignKey("team.id"))

    def __repr__(self):
        return "<Player {}>".format(self.name)

    def format(self):
        if self.team:
            return {
                "id": self.id,
                "name": self.name,
                "gender": self.gender,
                "jersey_number": self.jersey_number,
                "position": self.position,
                "team": self.team.name,
            }
        else:
            return {
                "id": self.id,
                "name": self.name,
                "gender": self.gender,
                "jersey_number": self.jersey_number,
                "position": self.position,
                "team": "",
            }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


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

    def format(self):
        return {
            "id": self.id,
            "name": self.name,
            "location": self.location,
            "division": self.division,
            "level": self.level,
            "roster": [player.name for player in self.players],
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

