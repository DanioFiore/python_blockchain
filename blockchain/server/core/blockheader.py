from blockchain.server.utils.utils import hash256

class BlockHeader:
    def __init__(self, version, previous_block_hash, merkle_root, timestamp, bits):
        self.version = version
        self.previous_block_hash = previous_block_hash
        # A Merkle root is the result of hashing the transactions in a block, pairing those hashes, and hashing them again until a single hash remains
        self.merkle_root = merkle_root
        # when the block is created
        self.timestamp = timestamp
        self.bits = bits
        self.nonce = 0
        self.block_hash = ''

    def mine(self):
        # in order to create the block hash, we have to concatenate all together and pass the fields as an input to hash256 that will generate an hash and that hash will check if it has the leading 0000 or not
        while (self.block_hash[0:4]) != '0000':
            # we have to pass all as a string, so cast all the vars that are not string and encode all
            # the function will return a response in a bite format so we have to convert it in hexadecial
            # like this we can have the block hash
            self.block_hash = hash256((str(self.version) + self.previous_block_hash + self.merkle_root + str(self.timestamp) + self.bits + str(self.nonce)).encode()).hex()
