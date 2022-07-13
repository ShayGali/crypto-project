from dataclasses import dataclass
import dataclasses as dc
from datetime import datetime
import exceptions
import rsa
from classes.Block import Block
from utilities import get_fields_str
import hashlib
import Message
from typing import Callable, List

@dataclass
class BlockChain:
    block_head: Block
    block_hash: str

    # TODO: Create the method, return something to Miner
    def add_trans_to_block(self) -> None:
        pass

    def add_trans_to_queue(self) -> Transaction:
        pass
