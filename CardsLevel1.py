R = "red"
U = "blue"
G = "green"
W = "white"
B = "black"

PNTS = "points"

# each color has six cards with the following points:
# 1, 1, 2, 2, 2, 3
# and costs
# 7, 8, 5, 7, 8, 6

RedCards = [
    {W: 2, R: 2, B: 3, PNTS: 1},
    {U: 3, R: 2, B: 3, PNTS: 1},
    {B: 5, PNTS: 2},
    {W: 1, U: 4, G: 2, PNTS: 2},
    {W: 3, B: 5, PNTS: 2},
    {R: 6, PNTS: 3}
]


WhiteCards = [
    {B: 2, R: 2, G: 3, PNTS: 1},
    {U: 3, R: 2, B: 3, PNTS: 1},
    {B: 5, PNTS: 2},
    {W: 1, U: 4, G: 2, PNTS: 2},
    {W: 3, B: 5, PNTS: 2},
    {R: 6, PNTS: 3}    
]
BlackCards = [
    {U: 2, R: 2, W: 3, PNTS: 1},
    {W: 3, B: 2, G: 3, PNTS: 1},
    {W: 5, PNTS: 2},
    {U: 1, G: 4, R: 2, PNTS: 2},
    {R: 3, G: 5, PNTS: 2},
    {B: 6, PNTS: 3}    
]

GreenCards = [
    {W: 2, B: 2, U: 3, PNTS: 1},
    {W: 3, G: 2, R: 3, PNTS: 1},
    {G: 5, PNTS: 2},
    {B: 1, W: 4, U: 2, PNTS: 2},
    {G: 3, U: 5, PNTS: 2},
    {G: 6, PNTS: 3}    
]

BlueCards = [
    {G: 2, U: 2, R: 3, PNTS: 1},
    {G: 3, U: 2, B: 3, PNTS: 1},
    {U: 5, PNTS: 2},
    {R: 1, B: 4, W: 2, PNTS: 2},
    {U: 3, W: 5, PNTS: 2},
    {U: 6, PNTS: 3}    
]
   

AllCardsLevel1 = {
    "black": BlackCards,
    "white": WhiteCards,
    "blue": BlueCards,
    "red": RedCards,
    "green": GreenCards
}

expCosts = [ 7, 8, 5, 7, 8, 6]

for thisColor, colorCards in AllCardsLevel1.items():
    costs = []
    for card in colorCards:
        cost = 0
        for color, coins in card.items():
            if color != "points":
                cost += coins
        costs.append(cost)
    # print(costs)    
    assert(costs == expCosts) 