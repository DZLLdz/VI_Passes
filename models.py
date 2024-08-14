import enum

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum, DECIMAL, DateTime
from sqlalchemy.dialects.postgresql import ARRAY
from datetime import datetime

db = SQLAlchemy()


class StatusEnum(enum.Enum):
    NEW = 'New'
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'


class LevelEnum(enum.Enum):
    oneA = '1A'
    oneB = '1B'
    twoA = '2A'
    twoB = '2B'
    threeA = '3A'
    threeB = '3B'


class ActivitiesTypes(enum.Enum):
    t1 = 'пешком'
    t2 = 'лыжи'
    t3 = 'катамаран'
    t4 = 'байдарка'
    t5 = 'плот'
    t6 = 'сплав'
    t7 = 'велосипед'
    t8 = 'автомобиль'
    t9 = 'мотоцикл'
    t10 = 'парус'
    t11 = 'верхом'


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(Enum('admin', 'editor', 'tourist', name='user_roles'),
                     nullable=False,
                     default='tourist')
    atype = db.Column(Enum(ActivitiesTypes))
    passes = db.relationship('Passes', backref='author', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'


class Passes(db.Model):
    __tablename__ = 'passes'

    id = db.Column(db.Integer, primary_key=True)
    beautyTitle = db.Column(db.String(100))
    title = db.Column(db.String(100))
    other_titles = db.Column(db.String(200))
    connect = db.Column(ARRAY(db.Integer), nullable=True)
    add_time = db.Column(DateTime, default=datetime.utcnow, nullable=False)
    level_winter = db.Column(Enum(LevelEnum))
    level_spring = db.Column(Enum(LevelEnum))
    level_summer = db.Column(Enum(LevelEnum))
    level_autumn = db.Column(Enum(LevelEnum))
    status = db.Column(Enum(StatusEnum),
                       nullable=False,
                       default='new')

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    coords_id = db.Column(db.Integer, db.ForeignKey('coords.id'), nullable=False)
    images = db.relationship('images', backref='img', lazy=True)


class Coords(db.Model):
    __tablename__ = 'coords'

    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(DECIMAL(9, 6), nullable=False)
    longitude = db.Column(DECIMAL(9, 6), nullable=False)
    height = db.Column(db.Integer)

    passes = db.relationship('Passes', backref='locations', lazy=True)

class Images(db.Model):
    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True)
    pass_id = db.Column(db.Integer, db.ForeignKey('passes.id'), nullable=False)
