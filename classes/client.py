from dataclasses import dataclass
import dataclasses as dc
import rsa

@dataclass
class Client:
    _tokens: float
    address: rsa.PublicKey = dc.field(init=False)
    _private_key: rsa.PrivateKey = dc.field(init=False)

    def __post_init__(self):
        self.address, self._private_key = rsa.newkeys(512)

    def add_tokens(self, value):
        self._tokens += value

    def subtract_tokens(self, value):
        self._tokens -= value

    def validate_enough_tokens(self, value):
        if value < self._tokens:
            return True
        return False

