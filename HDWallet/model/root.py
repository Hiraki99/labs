import sys
import os
from datetime import datetime
from config import db


class RootKey(db.Model):
    __tablename__ = 'RootKey'

    id = db.Column(db.Integer, primary_key=True)
    main_network = db.Column(db.String(500), nullable=False)
    wallet_id= db.Column(db.Integer, unique=True,nullable=False)
    passphrase = db.Column(db.String(500),unique=True, nullable=False)
    scheme= db.Column(db.String(100),unique=True, nullable=False)
    createAt = db.Column(db.DateTime, nullable=False, default=datetime.now, index=True)
    updateAt = db.Column(db.DateTime, nullable=False, default=datetime.now, index=True)
    
    def __init__(self, main_network,wallet_id,passphrase,scheme):
        self.main_network = main_network
        self.wallet_id = wallet_id
        self.passphrase = passphrase
        self.scheme = scheme
    def __repr__(self):
        return '<NameGroRootKeyup %r>' % self.wallet_id
