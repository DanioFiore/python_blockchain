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

    # def mine(self):
