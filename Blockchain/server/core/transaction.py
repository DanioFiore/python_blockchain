from Blockchain.server.core.script import Script
class Transaction:
    # the version is used because transaction in a bitcoin network can have different versions with different features
    # ins = the input used to transfer money
    # outs = the output where the money will be sent to
    # if we have defined the locktime, for example a transaction cannot go inside the blockchain until block number 1001 was mined
    def __init__(self, version, transaction_ins, transaction_outs, locktime):
        self.version = version
        self.transaction_ins = transaction_ins
        self.transaction_outs = transaction_outs
        self.locktime = locktime

class TransactionIn:
    def __init__(self, prev_transaction, prev_index, script_sig = None, sequence = 0xffffffff):
        self.prev_transaction = prev_transaction
        self.prev_index = prev_index
        self.script_sig = (Script() if script_sig is None else script_sig)
        self.sequence = sequence

class TransactionOut:
    def __init__(self, amount, script_pubkey):
        # the amount of money that is being sent to the recipient
        self.amount = amount
        # the recipient's public key
        self.script_pubkey = script_pubkey