import sys
import os
from datetime import datetime
from config import db


class Subkey(db.Model):
    __tablename__ = 'SubKey'

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(500),unique=True, nullable=False)
    key_private = db.Column(db.String(500),unique=True, nullable=False)
    key_public = db.Column(db.String(500),unique=True, nullable=False)
    wif = db.Column(db.String(500),unique=True, nullable=False)
    path = db.Column(db.String(500),unique=True, nullable=False)
    wallet_id_sqlite = db.Column(db.Integer, unique=True,nullable=False)
    parent_id = db.Column(db.Integer, nullable=False) # id pf masterkey
    key_id = db.Column(db.Integer, nullable=False,unique=True) # id pf masterkey
    balance = db.Column(db.Float,nullable=False, default=0, index=True)
    useraccount_id = db.Column(db.Integer,unique=True) # account of user with each currency
    createAt = db.Column(db.DateTime, nullable=False, default=datetime.now, index=True)
    updateAt = db.Column(db.DateTime, nullable=False, default=datetime.now, index=True)
    
    def __init__(self, address, key_private,key_public,wif,path,wallet_id_sqlite,parent_id,
                balance,useraccount_id,key_id):
        self.address = address
        self.key_private = key_private
        self.key_public = key_public
        self.wif = wif
        self.path = path
        self.wallet_id_sqlite = wallet_id_sqlite
        self.parent_id = parent_id
        self.useraccount_id = useraccount_id
        self.balance = balance
        self.key_id = key_id
    def __repr__(self):
        return '<Subkey %r>' % self.address
