R = "red"
U = "blue"
G = "green"
W = "white"
B = "black"
#COLORS = ["red", "blue", "green", "white", "black"]


RedCards = [
    {W: 3},
    {U:2, G: 1},
    {W:2, R: 2},
    {W: 1, U: 1, G: 1, B: 1},
    {W: 4, "points": 1},
    {W: 2, G: 1, B: 2},
    {W: 2, U: 1, G: 1, B: 1},
    {W: 1, R: 1, B: 3},
]

WhiteCards = [
    {U: 3},
    {R: 2, B: 1},
    {U:2, B: 2},
    {U: 1, G: 1, R: 1, B: 1},
    {G: 4, "points": 1},
    {U: 1, G: 2, R: 1, B: 1},
    {U: 2, G: 2, B: 1},
    {W: 3, U: 1, B: 1}
]

BlueCards = [
    {B: 3},
    {W:1, B: 2},
    {G:2, B: 2},
    {W: 1, G: 1, R: 1, B: 1},
    {R: 4, "points": 1},
    {W: 1, G: 1, R: 2, B: 1},
    {B: 1, G: 3, R: 1},
    {W: 1, G: 2, R: 2}
]

BlackCards = [
    {G: 3},
    {G:2, R: 1},
    {W: 2, G: 2},
    {W: 1, U: 1, G: 1, R: 1},
    {B: 4, "points": 1},
    {G: 1, R: 3, B: 1},
    {W: 1, U: 2, G: 1, R: 1},
    {W: 2, U: 2, R: 1}
]

GreenCards = [
    {R: 3},
    {G: 2, U: 1},
    {U: 2, R: 2},
    {W: 1, U: 1, R: 1, B: 1},
    {B: 4, "points": 1},
    {U: 1, R: 2, B: 2},
    {W: 1, B: 3, G: 1},
    {W: 1, U: 1, R: 1, B: 2}
]

AllCardsLevel0 = {
    "black": BlackCards,
    "white": WhiteCards,
    "blue": BlueCards,
    "red": RedCards,
    "green": GreenCards
}

expCosts = [3, 3, 4, 4, 4, 5, 5, 5]

for thisColor, colorCards in AllCardsLevel0.items():
    costs = []
    for card in colorCards:
        cost = 0
        for color, coins in card.items():
            if color != "points":
                cost += coins
        costs.append(cost)
    # print(costs)    
    assert(costs == expCosts)        