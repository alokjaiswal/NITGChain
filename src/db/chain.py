import plyvel
import json
db = 0;
NEW_BLOCKCHAIN = False

try:
    db = plyvel.DB('./db')
except IOError:
    print("Database already running")
except:
    NEW_BLOCKCHAIN = True
    print("ERROR accessing database ")
finally:
    pass

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
        
        