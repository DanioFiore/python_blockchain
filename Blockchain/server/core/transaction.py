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
from Blockchain.server.tools.tools import intToLittleEndian, bytesNeeded, decodeBase58

ZERO_HASH = b'\0' * 32
REWARD = 50 # miner reward

PRIVATE_KEY = '65266629941907463941282944902653750347563149523387475133429792088025011748586' # private key for testing, to have it run account.py as main and copy Private Key
MINER_ADDRESS = '1dwKaRYeHqMXu72dRrDx2AGKDBYKZueZYYvm2CWBCbr3iu7XYWcxfRx4Xd3SmKHbpf9btfzw' # miner's address for testing, to have it run account.py as main and copy Public Address
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
    def __init__(self, amount, script_pub_key):
        # the amount of money that is being sent to the recipient
        self.amount = amount
        # the recipient's public key
        self.script_pub_key = script_pub_key

class CoinbaseTransaction:
    def __init__(self, block_height):
        """
        Initialize a CoinbaseTransaction object with the given block height.

        Parameters:
        block_height (int): The height of the block where the coinbase transaction is created.

        The block_height_in_little_endian attribute is set to the little-endian representation of the block height.
        """
        self.block_height_in_little_endian = intToLittleEndian(block_height, bytesNeeded(block_height))

    def coinbaseTX(self):
        """
        Create a coinbase transaction.

        The coinbase transaction is a special type of transaction that miners include in a block to receive a reward.
        It has a single input (TransactionIn) and a single output (TransactionOut).

        Returns:
        Transaction: A coinbase transaction object with the specified attributes.
        """
        prev_tx_hash = ZERO_HASH
        prev_tx_index = 0xffffffff # this is a number in hexadecimal format

        tx_ins = []
        tx_ins.append(TransactionIn(prev_tx_hash, prev_tx_index))
        tx_ins[0].script_sig.cmds.append(self.block_height_in_little_endian)
        
        tx_outs = []
        target_amount = REWARD * 100000000
        target_hash160 = decodeBase58(MINER_ADDRESS)
        target_script = Script.p2pkh_script(target_hash160)
        tx_outs.append(TransactionOut(amount = target_amount, script_pub_key = target_script))

        return Transaction(1, tx_ins, tx_outs, 0)
