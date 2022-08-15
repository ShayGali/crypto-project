from dataclasses import dataclass
import dataclasses as dc
import rsa


@dataclass
class Miner:
    tokens: float
    address: rsa.PublicKey

    def __post_init__(self):
        self.address = rsa.PublicKey.e

    # TODO: mining a new block ?
    def mine_block(self):
        pass

# if __name__ == '__main__':
#     m = Miner(5.0,rsa.newkeys(512))
#     print(m)
