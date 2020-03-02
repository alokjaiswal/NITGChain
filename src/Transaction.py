from dataclasses import dataclass
import json

@dataclass
class Transaction:
    def __init__(self,nonce,from_account,to_account,amount,v,r,s,data):
        self.nonce = nonce
        self.from_account = from_account
        self.to_account = to_account
        self.amount = amount
        self.v = v
        self.r = r
        self.s = s
        self.data = data
        
    def __str__(self):
        return self.__dict__
    
    def sign(self):
        '''
        Function to make a signing function
        INPUT: private key of sender,
        OUTPUT: string of signature
        '''
    def describe(self):
        '''
        submarize the transaction and return basic infos
        '''
        
    def verify(self):
        '''
        verify the transaction
        check types of input
        
        '''

    def Objectify(self):
        '''
        funtion to convert 
        '''




























    
        