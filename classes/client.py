from dataclasses import dataclass
import dataclasses as dc
import rsa

@dataclass
class Client:
    tokens: float
    address: rsa.PublicKey = dc.field(init=False)
    private_key: rsa.PrivateKey = dc.field(init=False)

    def __post_init__(self):
        self.address, self.private_key = rsa.newkeys(512)

    # TODO: add validations
    def validate_enough_tokens(self, amount):
        if amount < self.tokens:
            return True
        return False


