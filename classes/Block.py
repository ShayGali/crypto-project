from dataclasses import dataclass
import dataclasses as dc
from datetime import datetime
import TransactionException
import rsa
from utilities import get_fields_str
import hashlib
import Message
from typing import Callable, List


@dataclass
class Block:
    prev_block_hash: str
    index: int
    messages: List[Message]
    current_block_hash: str = dc.field(init=False)
    time_added: datetime = dc.field(init=False)
    nonce: int = dc.field(init=False)   # A counter used for the proof-of-work algorithm

    TOKEN_PRIZE = 3

    # Returns str of all data members -> called by compute_block_hash()
    def compute_block_header(self) -> bytes:
        block_str = \
            get_fields_str(self.prev_block_hash, self.index, self.messages, self.time_added, self.nonce)
        return block_str.encode()

    # Returns a hashed str of all data members
    def compute_block_hash(self) -> str:
        """
        computes the hash of the block using SHA-256 algorithm
        :return: the hash in hexadecimal
        """
        block_hash = hashlib.sha256(self.compute_block_header()).hexdigest()
        self.current_block_hash = block_hash
        return block_hash

    def seal_block(self):
        self.time_added = datetime.now()
        self.current_block_hash = self.compute_block_hash()


    # TODO: the Method - SHAY
    # natan's code - maybe can help with the solution of this method
    def validate_block(self):
        """
        1. validate integrity of each transaction
        2. validate integrity of chain of transactions
        :return:
        """
        for index, transaction in enumerate(self.transactions):
            try:
                transaction.validate_integrity()
                # now, check the integrity of the chain of messages
                # self.prev_trans_hash = prev_trans.trans_hash
                if index > 0 and transaction.prev_trans_hash != self.transactions[index - 1].trans_hash:
                    raise TransactionException.BlockException("Block creation failed due linking problem in transaction number: "
                                         + index)
            except TransactionException as tte:
                raise TransactionException.BlockException("Block creation failed due to validation problem in transaction number: "
                                     + index + str(tte))

