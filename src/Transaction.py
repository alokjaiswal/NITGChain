#chnage kiya h

from dataclasses import dataclass
import json
from hashlib import sha256
import sys

sys.path.insert(1, '/home/sheetal/Desktop/8th/(5-3-2020)zip/util')
import util.digital_signature as dg

@dataclass
class Transaction:
    def __init__(self,nonce,from_account,to_account,amount,vk,data,timestamp):
        self.nonce = nonce
        self.from_account = from_account
        self.to_account = to_account
        self.amount = amount
        self.vk = vk
        #self.sk = sk
        self.data = data
        self.timestamp=timestamp
        
    def __str__(self):
        return self.__dict__
    
    def toStr(self):
        return json.dumps(self.__dict__, default=lambda o: o.__dict__)
    
    def compute_hash(self):
        txn_string = json.dumps(self.__dict__, sort_keys=True)
        #txn_string = jsonpickle.encode(self, unpicklable=False)
        return sha256(txn_string.encode()).hexdigest()
    
    def sign(self):
        txn_hash = self.compute_hash()
        sk = 5 # extract sk from node_db at the start of node
        txn_sign = dg.signature(sk,txn_hash)
        return txn_sign
       # sig = 
        '''
        Function to make a signing function
        INPUT: private key of sender,
        OUTPUT: string of signature
        '''
    def describe(self):
        '''
        submarize the transaction and return basic infos
        '''
        
    def verify(self,txn_sign,txn_hash,vk):
      sign_verified = dg.verification(txn_sign,txn_hash,vk)
      if sign_verified:
          return True
      else:
            return False
    
    @classmethod
    def Objectify(cls,txn_str):
        
        '''
        funtion to convert 
        use this as:=> p = Transaction.Objectify(r)
        '''
        txn_str = json.loads(txn_str)
        return Transaction(txn_str['nonce'],txn_str['from_account'],txn_str['to_account'],txn_str['amount'],txn_str['vk'],txn_str['data'],txn_str['timestamp'])
       



























    
        
