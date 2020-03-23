

import time
import calendar
import threading
import json

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(1,currentdir) 



from Blockchain import Blockchain
from Block import Block
import util.consts as consts
import db.chain as db

from Transaction import Transaction



from flask import Flask, request
import requests
from flask_fastrpc import FastRPCHandler
from xmlrpc import client

import socket


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255',1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

app = Flask(__name__)



#blockchain object
blockchain = Blockchain()


content_types = ["application/json"]
#RPC handler for rpc calls between the blockchain_nodes
#rpc = FastRPCHandler(app,allowed_content_types = content_types,url = '/API')
rpc = FastRPCHandler(app,url = '/API')


peers = set()



def sync_nodes():
    """
    Our simple consnsus algorithm. If a longer valid chain is
    found, our chain is replaced with it.
    """
    global blockchain

    longest_chain = None
    current_len = len(blockchain.chain)
    for node in peers:

        try:
            myserver = client.Server(node+'/API')
            response = myserver.get_chain()
            response = json.loads(response)
            print(type(response))
            print(response)
            length = response['length']
            chain = response['chain']
            if length > current_len and blockchain.check_chain_validity(chain):
                current_len = length
                longest_chain = chain
        except Exception:
            print(Exception)

    if longest_chain:
        blockchain = Blockchain()
        blockchain = blockchain.create_chain_from_dump(longest_chain)
        return True

    return False




def send_transaction(sender_public_key,sender_address,data,amount,reciever_address,signature):
    '''
    calculate of senders transactions in blockchain 
    sender signes using his wallet and sends the signature private key is not required to be sent to the blockchain node
    '''
    
    if (type(sender_public_key) != str):
        return {"ERROR":"TYPE_ERROR:Type of sender_public_key is not string"}
    
    if (type(sender_address) != str):
        return {"ERROR":"TYPE_ERROR:Type of sender_sender is not string"}
    
    if(type(data) != dict):
        return {"ERROR":"TYPE_ERROR: Invalid data format"}
    
    if(type(amount) != float):
        return {"ERROR":"Invalid type of amount"}
    
    if (type(reciever_address) != str):
        return {"ERROR":"TYPE_ERROR:Type of reciever_address is not string"}
    
    if (type(signature) != str):
        return {"ERROR":"TYPE_ERROR:Type of signature is not string"}
    
    
    txn = Transaction(0,sender_address,reciever_address,amount,sender_public_key,data,time.time())
    
    blockchain.unconfirmed_transactions.append(txn)
    
    
    send_txn_to_peers(txn)
        
    
    return txn.toStr()
    



def get_transaction(txn):
    
    if(type(txn) != str):
        return {"ERROR":"TYPE_ERROR: Type of data recieved is not string"}
    
    txn = Transaction.Objectify(txn)
    
    if(type(txn.nonce) != int):
        return {"ERROR":"Invalid type of nonce in transaction"}
    
    if (type(txn.vk) != str):
        return {"ERROR":"TYPE_ERROR:Type of sender_public_key is not string"}
    
    if (type(txn.from_account) != str):
        return {"ERROR":"TYPE_ERROR:Type of sender_address is not string"}
    
    if(type(txn.data) != dict):
        return {"ERROR":"TYPE_ERROR: Invalid data format"}
    
    if(type(txn.amount) != float):
        return {"ERROR":"Invalid type of amount"}
    
    if (type(txn.to_account) != str):
        return {"ERROR":"TYPE_ERROR:Type of reciever_address is not string"}
    
    if (type(txn.sig) != str):
        return {"ERROR":"TYPE_ERROR:Type of signature is not string"}
    
    blockchain.unconfirmed_transactions.append(txn)
    
    send_txn_to_peers(txn)
    
    return {"Status":"OK"}


def send_txn_to_peers(txn):
    for node in peers:
        myserver = client.Server(node+'/API')
        try:
            response = myserver.get_transaction(json.dumps(txn))
        except:
            peers.remove(node)


        
rpc.register_method("get_transaction",get_transaction)

if __name__=="__main__":
    global NODE_PORT
    try:
        if (db.NODE_KEY_STORE):
            sk,vk = db.store_key_pair()
            print(msg)
            print(keys)
            

        if (db.NEW_BLOCKCHAIN):
            print("Local Database Unavailable")
            db.create_database()
            print("Starting new node from genesis")
            
        else:
            print("FOUND Local database restoring data")
            block_headers = db.db_get_chain_metadata()
            blockchain.build_chain_from_header(block_headers)
            '''
            create an method in Blockchain class to create chain from block headers
            '''
            
        sync_nodes()
        
        NODE_PORT = 8000
        
        app.run(host = "0.0.0.0",port=NODE_PORT,debug=True)




    except KeyboardInterrupt:
        db.db.close()
        db.node_db.close()
        print("FullNode: singing offf!!!!")
        
