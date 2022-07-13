from datetime import datetime
import hashlib
import TransactionException

class Transaction:
    def __init__(self,amount,sender,receiver):
        if isinstance(amount,(int,float)) and isinstance((sender,receiver),str):
            self.timestamp = datetime.now()
            self.amount = amount
            self.sender = sender
            self.receiver = receiver
            self.payload_hash = self.compute_payload_hash()
            # both are determined when the transaction is added to the block
            self.prev_trans_hash = None
            self.trans_hash = None

        else:
            raise ValueError("arguments are of incorrect type")

    def compute_payload_hash(self):
        member_str = str(self.timestamp) + str(self.amount) + self.sender + \
                          self.receiver
        members_bytearray = bytearray(member_str, encoding="utf-8")
        """
        Shoshana-> [01010011 01101000 01101111 01110011 01101000 01100001 01101110 01100001]
        """
        return hashlib.sha256(members_bytearray).hexdigest()

    def seal(self):
        """
        this method  is invoked by the Block object.
        It takes a Transaction object as input,
        then computes its hash using the payload hash and the
        previous transaction's hash using sha256 algorithm.
        :return: a hash of the transaction
        """
        trans_hash_str = str(self.payload_hash) + str(self.prev_trans_hash)
        msg_bytearray = bytearray(trans_hash_str,encoding="utf-8")
        self.trans_hash = hashlib.sha256(msg_bytearray).hexdigest()
        return self # return the current object

    def validate_integrity(self):
        """
        if a Transaction is tempered with, payload might be changed. in order to
        check the validity of the transaction, just compute its payload again
        :return:
        """
        if self.payload_hash != self.compute_payload_hash() or self.trans_hash != self.seal():
            raise exceptions.TransactionException("Tempered transaction = " + str(self))

    def link_transactions(self,prev_trans):
        if isinstance(prev_trans,Transaction):
            self.prev_trans_hash = prev_trans.trans_hash
        else:
            raise ValueError("prev_trans argument is not of type Transaction")

    @staticmethod
    def static_link_transactions(current_trans,prev_trans):
        if isinstance((prev_trans,current_trans), Transaction):
            current_trans.prev_trans_hash = prev_trans.trans_hash
        else:
            raise ValueError("one or more argument is not of type Transaction")


    def __repr__(self):
        """
        :return: a string representation of the Transaction's fields
        """
        return "Transaction{\n"+"timestamp=" +str(self.timestamp) + ",\namount=" + str(self.amount) +\
               ",\npayload_hash="+str(self.payload_hash)+"\n}"


