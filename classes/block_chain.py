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
        genesis_block = Block(1,[],"0")
        self.chain.append(genesis_block)

    # TODO: create add block method
    def add_block(self, block):
        is_valid = block.validate_block()
        if is_valid:
            self.chain.append(block)

    # TODO: adds temp transactions to a new block
    def add_trans_to_block(self):
        new_block = Block(
            len(self.chain)+1,
            self.temp_transactions,
            self.chain[-1].compute_block_hash()
        )
        self.add_block(new_block)


