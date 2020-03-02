from hashlib import sha256
import json
from dataclasses import dataclass


@dataclass
class Block_Header:
    def __init__(self,index,transactions,timestamp,previous_hash,nonce):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce
        
    def compute_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()

@dataclass
class Block:
    def __init__(self, index, transactions, timestamp, previous_hash, nonce=0):
        self.header = Block_Header(index,transactions,timestamp,previous_hash,nonce)
        self.header_hash = self.header.compute_hash()
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.next_turn = []
    
    

    def compute_hash(self):
        """
        A function that takes all the parameters of the block as input and return the hash of the block contents.
        """
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()
    
    
    def sign():
        '''
        make a signing function for the authorities
        '''
        
    def verify():
        '''
        make a verifing function for the signed block
        '''
    def insert_next_turn(self,my_list):
        self.next_turn = my_list
        
        
        
        
    
