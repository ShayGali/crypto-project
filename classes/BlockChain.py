from dataclasses import dataclass
import dataclasses as dc
from datetime import datetime
import TransactionException
import rsa
from Block import Block
from Transaction import Transaction
from utilities import get_fields_str
import hashlib
import Message
from typing import Callable, List


@dataclass
class BlockChain:
    
        # TODO: return reward to Miner - SHIR
    def __init__(self,*transactions):
        """
        :param transactions: an unknown number of Transaction objects
        """
        self.transactions = list()
        if transactions:
            if all(isinstance(a_transaction,Transaction) for a_transaction in transactions):
                self.transactions.extend(transactions)

    def add_trans_to_block(self,transaction) -> None:
        if isinstance(transaction, Transaction):
            if len(self.transactions) > 0:
                transaction.link_transactions(self.transactions[-1])
            transaction.seal()
            # check that there is no tempering between seal() and appending the transaction
            transaction.validate_integrity()
            self.transactions.append(transaction)
    
    block_head: Block
    block_hash: str

    # TODO: Create the method - AVIAL
    def add_trans_to_queue(self, trans: Transaction) -> None:
        pass
