from Block import Block
from hashlib import sha256
import time
import json
from dataclasses import dataclass
from db.chain import db
@dataclass
class Blockchain:
    # difficulty of our PoW algorithm
    difficulty: int = 2

    def __init__(self):
        self.unconfirmed_transactions = []
        self.chain = []

    def create_genesis_block(self):
        """
        A function to generate genesis block and appends it to
        the chain. The block has index 0, previous_hash as 0, and
        a valid hash.
        """
        #genesis_block = Block(0, [], time.time(), "0")
        genesis_block = Block(0, [], 1560022896.0091162, "0")
        #genesis_block.hash = genesis_block.compute_hash()
        genesis_block.hash = "00a64cd84b07979ff4a3e51646a8c01dcefb5f569d0055a793c5f6c9aec240cc"
        self.chain.append(genesis_block)

    @property
    def last_block(self):
        return self.chain[-1]

    def add_block(self, block, proof):
        """
        A function that adds the block to the chain after verification.
        Verification includes:
        * Checking if the proof is valid.
        * The previous_hash referred in the block and the hash of latest block
          in the chain match.
        """
        # print(self.last_block)
        previous_hash = self.last_block.hash
        if previous_hash != block.previous_hash:
            return False

        if not Blockchain.is_valid_proof(block, proof):
            return False

        block.hash = proof
        self.chain.append(block)
        print("====================================")
        print("BLOCK CREATED : ",block.index," HASH : ",proof)
        print("====================================")
        return True

    def proof_of_work(self, block):
        """
        Function that tries different values of nonce to get a hash
        that satisfies our difficulty criteria.
        """
        block.nonce = 0

        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()

        return computed_hash

    def add_new_transaction(self, transaction):
        # print('added++++++++++++')
        # print(len(self.unconfirmed_transactions))
        # print(transaction,type(transaction))
        txn_string = json.dumps(transaction, sort_keys=True)
        print("TRANSACTION HASH : ",sha256(txn_string.encode()).hexdigest())
        self.unconfirmed_transactions.append(transaction)

    @classmethod
    def is_valid_proof(cls, block, block_hash):
        """
        Check if block_hash is valid hash of block and satisfies
        the difficulty criteria.
        """
        return (block_hash.startswith('0' * Blockchain.difficulty) and
                block_hash == block.compute_hash())

    @classmethod
    def check_chain_validity(cls, chain):
        result = True
        previous_hash = "0"

        for block in chain:
            block_hash = block['hash']
            # remove the hash field to recompute the hash again
            # using `compute_hash` method.
            del block['hash']

            if not cls.is_valid_proof(block, block_hash) or \
                    previous_hash != block['previous_hash']:
                result = False
                break

            block_hash, previous_hash = block_hash, block_hash

        return result
    
    def build_chain_from_header(self,headers):
        if headers != None:
            

    def mine(self):
        """
        This function serves as an interface to add the pending
        transactions to the blockchain by adding them to the block
        and figuring out Proof Of Work.
        """
        # print("$$1$$")
        if not self.unconfirmed_transactions:
            return False
        # print("$$2$$")
        last_block = self.last_block

        new_block = Block(index=last_block.index + 1,
                          transactions=self.unconfirmed_transactions,
                          timestamp=time.time(),
                          previous_hash=last_block.hash)
        # print("$$3$$")
        proof = self.proof_of_work(new_block)
        self.add_block(new_block, proof)
        # print("$$4$$")
        self.unconfirmed_transactions = []
        # print("$$5$$")
        # announce it to the network
        return new_block.index
