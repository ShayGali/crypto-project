import hashlib
from dataclasses import dataclass
from typing import List, Callable, ClassVar
from transaction import Transaction
import dataclasses as dc
from datetime import datetime
from utilities import get_fields_str


@dataclass
class Block:
    index:int
    transactions: List[Transaction]  # list of transactions
    timestamp: datetime = dc.field(init=False)  # time the block got mined
    previous_hash: str  # hash from the previous block
    miner_address: str = dc.field(default=None)

    TOKEN_PRIZE: ClassVar[float] = dc.field(default=.1)  # reword to miner

    def __post_init__(self):
        self.timestamp = datetime.now()

    # Returns str of all data members -> called by compute_block_hash()
    def compute_block_header(self) -> bytes:
        block_str = \
            get_fields_str(self.previous_hash, self.index, self.timestamp, self.nonce)
        return block_str.encode()

    # Returns a hashed str of all data members
    def compute_block_hash(self) -> str:
        """
        computes the hash of the block using SHA-256 algorithm
        :return: the hash in hexadecimal
        """
        block_hash = hashlib.sha256(self.compute_block_header()).hexdigest()
        return block_hash

    def validate_block(self, validate_function: Callable[[any], bool]) -> bool:
        return validate_function(self)



