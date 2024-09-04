# our main file
import sys
# all our modules now are in python_blockchain folder
sys.path.append('/home/danio/personal/wa/python_blockchain')

from blockchain.server.core.block import Block
from blockchain.server.core.block_header import BlockHeader
from blockchain.server.utils.utils import hash256
import time

# manual hash of the genesis block
ZERO_HASH = '0' * 64
# our blockchain version
VERSION = 1
class Blockchain:
    def __init__(self):
        self.chain = []
        self.GenesisBlock()

    # the genesis block is the first block in the blockchain
    def GenesisBlock(self):
        # the first block has height 0
        block_height = 0
        # the first block has not a previous_block_hash, so create it manually
        prev_block_hash = ZERO_HASH
        self.addBlock(block_height, prev_block_hash)

    def addBlock(self, block_height, prev_block_hash):
        timestamp = int(time.time())
        # create a dummy transaction for no
        transaction = f"Danio sent {block_height} Bitcoins to Fabio"
        # combine the hash of all transactions using merkle_root, encode the transaction and then format in hex
        merkle_root = hash256(transaction.encode()).hex()
        # in simple terms bits are the target
        bits = 'ffff001f'
        # create the block header
        block_header = BlockHeader(VERSION, prev_block_hash, merkle_root, timestamp, bits)
        # mine
        block_header.mine()
        # after mined a block, add it to the blockchain by creating an instance of our block
        self.chain.append(Block(block_height, 1, block_header, 1, transaction))
        print(self.chain)

# in python we have __name__ that is a special built-in variable. If a file is run directly, __name__ is set to __main__ automatically. If the file is imported as a module, __name__ will be the file name
if __name__ == '__main__':
    blockchain = Blockchain()

