class Block:
    # constructor
    # if capital case, that means is a class that we pass
    def __init__(self, height, block_size, block_header, tx_count, txs):
        # height of the block
        self.height = height
        # size of the block
        self.block_size = block_size
        self.block_header = block_header
        # number of transactions
        self.tx_count = tx_count
        # transaction itself
        self.txs = txs
