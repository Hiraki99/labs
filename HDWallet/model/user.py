import sys
import os
from datetime import datetime
from config import db
from passlib.apps import custom_app_context as pwd_context
import hashlib


class User(db.Model):
    __tablename__ = 'User'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(500), unique=True, nullable=False)
    password = db.Column(db.String(500), nullable=False)

    passwordresettoken = db.Column(db.String(500))
    passwordresetexpires = db.Column(db.DateTime)
    confirmed = db.Column(db.Boolean, default=False)
    confirmed_on = db.Column(db.DateTime)
    email = db.Column(db.String(500), unique=True, nullable=False)
    phone = db.Column(db.String(500), unique=True, nullable=False)
    facebook = db.Column(db.String(500))
    google = db.Column(db.String(500))
    linkin = db.Column(db.String(500))
    createAt = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    updateAt = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    role = db.Column(db.String(125), nullable=False)


    def __init__(self, username, passwordresettoken, passwordresetexpires, password, email, phone, facebook, google, linkin, group_id):
        """This function is using so many parameter. Function should only have no more than 7 parameter only
        
        Arguments:
            username {[type]} -- [description]
            passwordresettoken {[type]} -- [description]
            passwordresetexpires {[type]} -- [description]
            password {[type]} -- [description]
            email {[type]} -- [description]
            phone {[type]} -- [description]
            facebook {[type]} -- [description]
            google {[type]} -- [description]
            linkin {[type]} -- [description]
            group_id {[type]} -- [description]
        """

        self.username = username
        self.passwordresettoken = passwordresettoken
        self.passwordresetexpires = passwordresetexpires
        self.password = password
        self.email = email
        self.phone = phone
        self.facebook = facebook
        self.google = google
        self.linkin = linkin
        self.createdate = datetime.now()
        self.updatedate = datetime.now()
        self.group_id = group_id

    def __repr__(self):
        return '<User %r>' % self.username
    
    @staticmethod
    def hash_password(password):
        return pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password)


