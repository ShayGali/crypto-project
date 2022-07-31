class TransactionException(Exception):
    def __init__(self, *args):
        Exception.__init__(self, *args)

class BlockException(Exception):
    def __init__(self,*args):
        Exception.__init__(self,*args)

class BlockChainException(Exception):
    def __init__(self,*args):
        Exception.__init__(self,*args)
