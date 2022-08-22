from dataclasses import dataclass
from typing import List
from transaction import Transaction
from exceptions import TransactionException, BlockChainException
from block import Block
from dataclasses import dataclass
import dataclasses as dc


@dataclass
class BlockChain:
    unverified_transactions: List[Transaction]  # temporary list of unverified transactions
    chain: List[Block] = dc.field(init=False)  # the chain of blocks

    def __post_init__(self):
        """
        creates the GENESIS_BLOCK, this is the first block in the chain,
        called right after the object receives values for its fields
        :return: None
        """
        genesis_block = Block(1,[],"0")
        self.chain.append(genesis_block)

    def add_block(self, block, miner):
        """
        checks if the block is valid and adds the block to chain
        :param block: new block
        :param miner: the current miner who mined the block
        :return: None
        """
        is_valid = block.validate_block(lambda: self.chain[-1].compute_block_hash() == block.compute_block_hash())
        if is_valid:
            self.create_block(miner)

    def create_block(self, miner):
        """
        creates a new block and adds the unverified transactions list to this new block,
        checks the proof of work and mines the to block to miner,
        and sends reward to miner.
        :param miner: the current miner
        :return: None
        """
        new_block = Block(
            self.chain[-1].index+1,
            self.unverified_transactions,
            self.chain[-1].compute_block_hash(),
            False,
            ""
        )
        new_block.proof_of_work(self.chain[-1].nonce)
        if new_block.proof:
            new_block.miner_address = miner.address
            miner.set_tokens(new_block.TOKEN_PRIZE)
            self.unverified_transactions.clear()
        else:
            raise BlockChainException("The block have not been mined")

    def add_transaction_to_queue(self,transaction):
        """
        checks if transaction is valid and checks if it's possible to make the transaction -
        if the sender has the amount of tokens that needed
        :param transaction:
        :return: None
        """
        if isinstance(transaction, Transaction):
            if len(self.unverified_transactions) > 0:
                transaction.link_transactions(self.unverified_transactions[-1])
            transaction.seal()
            # check that there is no tempering between seal() and appending the transaction
            transaction.validate_integrity()
            if transaction.sender.validate_enough_tokens(transaction.message.amount):
                self.unverified_transactions.append(transaction)
                transaction.sender.subtract_tokens(transaction.message.amount)
                transaction.receiver.add_tokens(transaction.message.amount)
            else:
                raise TransactionException("you don't have enough tokens")


