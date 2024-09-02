class Block:
    # constructor
    # if capital case, that means is a class that we pass
    def __init__(self, Height, Blocksize, Blockheader, TxCount, Txs):
        # height of the block
        self.Height = Height
        # size of the block
        self.Blocksize = Blocksize
        self.Blockheader = Blockheader
        # number of transactions
        self.TxCount = TxCount
        # transaction itself
        self.Txs = Txs
