import hashlib
from dataclasses import dataclass
import dataclasses as dc
from datetime import datetime
from message import Message
import exceptions

@dataclass
class Transaction:
    timestamp: datetime = dc.field(init=False)
    message: Message
    # sender: str
    # receiver: str
    # amount: float
    payload_hash: str
    prev_trans_hash: str = dc.field(default=None)
    trans_hash: str = dc.field(default=None)

    def __post_init__(self):
        self.timestamp = datetime.now()
        self.payload_hash = self.compute_payload_hash()
        self.trans_hash = self.__compute_trans_hash()

    def seal(self):
        self.trans_hash = self.__compute_trans_hash()

    def compute_payload_hash(self):
        # member_str = str(self.timestamp) + str(self.amount) + self.sender + self.receiver
        # members_bytearray = bytearray(member_str, encoding="utf-8")
        members_bytearray = self.message.message_as_bytes()
        return hashlib.sha256(members_bytearray).hexdigest()

    def __compute_trans_hash(self):
        """
        this method is invoked by the Block object.
        It takes a Transaction object as input,
        then computes its hash using the payload hash and the
        previous transaction's hash using sha256 algorithm.
        :return: a hash of the transaction
        """
        trans_hash_str = str(self.payload_hash) + str(self.prev_trans_hash)
        msg_bytearray = bytearray(trans_hash_str,encoding="utf-8")
        return hashlib.sha256(msg_bytearray).hexdigest()

    def validate_integrity(self):
        """
        if a Transaction is tempered with, payload might be changed. in order to
        check the validity of the transaction, just compute its payload again
        :return:
        """
        if self.payload_hash != self.compute_payload_hash() or self.trans_hash != self.__compute_trans_hash():
            raise exceptions.TransactionException("Tempered transaction number = " + str(self))

    # TODO: validate that there is no double spending
    def double_spending(self):
        pass

    def link_transactions(self,prev_trans):
        if isinstance(prev_trans,Transaction):
            self.prev_trans_hash = prev_trans.trans_hash
        else:
            raise ValueError("prev_trans argument is not of type Transaction")

    def __repr__(self):
        """
        :return: a string representation of the Transaction's fields
        """
        return "Transaction{\n"+"timestamp=" + str(self.timestamp) + ",\namount=" + str(self.amount) +\
               ",\npayload_hash="+str(self.payload_hash)+"\n}"

