import datetime
from dataclasses import dataclass
from typing import List
from transaction import Transaction
from block import Block
from datetime import datetime


@dataclass
class BlockChain:
    unverified_transactions: List[Transaction]
    chain: List[Block]

    def __post_init__(self):
        genesis_block = Block(1,[],"0")  # GENESIS_BLOCK is the first block in the chain
        self.chain.append(genesis_block)

    # add block to chain
    def add_block(self, block):
        is_valid = block.validate_block()
        if is_valid:
            self.chain.append(block)

    # adds temporary transactions to a new block
    def create_block(self, miner):
        new_block = Block(
            len(self.chain)+1,
            self.unverified_transactions,
            self.chain[-1].compute_block_hash(),
            # True,  # TODO: this is for updating 'proof' attribute in Block class
            miner.address
        )
        miner.tokens += new_block.TOKEN_PRIZE
        self.unverified_transactions.clear()
        self.add_block(new_block)

    # TODO: validate if its possible to transfer
    #       the amount of tokens from the sender to the receiver
    def add_transaction_to_queue(self,transaction):
        if isinstance(transaction, Transaction):
            if len(self.unverified_transactions) > 0:  # to add here
                transaction.link_transactions(self.unverified_transactions[-1])
            transaction.seal()
            # check that there is no tempering between seal() and appending the transaction
            transaction.validate_integrity()
            self.unverified_transactions.append(transaction)



