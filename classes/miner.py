from dataclasses import dataclass
import dataclasses as dc
import rsa


@dataclass
class Miner:
    tokens: float
    address: rsa.PublicKey = dc.field(init=False)
    private_key: rsa.PrivateKey = dc.field(init=False)

    def __post_init__(self):
        self.address, self.private_key = rsa.newkeys(512)

    def address_as_str(self):
        return str(self.address)

    # TODO: mining a new block ?
    def mine_block(self):
        pass

# if __name__ == '__main__':
#     m = Miner(5.0)
#     print(m)