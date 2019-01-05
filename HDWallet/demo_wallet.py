from bitcoinlib.wallets import HDWallet
from bitcoinlib.mnemonic import Mnemonic
from flask import Flask, request, redirect, jsonify, send_from_directory, render_template, session
from flask import flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from datetime import timedelta
import sys,traceback
from itsdangerous import URLSafeTimedSerializer
from bitcoinlib.wallets import HDWallet
from bitcoinlib.mnemonic import Mnemonic
import uuid, random
from bitcoinlib.networks import Network, DEFAULT_NETWORK
from model.root import RootKey
from model.masterkey import MasterKey
from model.subkey import Subkey

def obj_to_dict(item, force=False):
    """[Convert from class to Dict(). The idea is the same as bean in java]

    Arguments:
        item {[class]} -- [any type of class have __dict__ readable]

    Returns:
        [dict] -- [contain all method self.* of class]
    """
    obj = dict()
    for key in item.__dict__.keys():
        try:
            if isinstance(item.__getattribute__(key), str) or isinstance(item.__getattribute__(key), int) or isinstance(item.__getattribute__(key), float) or isinstance(item.__getattribute__(key), dict) or isinstance(item.__getattribute__(key), list):
                obj[key] = item.__getattribute__(key)
            elif item.__getattribute__(key) is None:
                obj[key] = None
            elif force:
                obj[key] = str(item.__getattribute__(key))
        except:
            continue
    return obj

from bitcoinlib.transactions import Transaction, serialize_multisig_redeemscript, Output, Input, SIGHASH_ALL
import uuid, random

# passphrase = Mnemonic().generate()
# print(passphrase)
# name = uuid.uuid4().hex
# new_wallet = HDWallet.create(name, key=passphrase, network='testnet')
import json

import config
db = config.db
from initdb import db_session

with db_session() as session:
    root = session.query(RootKey).order_by(RootKey.id.desc()).first()
    print(obj_to_dict(root))