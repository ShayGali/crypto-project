from dataclasses import dataclass
import dataclasses as dc
from datetime import datetime
import TransactionException
import rsa
from classes.Block import Block
from classes.Transaction import Transaction
from utilities import get_fields_str
import hashlib
import Message
from typing import Callable, List


@dataclass
class BlockChain:
    block_head: Block
    block_hash: str

    # TODO: Create the method, return something to Miner - SHIR
    def add_trans_to_block(self) -> None:
        pass

    # TODO: Create the method - AVIAL
    def add_trans_to_queue(self, trans: Transaction) -> None:
        pass
