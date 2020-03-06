import plyvel
import json

import os,sys,inspect
'''
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)+"/util"
sys.path.insert(0,parentdir) 
sys.path.insert(1,currentdir)
yy = os.path.abspath(os.getcwd())
'''
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)+"/util"
sys.path.insert(0,parentdir)

import digital_signature as digi_sign
db = 0;
NEW_BLOCKCHAIN = False
NODE_KEY_STORE = False

try:
    db = plyvel.DB('./db')
except IOError:
    print("Database already running")
except:
    NEW_BLOCKCHAIN = True
    print("ERROR accessing database ")
finally:
    pass

try:
    node_db = plyvel.DB('./')
except IOError:
    print("Node database already running")
except:
    NODE_KEY_STORE = True
    print("ERROR accessing database ")
finally:
    pass


########################################################################################################
def create_database():
    global db
    if(NEW_BLOCKCHAIN):
        db = plyvel.DB('./db', create_if_missing=True)
    


def db_get_chain_metadata():
    with open("./db/header.json","r") as file:
        if file:
            return json.load(file)
        return None


def db_write_block_header(header):
    print(header)
    with open("./db/header.json","r") as file:
        data = json.load(file)
        temp = data['metadata']
        temp[str(header.index)]=str(json.dumps(header,default=lambda o: o.__dict__))
        print(data)
    with open("./db/header.json","w") as file:
        json.dump(data, file, indent=4)


def db_get_block_from_headers(header_hash):
    try:
        return db.get(header_hash.encode('utf-8')).decode('utf-8')
    except:
        print("ERROR: Unable to retrieve block from database")


def db_write_block_with_header(header_hash,block):
    try:
        db.put(header_hash.encode('utf-8'),json.dumps(block,default=lambda o: o.__dict__).encode('utf-8'))
    except:
        print("ERROR: Unable to write into block with"+header_hash)
        raise
        
def db_close():
    db.close() 

#################################################################################################

def create_node_database():
    global node_db
    if(NODE_KEY_STORE):
        node_db = plyvel.DB('./', create_if_missing=True)
    

def store_key_pair():
    sk,vk = digi_sign.generate_key_pair()
    data = {"private_k":digi_sign.get_string_of_sk(sk),"public_k":digi_sign.get_string_of_pk(vk)}
    node_db.put(b'key_pair',json.dumps(data).encode('utf-8'))
    return sk,vk

def get_key_pair():
    key_pair = json.loads((node_db.get(b"key_pair")).decode('utf-8'))
    priv_k = digi_sign.get_sk_from_string(key_pair['private_k'])
    pub_k = digi_sign.get_pk_from_string(key_pair['public_k'])
    return priv_k,pub_k

def get_nodeID():
    '''
    return hash of public key of a node
    '''

























        
        
        