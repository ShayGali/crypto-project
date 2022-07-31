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
    def __init__(self, *transactions):
        """
        :param transactions: an unknown number of Transaction objects
        """
        self.transactions = list()
        if transactions:
            if all(isinstance(a_transaction,Transaction) for a_transaction in transactions):
                self.transactions.extend(transactions)
        self.timestamp = datetime.now()
        self.blocks = list()

    # def add_block(self,proof):
    #     """
    #     Several miners compete on solving the problem of a new block
    #     remember: blocks include 2 major components:
    #     1. maintain the proof of the block's problem
    #     2. transactions tht did not appear in previous blocks
    #     :param proof:
    #     :return:
    #     """
    #     new_block = {
    #         'location': len(self.blocks),
    #         'proof': proof,
    #         'transactions': self.pending_trans,
    #         'prev_block_hash': DistributedLedger.validate_block_hash(self.blocks[-1])
    #                            if len(self.blocks) > 0 else 1
    #     }
    #     self.pending_trans.clear()
    #     self.blocks.append(new_block)
    #
    # @staticmethod
    # def validate_block_hash(block_json):
    #     # json string representation of a dictionary
    #     block = json.dumps(block_json,sort_keys=True).encode()
    #     block_hash = hashlib.sha256(block).hexdigest()  # returns hexadecimal digits
    #     return block_hash


    def add_block_to_chain(self,a_block):
        if isinstance(a_block,Block):
            if len(self.blocks) > 0 : a_block.prev_block_hash = self.blocks[-1].block_hash
            a_block.seal_block()
            a_block.validate_block()
            self.blocks.append(a_block)
        else:
            raise ValueError("argument is not of type Block")

    def validate_chain(self):
        for index, block in enumerate(self.blocks):
            try:
                block.validate_block()
            except TransactionException.BlockException as bfe:
                raise TransactionException.BlockChainException\
                    ("Blockchain creation failed due to block number = " + index + str(bfe))

    # TODO: Create the method - AVIAL
    def add_trans_to_queue(self, trans: Transaction) -> None:
        pass
    # natan's code - maybe can help with the solution of this method
    def add_transaction(self,transaction) -> None:
        if isinstance(transaction, Transaction):
            if len(self.transactions) > 0:
                transaction.link_transactions(self.transactions[-1])
            transaction.seal()
            # check that there is no tempering between seal() and appending the transaction
            transaction.validate_integrity()
            self.transactions.append(transaction)


