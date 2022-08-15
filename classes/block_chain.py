import datetime
from dataclasses import dataclass
from typing import List
from transaction import Transaction
from block import Block
from datetime import datetime


@dataclass
class BlockChain:
    temp_transactions: List[Transaction]
    chain: List[Block]

    def __post_init__(self):
        genesis_block = Block(1,[],"0")  # GENESIS_BLOCK is the first block of the chain
        self.chain.append(genesis_block)

    # TODO: create add block method
    def add_block(self, block):
        is_valid = block.validate_block()
        if is_valid:
            self.chain.append(block)

    # TODO: adds temp transactions to a new block
    def create_block(self, miner):
        new_block = Block(
            len(self.chain)+1,
            self.temp_transactions,
            self.chain[-1].compute_block_hash(),
            True,
            miner.address
        )
        miner.tokens += new_block.TOKEN_PRIZE
        self.temp_transactions.clear()
        self.add_block(new_block)

    # TODO: add a check if its possible to transfer
    #       the amount of tokens from the sender to the receiver
    def add_transaction(self,transaction):
        if isinstance(transaction, Transaction):
            if len(self.temp_transactions) > 0:
                transaction.link_transactions(self.temp_transactions[-1])
            transaction.seal()
            # check that there is no tempering between seal() and appending the transaction
            transaction.validate_integrity()
            self.temp_transactions.append(transaction)



