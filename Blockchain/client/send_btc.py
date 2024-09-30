from Blockchain.server.tools.tools import decodeBase58
from Blockchain.server.core.script import Script
from Blockchain.server.core.transaction import TransactionIn, TransactionOut, Transaction
import time
class SendBTC:
    def __init__(self, from_account, to_account, amount, unspend_tx):
        self.coin = 100000000
        self.from_public_address = from_account
        self.to_account = to_account
        self.amount = amount * self.coin
        self.unspend_tx = unspend_tx

    def scriptPubKey(self, public_address):
        h160 = decodeBase58(public_address)
        script_pub_key = Script().p2pkh_script(h160)
        return script_pub_key

    def prepareTransactionIn(self):
        transaction_ins = []
        self.total = 0

        """
        Convert Public Address into Public Hash to find tx_outs that are locked to this hash
        """
        self.from_address_script_pub_key = self.scriptPubKey(self.from_public_address)
        self.from_pub_key_hash = self.from_address_script_pub_key.cmds[2]

        new_unspend_tx = {}

        try:
            while len(new_unspend_tx) < 1:
                new_unspend_tx = dict(self.unspend_tx)
                time.sleep(2)
        except Exception as e:
            print(f"Error in converting the Manage Dict to Normal Dict")

        for transaction_byte in new_unspend_tx:
            if self.total < self.amount:
                transaction_obj = new_unspend_tx[transaction_byte]

                for index, tx_out in enumerate(transaction_obj.tx_outs):
                    if tx_out.script_pub_key.cmds[2] == self.from_pub_key_hash:
                        self.total += tx_out.amount
                        prev_tx = bytes.fromhex(transaction_obj.id())
                        transaction_ins.append(TransactionIn(prev_tx, index))
            else:
                break
        
        if self.total < self.amount:
            self.is_balance_enough = False

        return transaction_ins

    def prepareTransactionOut(self):
        pass

    def prepare_transaction(self):
        self.prepareTransactionIn()
        self.prepareTransactionOut()