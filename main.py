# Import the needed guff
from tiles import *
from random import shuffle, randint
from itertools import cycle
from time import sleep


# Create a Player class
class Player:
    def __init__(self, name):
        self.name = name
        self.pos = 0
        self.balance = 1500
        self.properties = {}
        self.jailCards = 0
        self.jailTurns = 0

    def __str__(self):
        out = ""
        if not self.properties:
            out = "No properties"
            return out
        for group, props in self.properties.items():
            out += f"\n{group}: "
            out += ", ".join([p.name for p in props])
        return out.lstrip("\n")

    def _remove_empty(self):
        self.properties = {k: v for k, v in self.properties.items() if v}

    def move(self, roll, passGoMoney=True):
        newPos = (self.pos + sum(roll)) % 40
        if newPos < self.pos and passGoMoney:
            self.balance += 200
        self.pos = newPos

    def move_to(self, destination, passGoMoney=True):
        if destination < self.pos and passGoMoney:
            self.balance += 200
        self.pos = destination

    def get_out_of_jail(self, useCard=True, rolledDouble=False):
        if rolledDouble:
            self.pos = 10
        elif useCard and self.jailCards:
            self.jailCards -= 1

            self.pos = 10
        else:
            self.balance -= 50
            board[20].moneyPot += 50

    def pay_rent(self, tile, roll=None):
        if tile.tileType == "Property":
            rentDue = tile.rents[tile.houses]
            self.balance -= rentDue
            tile.owner.balance += rentDue
        elif tile.tileType == "Station":
            numberOwned = len(tile.owner.properties["Station"])
            rentDue = tile.rents[numberOwned]
            self.balance -= rentDue
            tile.owner.balance += rentDue
        elif tile.tileType == "Utility":
            numberOwned = len(tile.owner.properties["Utility"])
            if numberOwned == 1:
                rentDue = sum(roll) * 4
            else:
                rentDue = sum(roll) * 10
            self.balance -= rentDue
            tile.owner.balance += rentDue

    def buy_tile(self, tile):
        try:
            self.properties[tile.group].append(tile)
        except KeyError:
            self.properties[tile.group] = [tile]
        tile.owner = self
        self.balance -= tile.price

    def sell_tile(self, tile):
        tileOwned = False
        for properties in self.properties.values():
            try:
                properties.remove(tile)
                tileOwned = True
            except ValueError:
                pass
        if tile.mortgaged:
            self.balance += tile.price / 2
        else:
            self.balance += tile.price
        self._remove_empty()

    def buy_houses(self, group, num):
        for tile in self.properties[group]:
            tile.houses += num
            self.balance -= num * tile.housePrice

    def sell_houses(self, group, num):
        for tile in self.properties[group]:
            tile.houses -= num
            self.balance += num * tile.housePrice

    def street_repairs(self):
        pass


# Simulates a two dice roll
def roll():
    return randint(1, 6), randint(1, 6)


def get_card(player, deck):
    if deck == "Chance":
        card = chanceCards.pop(0)
    else:
        card = chestCards.pop(0)

    returnCard = True
    cardtype = card[0][0]
    print("Your card says: ")
    print(card[1], end=" ")

    if cardtype == "M":
        if card[0][1] == "-":
            player.move((card[0][1:]))
        else:
            player.move_to(card[0][1:])

    elif cardtype == "F":
        money = int(card[0][1:])
        print(f"£{money}")
        player.balance -= money
        board[20].moneyPot += money
    elif cardtype == "P":
        if card[0][1] == "B":
            for p in filter(lambda p: p.name != player.name, players):
                p.balance -= card[0][2:]
                player.balance += card[0][2:]
        else:
            p.balance += card[0][1:]

    elif cardtype == "J":
        player.jailCards += 1
        returnCard = False

    elif cardtype == "C":
        chanceChoice = input("\nWould you like to pay the fine (F) or take a Chance (C)?").lower()
        if chanceChoice == "c":
            get_card(player, "Chance")
        else:
            player.balance -= 10
            board[20].moneyPot += 10

    if returnCard:
        if deck == "Chance":
            chanceCards.append(card)
        else:
            chestCards.append(card)


# Get the information gubbins from the .csv files
with open("board.csv", encoding='utf-8-sig') as file:
    tiles = [tile.split(",") for tile in file.read().split("\n")]
    tiles = [list(filter(None, t)) for t in tiles]
    board = []
    for tile in tiles:
        eval(f"board.append({tile[0]}(*tile))")
    board.append(Jail())
    board.sort(key=lambda l: l.pos)

with open("chance.csv", encoding='utf-8-sig') as file:
    chanceCards = [card.split(",") for card in file.read().splitlines(False)]
    shuffle(chanceCards)

with open("communitychest.csv", encoding='utf-8-sig') as file:
    chestCards = [card.split(",") for card in file.read().splitlines(False)]
    shuffle(chestCards)


# Create the players
players = [Player(a) for a in range(4)]


# Main game logic loop
for player in cycle(players):
    print("-" * 40)
    r = roll()

    # Special handling for if the player is in Jail (at the ususally unreachable pos 40)
    if player.pos == 40:
        if r[0] == r[1]:
            player.get_out_of_jail(rolledDouble=True)
            print(f"Player {player.name}, you rolled a double {r[0]} so you have left jail")
            player.pos = 10
            player.jailTurns = 0
        elif player.jailCards > 0:
            freeChoice = input("Would you like to use your Get Out Of Jail Free card? [Y/N]: ").lower()
            if freeChoice == "y":
                player.jailCards -= 1
                player.pos = 10
                player.jailTurns = 0
                print("You have been released from jail")
        elif player.balance > 50:
            payChoice = input("Would like to pay £50 to leave jail early? [Y/N]: ").lower()
            if payChoice == "y":
                player.balance -= 50
                board[20].moneyPot += 50
                player.jailTurns = 0
                player.pos = 10
        else:
            player.jailTurns += 1
        if player.jailTurns == 3:
            print("You have done your jail time, so you have been released")
            player.pos = 10
            player.jailTurn = 0
        else:
            print("You cannot leave jail at this time")

    # If the player isn't in jail, move the player and allow the player to decide what action to take
    else:
        player.move(r)
        currentTile = board[player.pos]
        print(f"Player {player.name}, you rolled a {r[0]} and a {r[1]}")
        print(f"You landed on {currentTile.name}")

        if currentTile.isbuyable:
            if currentTile.owner is not None:
                player.pay_rent(currentTile, r)
                print(f"You have paid Player {currentTile.owner.name}. Current balance: £{player.balance}")
            elif player.balance > currentTile.price:
                buyChoice = input(f"This tile is available to buy for £{currentTile.price}. "
                                  f"Current balance: £{player.balance} Purchase it? [Y/N]").lower()
                buyChoice = "y"
                if buyChoice == "y":
                    player.buy_tile(currentTile)
                    print(f"You have bought {currentTile.name}. Current balance: £{player.balance}")
            else:
                print("You cannot afford to buy this porperty")

        elif currentTile.tileType == "CommunityChest":
            get_card(player, "CommunityChest")

        elif currentTile.tileType == "Chance":
            get_card(player, "Chance")

        elif currentTile.tileType == "Tax":
            player.balance -= currentTile.taxValue
            board[20].moneyPot += currentTile.taxValue
            print(f"You have paid {currentTile.taxValue} into the Free Parking money pot. "
                  f"Current balance: £{player.balance}")

        elif currentTile.tileType == "GoToJail":
            player.move_to(40, passGoMoney=False)
            print("You have been put in jail. Wait for your next turn to roll a double, use a card or pay to get out")

        elif currentTile.tileType == "FreeParking":
            amountCollected = currentTile.moneyPot
            player.balance += currentTile.moneyPot
            currentTile.moneyPot = 500
            print(f"You collected {amountCollected}. Current balace: £{player.balance}")

        print(f"\nWould you like to :")
        print("  A. Buy/sell houses")
        print("  B. View your own properties")
        print("  C. View other players' properties")
        print("Any other key will pass play to the next player")
        menuChoice = input().lower()

        if menuChoice == "a":
            fullSets = {}
            for group, props in player.properties.items():
                if group not in ("Station", "Utility") and props[0].groupSize == len(props):
                    fullSets += {group, props}
                    print(f"{group} has {props[0].houses} houses")
            if not fullSets:
                print("You own no complete sets")
            else:
                print(f"Enter colour+number to buy a number of houses (eg. Green+2), "
                      f"colour-number to sell a number of houses (eg. Green-3)")
                houseChoice = input()
                if "+" in houseChoice:
                    houseChoice = houseChoice.split("+")
                    player.buy_houses(houseChoice[0], int(houseChoice[1]))
                elif "-" in houseChoice:
                    houseChoice = houseChoice.split("-")
                    player.sell_houses(houseChoice[0], int(houseChoice[1]));

        elif menuChoice == "b":
            print(player)

        elif menuChoice == "c":
            for p in filter(lambda p: p.name != player.name, players):
                if str(p) == "No properties":
                    print(f"{p.name}:\n  {p}")
                else:
                    print(f"{p.name}:")
                    print(''.join("  " + line for line in str(p).splitlines(True)))
