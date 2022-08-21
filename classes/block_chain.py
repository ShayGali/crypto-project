from dataclasses import dataclass
from typing import List
from transaction import Transaction
from exceptions import TransactionException
from block import Block


@dataclass
class BlockChain:
    unverified_transactions: List[Transaction]
    chain: List[Block]

    def __post_init__(self):
        genesis_block = Block(1,[],"0")  # GENESIS_BLOCK is the first block in the chain
        self.chain.append(genesis_block)

    # adds block to chain
    def add_block(self, block, miner):
        is_valid = block.validate_block(lambda block2: True)
        if is_valid:
            self.create_block(miner)

    # adds temporary transactions to a new block
    def create_block(self, miner):
        new_block = Block(
            len(self.chain)+1,
            self.unverified_transactions,
            self.chain[-1].compute_block_hash(),
            # True,  # TODO: this is for updating 'proof' attribute in Block class
            miner.address
        )
        miner.set_tokens(new_block.TOKEN_PRIZE)
        self.unverified_transactions.clear()

    def add_transaction_to_queue(self,transaction):
        if isinstance(transaction, Transaction):
            if len(self.unverified_transactions) > 0:  # to add here
                transaction.link_transactions(self.unverified_transactions[-1])
            transaction.seal()
            # check that there is no tempering between seal() and appending the transaction
            transaction.validate_integrity()
            if transaction.sender.validate_enough_tokens(transaction.message.amount):
                self.unverified_transactions.append(transaction)
            else:
                raise TransactionException("you don't have enough tokens")



