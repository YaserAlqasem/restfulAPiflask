from marshmallow import Schema, fields, pre_load, validate
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
import datetime,bcrypt
ma = Marshmallow()
db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(150), unique=True, nullable=False)
    Email = db.Column(db.String(150), nullable=False)
    Password = db.Column(db.String(255), nullable=False)
    Registered_on = db.Column(db.DateTime, nullable=False)
    def __init__(self, Username, Email,Password):
        self.Username = Username
        self.Email = Email
        self.Password = bcrypt.hashpw(Password.encode('utf8'), bcrypt.gensalt(12)).decode('utf-8')
        self.Registered_on = datetime.datetime.now()
        
class UserSchema(ma.Schema):
    id = fields.Integer()
    Username = fields.String(required=True)
    Email = fields.String(required=False)
    Password = fields.String(required=True)
    Registered_on = fields.DateTime()