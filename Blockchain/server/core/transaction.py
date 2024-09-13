"""
1. Transaction class: This class represents a transaction in the blockchain. It has the following attributes:
    version: Represents the version of the transaction. Different versions can have different features.
    transaction_ins: Represents the inputs used to transfer money. It is a list of TransactionIn objects.
    transaction_outs: Represents the outputs where the money will be sent to. It is a list of TransactionOut objects.
    locktime: Represents the locktime of the transaction. It specifies a condition for when the transaction can be added to the blockchain.
2. TransactionIn class: This class represents an input used in a transaction. It has the following attributes:
    prev_transaction: Represents the previous transaction's hash.
    prev_index: Represents the index of the output in the previous transaction that is being spent.
    script_sig: Represents the script signature that authorizes the spending of the previous transaction's output. If not provided, it defaults to an empty Script object.
    sequence: Represents the sequence number. It is used to control the order of transactions in a block.
3. TransactionOut class: This class represents an output in a transaction. It has the following attributes:
amount: Represents the amount of money being sent to the recipient.
script_pubkey: Represents the recipient's public key. It is used to verify the recipient's identity when the transaction is being spent.


These classes form the basic building blocks of a transaction in a blockchain system, enabling the transfer of funds between participants.
"""

from Blockchain.server.core.script import Script
class Transaction:
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