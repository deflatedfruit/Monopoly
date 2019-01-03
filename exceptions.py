class MonopolyError(Exception):
    pass


class PurchaseError(MonopolyError):
    def __init__(self, message=None):
        if message is not None:
            self.message = message

class OwnershipError(MonopolyError):
    def __init__(self, message=None):
        if message is not None:
            self.message = message


class MoneyError(MonopolyError):
    def __init__(self, message=None):
        if message is not None:
            self.message = message


class HouseError(MonopolyError):
    def __init__(self, message=None):
        if message is not None:
            self.message = message