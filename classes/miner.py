from dataclasses import dataclass
import dataclasses as dc
import rsa


@dataclass
class Miner:
    _tokens: float = dc.field(init=False)
    address: rsa.PublicKey = dc.field(init=False)
    _private_key: rsa.PrivateKey = dc.field(init=False)

    def __post_init__(self):
        """
        initialize miner's keys, called right after the object receives values for its fields
        :return: None
        """
        self.address, self._private_key = rsa.newkeys(512)
        self._tokens = 0

    def address_as_str(self):
        """
        :return: the address(public key) as string
        """
        return str(self.address)

    def set_tokens(self, value):
        """
        adds tokens to miner's tokens
        :param value: amount of tokens
        :return: None
        """
        self._tokens += value



