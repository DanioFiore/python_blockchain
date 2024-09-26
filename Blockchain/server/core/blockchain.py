# our main file
import sys
# all our modules now are in python_blockchain folder
sys.path.append('/home/danio/personal/wa/python_blockchain')

from Blockchain.server.core.block import Block
from Blockchain.server.core.block_header import BlockHeader
from Blockchain.server.tools.tools import hash256
from Blockchain.server.core.database.database import BlockchainDB
from Blockchain.server.core.transaction import CoinbaseTransaction

import time

# manual hash of the genesis block
ZERO_HASH = '0' * 64
# our blockchain version
VERSION = 1
class Blockchain:
    def __init__(self):
        pass

    def writeOnDisk(self, block):
        blockchain_db = BlockchainDB()
        blockchain_db.write(block)

    def fetchLastBlock(self):
        blockchain_db = BlockchainDB()
        return blockchain_db.lastBlock()

    # the genesis block is the first block in the blockchain
    def genesisBlock(self):
        # the first block has height 0
        block_height = 0
        # the first block has not a previous_block_hash, so create it manually
        prev_block_hash = ZERO_HASH
        self.addBlock(block_height, prev_block_hash)

    def addBlock(self, block_height, prev_block_hash):
        timestamp = int(time.time())
        
        coinbase_instance = CoinbaseTransaction(block_height)
        coinbase_tx = coinbase_instance.coinbaseTX()
        # combine the hash of all transactions using merkle_root, encode the transaction and then format in hex
        merkle_root = coinbase_tx.tx_id
        # in simple terms bits are the target
        bits = 'ffff001f'
        # create the block header
        block_header = BlockHeader(VERSION, prev_block_hash, merkle_root, timestamp, bits)
        # mine
        block_header.mine()
        # after mined a block, add it to the blockchain by creating an instance of our block
        # transform the Block class and BlockHeader class in a dictionary result and put all in a list
        self.writeOnDisk([Block(block_height, 1, block_header.__dict__, 1, coinbase_tx.toDictionary()).__dict__])
    
    def main(self):
        last_block = self.fetchLastBlock()
        if last_block is None:
            self.genesisBlock()
        # add the last block created from the mining to our chain. This process will continue always to connect block each other
        while True:
            # take the last block
            last_block = self.fetchLastBlock()
            block_height = last_block['height'] + 1
            prev_block_hash = last_block['block_header']['block_hash']
            self.addBlock(block_height, prev_block_hash)

# in python we have __name__ that is a special built-in variable. If a file is run directly, __name__ is set to __main__ automatically. If the file is imported as a module, __name__ will be the file name
if __name__ == '__main__':
    blockchain = Blockchain()
    blockchain.main()


