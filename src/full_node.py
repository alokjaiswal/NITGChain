

import time
import calendar
import threading
import json

import sys
sys.path.append('./')


from Blockchain import Blockchain
from Block import Block
import util.consts as consts
import db.chain as db


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


def transaction():
    return json.loads(json.dumps({"data":"hello"}))


rpc.register_method('test',transaction)



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






if __name__=="__main__":
    try:

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
        
        app.run(host = "0.0.0.0",port=8000,debug=True)




    except KeyboardInterrupt:
        db.db_close()
        print("FullNode: singing offf!!!!")
        
