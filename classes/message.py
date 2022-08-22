from dataclasses import dataclass
import dataclasses as dc
from datetime import datetime
import exceptions
import rsa
from rsa import VerificationError
from utilities import get_fields_str

@dataclass
class Message:
    # data
    timestamp: datetime = dc.field(init=False)
    amount:float
    sender_addr:rsa.PublicKey
    receiver_addr:rsa.PublicKey
    # encryption segment
    message_signature:bytes = dc.field(init=False)

    def __post_init__(self):
        """
        initialize the current time, called right after the object receives values for its fields
        :return: None
        """
        self.timestamp = datetime.now()

    def message_as_bytes(self) -> bytes:
        """
        :return: message details in bytes
        """
        message_str = get_fields_str(self.timestamp, self.amount, self.sender_addr, self.receiver_addr)
        return message_str.encode()

    def sign_message(self,sender_priv_key:rsa.PrivateKey,hash_algo:str) -> None:
        """
        signs the message by a given hash algorithm
        :param sender_priv_key: private key of sender
        :param hash_algo: hash algorithm
        :return: None
        """
        known_hashes = ['MD5', 'SHA-1','SHA-224', 'SHA-256', 'SHA-384','SHA-512']
        if hash_algo not in known_hashes:
            raise exceptions.TransactionException("Hash method is not valid")
        self.message_signature = rsa.sign(self.message_as_bytes(),sender_priv_key,hash_algo)
        # verify that the original message corresponds to the signed message
        self.verify_message()

    def verify_message(self) -> str:
        """
        This method validates the integrity of the signed message using the following:
        the data used for signing, the signature itself and the public key
        :return: None or raise VerificationError when the signature doesn't match the message.
        """
        try:
            hash_method_name = rsa.verify(self.message_as_bytes(),self.message_signature,self.sender_addr)
            return hash_method_name
        except VerificationError as ve:
            raise exceptions.TransactionException("Verification failed: " + str(ve))


