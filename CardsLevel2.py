R = "red"
U = "blue"
G = "green"
W = "white"
B = "black"

PNTS = "points"

# each color has six cards with the following points:
# 3, 4, 4, 5
# and costs
# 14, 7, 12, 10
RedCards = [
    {W: 3, G: 3, B: 3, U: 5, PNTS: 3},
    {U: 3, R: 3, G: 6, PNTS: 4},
    {G: 7, PNTS: 4},
    {R: 3, G: 7, PNTS: 5}
]

BlackCards = [
    {W: 3, U: 3, R: 3, G: 5, PNTS: 3},
    {G: 3, B: 3, R: 6, PNTS: 4},
    {R: 7, PNTS: 4},
    {B: 3, R: 7, PNTS: 5}
]

GreenCards = [
    {B: 3, R: 3, U: 3, W: 5, PNTS: 3},
    {W: 3, G: 3, U: 6, PNTS: 4},
    {U: 7, PNTS: 4},
    {G: 3, U: 7, PNTS: 5}
]

WhiteCards = [
    {G: 3, B: 3, U: 3, R: 5, PNTS: 3},
    {R: 3, W: 3, B: 6, PNTS: 4},
    {B: 7, PNTS: 4},
    {W: 3, B: 7, PNTS: 5}
]

BlueCards = [
    {R: 3, W: 3, G: 3, B: 5, PNTS: 3},
    {B: 3, U: 3, W: 6, PNTS: 4},
    {W: 7, PNTS: 4},
    {U: 3, W: 7, PNTS: 5}
]
# RedCards = {
#     {W: 3, G: 3, B: 3, U: 5, PNTS: 3},
#     {U: 3, R: 3, G: 6, PNTS: 4},
#     {G: 7, PNTS: 4},
#     {R: 3, G: 7, PNTS: 5}    
# }

# BlackCards = {
#     {W: 3, U: 3, R: 3, G: 5, PNTS: 3},
#     {G: 3, B: 3, R: 6, PNTS: 4},
#     {R: 7, PNTS: 4},
#     {B: 3, R: 7, PNTS: 5}    
# }

# GreenCards = {
#     {B: 3, R: 3, U: 3, W:: 5, PNTS: 3},
#     {W: 3, G: 3, U: 6, PNTS: 4},
#     {U: 7, PNTS: 4},
#     {G: 3, U: 7, PNTS: 5}
# }

# WhiteCards = {
#     {G: 3, B: 3, U: 3, R: 5, PNTS: 3},
#     {R: 3, W: 3, B: 6, PNTS: 4},
#     {B: 7, PNTS: 4},
#     {W: 3, B: 7, PNTS: 5}
# }

# BlueCards = {
#     {R: 3, W: 3, G: 3, B: 5, PNTS: 3},
#     {B: 3, U: 3, W: 6, PNTS: 4},
#     {W: 7, PNTS: 4},
#     {U: 3, W: 7, PNTS: 5}
# }

AllCardsLevel2 = {
    "black": BlackCards,
    "white": WhiteCards,
    "blue": BlueCards,
    "red": RedCards,
    "green": GreenCards
}