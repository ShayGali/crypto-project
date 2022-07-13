from dataclasses import dataclass
import dataclasses as dc
from datetime import datetime
import exceptions
import rsa
from utilities import get_fields_str
from rsa import VerificationError

@dataclass
class Message:
    # data
    timestamp: datetime=dc.field(init=False)
    amount:float
    sender_addr:rsa.PublicKey
    receiver_addr:rsa.PublicKey
    # encryption segment
    message_signature:bytes=dc.field(default=b'')

    def __post_init__(self):
        self.timestamp = datetime.now()

    def message_as_bytes(self) -> bytes:
        message_str = get_fields_str(self.timestamp, self.amount, self.sender_addr, self.receiver_addr)
        return message_str.encode()

    def sign_message(self,sender_priv_key:rsa.PrivateKey,hash_algo:str)->None:
        known_hashes = ['MD5', 'SHA-1','SHA-224', 'SHA-256', 'SHA-384','SHA-512']
        if hash_algo not in known_hashes:
            raise exceptions.TransactionException("Hash method is not valid")
        self.message_signature = rsa.sign(self.message_as_bytes(),sender_priv_key,hash_algo)
        # verify that the original message corresponds to the signed message
        self.verify()

    def verify_message(self)->None:
        """
        This method validates the integrity of the signed message using the following:
        the data used for signing, the signature itself and the public key
        :param self:
        :return:None or raise VerificationError when the signature doesn't match the message.
        """
        try:
            hash_method_name = rsa.verify(self.message_as_bytes(),self.message_signature,self.sender_addr)
            return hash_method_name
        except VerificationError as ve:
            raise exceptions.TransactionException("Verification failed: " + str(ve))


# if __name__ == '__main__':
#     sender_public_key, sender_priv_key = rsa.newkeys(512)
#     print(f"public key = {sender_public_key},private key = {sender_priv_key}")





