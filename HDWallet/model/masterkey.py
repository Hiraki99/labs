import sys
import os
from datetime import datetime
from config import db


class MasterKey(db.Model):
    __tablename__ = 'MasterKey'

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(500),unique=True, nullable=False)
    key_private = db.Column(db.String(500),unique=True, nullable=False)
    key_public = db.Column(db.String(500),unique=True, nullable=False)
    wif = db.Column(db.String(500),unique=True, nullable=False)
    path = db.Column(db.String(500),unique=True, nullable=False)
    wallet_id_sqlite = db.Column(db.Integer, unique=True,nullable=False)
    balance = db.Column(db.Float,nullable=False, default=0)
    account_id= db.Column(db.Integer, unique=True, nullable=False)
    root_id = db.Column(db.Integer,nullable=False)
    currency = db.Column(db.String(500),unique=True, nullable=False)
    createAt = db.Column(db.DateTime, nullable=False, default=datetime.now, index=True)
    updateAt = db.Column(db.DateTime, nullable=False, default=datetime.now, index=True)

    def __init__(self, address, key_private,key_public,wif,path,wallet_id_sqlite,balance,root_id,account_id):
        self.address = address
        self.key_private = key_private
        self.key_public = key_public
        self.wif = wif
        self.path = path
        self.wallet_id_sqlite = wallet_id_sqlite
        self.balance = balance
        self.root_id = root_id
        self.account_id = account_id

    def __repr__(self):
        return '<NameGroup %r>' % self.address
