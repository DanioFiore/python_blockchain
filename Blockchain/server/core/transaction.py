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
script_pub_key: Represents the recipient's public key. It is used to verify the recipient's identity when the transaction is being spent.


These classes form the basic building blocks of a transaction in a blockchain system, enabling the transfer of funds between participants.
"""

from Blockchain.server.core.script import Script
from Blockchain.server.tools.tools import intToLittleEndian, bytesNeeded, decodeBase58, littleEndianToInt, encodeVarInt, hash256

ZERO_HASH = b'\0' * 32
REWARD = 50 # miner reward

PRIVATE_KEY = '65266629941907463941282944902653750347563149523387475133429792088025011748586' # private key for testing, to have it run account.py as main and copy Private Key
MINER_ADDRESS = '1BzcZDjL4ZkERkVp1vpHQDd57KX4q4WQXK' # miner's address for testing, to have it run account.py as main and copy Public Address
class Transaction:
    def __init__(self, version, transaction_ins, transaction_outs, locktime):
        self.version = version
        self.transaction_ins = transaction_ins
        self.transaction_outs = transaction_outs
        self.locktime = locktime

    def id(self):
        """
        Human-readable identifier of the transaction.
        """
        return self.hash().hex()

    def hash(self):
        """
        Binary Hash of serialization of the transaction.
        """
        return hash256(self.serialize())[::-1]

    def serialize(self):
        """
        Serialize the transaction object into a byte array.

        Returns:
        bytes: A byte array representing the serialized transaction object.
        """
        result = intToLittleEndian(self.version, 4)
        result += encodeVarInt(len(self.transaction_ins))

        for tx_in in self.transaction_ins:
            result += tx_in.serialize()

        result += encodeVarInt(len(self.transaction_outs))
        for tx_out in self.transaction_outs:
            result += tx_out.serialize()
        
        result += intToLittleEndian(self.locktime, 4)

        return result


    def isCoinbase(self):
        """
        Check if the transaction is a coinbase transaction.

        Returns:
        bool: True if the transaction is a coinbase transaction, False otherwise.
        """
        if len(self.transaction_ins) != 1:
            return False
        first_input = self.transaction_ins[0]
        if first_input.prev_transaction != b'\x00' * 32:
            return False
        if first_input.prev_index != 0xffffffff:
            return False
        
        return True


    def toDictionary(self):
        """
        Convert the transaction object into a dictionary format.

        If the transaction is a coinbase transaction, perform necessary conversions on the attributes.

        Returns:
        dict: A dictionary representation of the transaction object.
        """
        if self.isCoinbase():
            self.transaction_ins[0].prev_transaction = self.transaction_ins[0].prev_transaction.hex()
            self.transaction_ins[0].script_sig.cmds[0] = littleEndianToInt(self.transaction_ins[0].script_sig.cmds[0])
            self.transaction_ins[0].script_sig = self.transaction_ins[0].script_sig.__dict__

        self.transaction_ins[0] = self.transaction_ins[0].__dict__

        self.transaction_outs[0].script_pub_key.cmds[2] = self.transaction_outs[0].script_pub_key.cmds[2].hex()
        self.transaction_outs[0].script_pub_key = self.transaction_outs[0].script_pub_key.__dict__
        self.transaction_outs[0] = self.transaction_outs[0].__dict__

        return self.__dict__

class TransactionIn:
    def __init__(self, prev_transaction, prev_index, script_sig = None, sequence = 0xffffffff):
        self.prev_transaction = prev_transaction
        self.prev_index = prev_index
        if script_sig is None:
            self.script_sig = Script()
        else:
            self.script_sig = script_sig
        self.sequence = sequence

    def serialize(self):
        result = self.prev_transaction[::-1] # reverse the order
        result += intToLittleEndian(self.prev_index, 4)
        result += self.script_sig.serialize()
        result += intToLittleEndian(self.sequence, 4)

        return result

class TransactionOut:
    def __init__(self, amount, script_pub_key):
        # the amount of money that is being sent to the recipient
        self.amount = amount
        # the recipient's public key
        self.script_pub_key = script_pub_key

    def serialize(self):
        result = intToLittleEndian(self.amount, 8)
        result += self.script_pub_key.serialize()

        return result

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
        coinbase_tx = Transaction(1, tx_ins, tx_outs, 0)
        coinbase_tx.tx_id = coinbase_tx.id()
        return coinbase_tx
