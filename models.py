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
    z1 = 'Определяется'
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


class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(Enum('admin', 'editor', 'tourist', name='user_roles'),
                     nullable=False,
                     default='tourist')
    atype = db.Column(Enum(ActivitiesTypes, default='t1'))
    passes = db.relationship('Passes', backref='users', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'


class Passes(db.Model):
    __tablename__ = 'passes'

    id = db.Column(db.Integer, primary_key=True)
    beautyTitle = db.Column(db.String(100))
    title = db.Column(db.String(100))
    other_titles = db.Column(db.String(200))
    connect = db.Column(ARRAY(db.Integer), nullable=True)
    add_time = db.Column(DateTime, default=datetime.now, nullable=False)
    level_winter = db.Column(Enum(LevelEnum), nullable=True)
    level_spring = db.Column(Enum(LevelEnum), nullable=True)
    level_summer = db.Column(Enum(LevelEnum), nullable=True)
    level_autumn = db.Column(Enum(LevelEnum), nullable=True)
    status = db.Column(Enum(StatusEnum),
                       nullable=False,
                       default='NEW')

    users_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    coords_id = db.Column(db.Integer, db.ForeignKey('coords.id'), nullable=False)
    images = db.relationship('Images', backref='img', lazy=True)


class Coords(db.Model):
    __tablename__ = 'coords'

    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(DECIMAL(9, 6), nullable=False)
    longitude = db.Column(DECIMAL(9, 6), nullable=False)
    height = db.Column(db.Integer)

    passes = db.relationship('Passes', backref='coords', lazy=True)


class Images(db.Model):
    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True)
    pass_id = db.Column(db.Integer, db.ForeignKey('passes.id'), nullable=False)

    @classmethod
    def create_img(cls, pass_id):
        new_img = cls(pass_id=pass_id)
        db.session.add(new_img)
        db.session.commit()
        return {
            'id': new_img.id,
            'pass_id': new_img.pass_id
        }
