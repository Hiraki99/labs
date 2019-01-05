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
from initdb import db_session
import json

import config

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
testnet= 'testnet'
db = config.db
db.init_app(app)

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
def init():

    with db_session() as session:
        root = session.query(RootKey).order_by(RootKey.id.desc()).first()
        if(root is None):
            passphrase = Mnemonic().generate()
            name = uuid.uuid4().hex
            new_wallet = HDWallet.create(name, key=passphrase, network='testnet')
            new_wallet = new_wallet.dict()
            rootkey= RootKey(new_wallet["main_network"],new_wallet["wallet_id"],passphrase, new_wallet["scheme"])
            session.add(rootkey)
            print(obj_to_dict(rootkey))
    
def init_master_key(currency):
    with db_session() as session:
        root = session.query(RootKey).order_by(RootKey.id.desc()).first()
        print(obj_to_dict(root))
    
        root_key = HDWallet(root.wallet_id)
        name = uuid.uuid4().hex

        master_key = session.query(MasterKey).filter(MasterKey.currency == currency).first()
        if(master_key is None):

            account_btc_master = root_key.new_account(name)
            master_key = account_btc_master.dict()
            masterkey = MasterKey(master_key["address"],master_key["key_private"],
                            master_key["key_public"],master_key["wif"],master_key["path"],
                            master_key["id"],master_key["balance"],
                            root_key_id,master_key["account_id"],currency)
            
            session.add(masterkey)

@app.route('/create_new_wallet', methods=['POST'])
def create_new_wallet():
    """ create new wallet """
    try:
        passphrase = Mnemonic().generate()
        name = uuid.uuid4().hex
        new_wallet = HDWallet.create(name, key=passphrase, network='testnet')
        new_wallet = new_wallet.dict()
        rootkey= RootKey(new_wallet["main_network"],new_wallet["wallet_id"],passphrase, new_wallet["scheme"])
        
        resoponse = {}
        resoponse["wallet"]= obj_to_dict(rootkey)
        print(obj_to_dict(rootkey))
        db.session.add(rootkey)
        db.session.commit()

        return jsonify(resoponse)
    except:
        traceback.print_exc()
        return jsonify({'status': 0, 'message': 'Create new wallet error'})

@app.route('/create_account_wallet_btc', methods=['POST'])
def create_children_wallet():
    """ create account wallet btc same wallet big of btc """
    try:
        root_key_id = request.json.get('root_key_id')
        currency = request.json.get('currency')

        root_key = HDWallet(root_key_id)
        name = uuid.uuid4().hex
        account_btc_master = root_key.new_account(name)
        master_key = account_btc_master.dict()
        masterkey = MasterKey(master_key["address"],master_key["key_private"],
                        master_key["key_public"],master_key["wif"],master_key["path"],
                        master_key["id"],master_key["balance"],
                        root_key_id,master_key["account_id"],currency)
        
        db.session.add(masterkey)
        response = {}

        response["masterkey"] = obj_to_dict(masterkey)
        db.session.commit()
        return jsonify(response)
    except:
        traceback.print_exc()
        return jsonify({'status': 0, 'message': 'Create new wallet children error'})

@app.route('/create_new_subkey', methods=['POST'])
def create_new_subkey():
    """ create new wallet """
    try:
        root_key_id = request.json.get('root_key_id')
        master_key_id = request.json.get('master_key_id')
        useraccount_id = request.json.get('useraccount_id')
        wallet_parent = HDWallet(root_key_id)
        hd_subkey_a = wallet_parent.new_key(account_id = master_key_id)
        print(hd_subkey_a.dict()["address"])
        hd_subkey = hd_subkey_a.dict()
        print(hd_subkey)
        subkey = Subkey(hd_subkey["address"], hd_subkey["key_private"],hd_subkey["key_public"],hd_subkey["wif"],
                        hd_subkey["path"], hd_subkey["id"], master_key_id,
                        hd_subkey["balance"],useraccount_id,hd_subkey["id"])
        db.session.add(subkey)
        response = {}

        response["subkey_info"] = obj_to_dict(subkey)

        db.session.commit()

    
        return jsonify(response)
    except:
        traceback.print_exc()
        return jsonify({'status': 0, 'message': 'Create new wallet error'})

@app.route('/send_transaction', methods=['POST'])
def send_transaction():
    """ create new wallet """
    try:
        master_key_id = request.json.get('master_key_id')
        wallet_parrent_id = request.json.get('wallet_parrent_id')
        amount = request.json.get('amount')
        to_address = request.json.get('to')
               
        wallet_parent = HDWallet(wallet_parrent_id)
        

        transaction = wallet_parent.send_to(to_address, amount * 100000000,account_id = master_key_id)

        response = {}

        response["transaction"]= transaction.dict()
        return jsonify(response)
    except:
        traceback.print_exc()
        return jsonify({'status': 0, 'message': 'Create Transaction error'})

@app.route('/getBalance', methods=['POST'])
def getBalance():
    """ get Balance  """
    try:
        root_key_id = request.json.get('root_key_id')
        master_key_id = request.json.get('master_key_id')
        
        wallet_parent = HDWallet(root_key_id)
        wallet_parent._balance_update(account_id = master_key_id)
        wallet_parent.utxos_update(account_id = master_key_id)
        wallet_parent.utxos( account_id = master_key_id)

        test = wallet_parent.account(account_id = master_key_id)
        wallet_parent.info()
        response = {}


        # response["balance"]= wallet_parent.balance(account_id=account_id)
        response["balance"]= test.dict()
        return jsonify(response)
    except:
        traceback.print_exc()
        return jsonify({'status': 0, 'message': 'Create Transaction error'})

@app.route('/getBalanceSubkey', methods=['POST'])
def getBalanceSubkey():
    """ get Balance Subkey"""
    try:
        root_key_id = request.json.get('root_key_id')
        subkey_id = request.json.get('subkey_id')

        wallet_parent = HDWallet(root_key_id)
        wallet_parent.utxos_update()
        wallet_parent.utxos()
       
        all_network = wallet_parent.networks()
        


        hd_key_child = wallet_parent.keys(depth = 5, network=all_network[0]['network_name'],key_id=subkey_id, is_active=True)
        hd_key_child_item = hd_key_child[0]
        
        response = {}
        response["address"] = hd_key_child_item.address
        response["balance"]= Network(hd_key_child_item.network_name).print_value(hd_key_child_item.balance)
        return jsonify(response)
    except:
        traceback.print_exc()
        return jsonify({'status': 0, 'message': 'Create Transaction error'})

@app.route("/updateTransaction",methods= ['POST'])
def updateTransaction():
    try:
        root_key_id = request.json.get('root_key_id')
        subkey_id = request.json.get('subkey_id')

        wallet_parent = HDWallet(root_key_id)

        wallet_parent.transactions_update(key_id = subkey_id)
        all_transaction = wallet_parent.transactions(key_id = subkey_id)
        print(all_transaction)
       
        return jsonify(all_transaction)

    except:
        traceback.print_exc()
        return jsonify([])
        pass

def main():
    with db_session() as session:
       init()
       init_master_key('BTC')
       init_master_key('ETH')
       init_master_key('USDT')
    app.run(host='0.0.0.0', port=8011, debug=True)

if __name__ == "__main__":
    main()
