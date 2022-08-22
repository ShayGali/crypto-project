from dataclasses import dataclass
import dataclasses as dc
import rsa

@dataclass
class Client:
    _tokens: float = dc.field(init=False)
    address: rsa.PublicKey = dc.field(init=False)
    _private_key: rsa.PrivateKey = dc.field(init=False)

    def __post_init__(self):
        """
        initialize client's keys, called right after the object receives values for its fields
        :return: None
        """
        self.address, self._private_key = rsa.newkeys(512)
        self._tokens = 0

    def add_tokens(self, value):
        """
        adds tokens to client's tokens
        :param value: amount of tokens
        :return: None
        """
        self._tokens += value

    def subtract_tokens(self, value):
        """
        subtracts tokens from client's tokens
        :param value: amount of tokens
        :return: None
        """
        self._tokens -= value

    def validate_enough_tokens(self, value):
        """
        validates if client has enough tokens
        :param value: the amount of tokens to validate
        :return: True or False
        """
        if value < self._tokens:
            return True
        return False

