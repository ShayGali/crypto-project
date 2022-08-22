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
    nonce: int = dc.field(init=False)  # A counter used for the proof-of-work algorithm
    proof: bool = dc.field(default=False)  # proof of mining the block
    miner_address: str = dc.field(default=None)  # miner public key address

    TOKEN_PRIZE: ClassVar[float] = dc.field(default=.1)  # reword to miner

    def __post_init__(self):
        """
        initialize the timestamp and the nonce, called right after the object receives values for its fields
        :return: None
        """
        self.timestamp = datetime.now()
        self.nonce = 1

    def compute_block_header(self) -> bytes:
        """
        Returns str of all data members -> called by compute_block_hash() method
        :return: all data members in bytes
        """
        block_str = \
            get_fields_str(self.previous_hash, self.index, self.timestamp, self.nonce)
        return block_str.encode()

    def compute_block_hash(self) -> str:
        """
        computes the hash of the block using SHA-256 algorithm
        :return: the hash in hexadecimal
        """
        block_hash = hashlib.sha256(self.compute_block_header()).hexdigest()
        return block_hash

    def validate_block(self, validate_function: Callable[[any], bool]) -> bool: 
        """
        validate a block by a given callback function
        :param validate_function:
        :return: if the block is valid
        """
        return validate_function(self)

    def proof_of_work(self, prev_nonce):
        """
        checks the miner's solution to the block's problem,
        by checking the first 4 characters of the computed hash.
        :param prev_nonce: the nonce of the previous block in the chain
        :return: the current nonce
        """
        while self.proof is False:
            compute_hash = hashlib.sha256(str(self.nonce**2 - prev_nonce**2).encode()).hexdigest()
            if compute_hash[:4] == '0000':  # more zeros more difficult it will be to mine the block
                self.proof = True
            else:
                self.nonce += 1
        return self.nonce

