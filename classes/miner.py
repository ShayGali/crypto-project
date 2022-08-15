from dataclasses import dataclass
import rsa


@dataclass
class Miner:
    tokens: float
    address: rsa.PublicKey


    # TODO: mining a new block ?
    def mine_block(self):
        pass
