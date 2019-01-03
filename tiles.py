from re import sub

class Tile:
    def __init__(self, tileType, pos, name):
        self.tileType = tileType
        self.pos = int(pos)
        self.name = name
        self.isbuyable = False


class BuyableTile(Tile):
    def __init__(self, tileType, pos, name, group, price):
        super().__init__(tileType, pos, name)
        self.isbuyable = True
        self.owner = None
        self.mortgaged = False
        self.price = int(price)
        self.group = group

    def mortgage(self):
        self.mortgaged = True
        self.owner.balance += self.price / 2

    def unmortgage(self):
        self.mortgaged = False
        self.owner.balance -= self.price / 2


class Property(BuyableTile):
    def __init__(self, tileType, pos, name, group, price, housePrice, r0, r1, r2, r3, r4, r5):
        super().__init__(tileType, pos, name, group, price)
        self.housePrice = int(housePrice)
        self.rents = list(map(int, [r0, r1, r2, r3, r4, r5]))
        self.houses = 0
        self.groupSize = 2 if group in ("Brown", "Blue") else 3


class Station(BuyableTile):
    def __init__(self, tileType, pos, name, group, price):
        super().__init__(tileType, pos, name, group, price)
        self.rents = [25, 50, 100, 200]


class Utility(BuyableTile):
    def __init__(self, tileType, pos, name, group, price):
        super().__init__(tileType, pos, name, group, price)


class Chance(Tile):
    def __init__(self, tileType, pos, name):
        super().__init__(tileType, pos, name)


class CommunityChest(Tile):
    def __init__(self, tileType, pos, name):
        super().__init__(tileType, pos, name)


class Tax(Tile):
    def __init__(self, tileType, pos, name, taxValue):
        super().__init__(tileType, pos, name)
        self.taxValue = int(taxValue)


class Go(Tile):
    def __init__(self, tileType, pos, name, passValue=200):
        super().__init__(tileType, pos, name)
        self.passValue = int(passValue)


class FreeParking(Tile):
    def __init__(self, tileType, pos, name):
        super().__init__(tileType, pos, name)
        self.moneyPot = 500


class GoToJail(Tile):
    def __init__(self, tileType, pos, name):
        super().__init__(tileType, pos, name)


class VisitingJail(Tile):
    def __init__(self, tileType, pos, name):
        super().__init__(tileType, pos, name)


class Jail(Tile):
    def __init__(self):
        super().__init__("Jail", 40, "Jail")
