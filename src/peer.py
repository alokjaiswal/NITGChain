#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 12:26:25 2020

@author: alok
"""

from flask import Flask
from flask_fastrpc import FastRPCHandler
from xmlrpc import client

import socket

import json


from full_node import peers

import util.consts as consts
from utils.consts import SEED_PORT


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




content_types = ["application/json"]
seed_rpc = FastRPCHandler(app,url = '/seed')



def send_peers():
    return json.dumps(list(peers))


def send_a_peer(nodeid):
    '''
    find if nodeid exist in the local database
    otherwise return the peer list
    '''
    for node in peers:
        if(json.loads(node)["id"] == nodeid):
            return {"Status":200,"data":node}
    return {"Status":400,"data":""}


def get_peers(node):
    myserver = client.Server(node+'/seed')
    try:
        response = myserver.send_peers()
    except:
        raise("ERROR getting peers")
        
        
def get_a_peer(node,search_node):
    myserver = client.Server(node+'/seed')
    try:
        response = myserver.send_a_peer(search_node)
    except:
        raise("ERROR getting node information from "+node["id"])
    
    
seed_rpc.register_method('get_peers',get_peers)
seed_rpc.register_method('get_a_peer',get_a_peer)


if __name__=="__main__":
    try:
                
        consts.SEED_PORT = 8008
        
        app.run(host = "0.0.0.0",port=consts.SEED_PORT,debug=True)
        
    except:
        raise("ERROR:Unable to start seeding server")




















