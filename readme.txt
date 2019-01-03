Reference for chance.csv and communitychest.csv
┏━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Code ┃ Meaning                   ┃ Modifyer ┃ Meaning                           ┃
┣━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃ Mn   ┃ Move the player to tile n ┃ -        ┃ Move the player backwards n tiles ┃
┃ Pn   ┃ Pay the player £n         ┃ B        ┃ Receive £n from each player       ┃
┃ R    ┃ Street Repairs            ┃ [1 or 2] ┃ Use prices 1 or 2                 ┃
┃ Fn   ┃ Fine the player £n        ┃          ┃                                   ┃
┃ J    ┃ Get out of jail free      ┃          ┃                                   ┃
┃ C    ┃ £10 fine or take a chance ┃          ┃                                   ┃
┗━━━━━━┻━━━━━━━━━━━━━━━━━━━━━━━━━━━┻━━━━━━━━━━┻━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

Information:
Chance/Community Chest cards: http://jumbloid.blogspot.com/2008/06/monopoly-cards.html
All property rents (I changed Picadilly w/ 0 houses to £24 as it should be that anyway): http://www.jdawiseman.com/papers/trivia/monopoly-rents.html
I wrote some more python code to generate the above table using the Unicode box chars (only viewable in monospaced fonts). For the code message me