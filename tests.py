from copy import copy
import unittest
from Splendor import Game, Player, Coin, Card, Noble, COLORS, COLORS_DICT

class TestGame(unittest.TestCase):

    def setUp(self):
        self.game = Game()

    def test_init_game(self):
        self.assertEqual(len(self.game.players), 4)
        self.assertEqual(len(self.game.coins["red"]), 6)
        self.assertEqual(len(self.game.coins["blue"]), 6)
        self.assertEqual(len(self.game.coins["green"]), 6)
        self.assertEqual(len(self.game.coins["white"]), 6)
        self.assertEqual(len(self.game.coins["black"]), 6)

    def test_num_coins_available(self):
        self.assertEqual(self.game.num_coins_available(), 5*6)

    def test_next_turn(self):
        initial_turn = self.game.turn
        self.game.next_turn()
        self.assertEqual(self.game.turn, (initial_turn + 1) % len(self.game.players))

    def test_add_player(self):
        new_player = Player(name="new_player")
        self.game.add_player(new_player)
        self.assertIn(new_player, self.game.players)

    def test_add_card(self):
        level = 0
        new_card = Card(points=1, color="red", level=level, owner=None)
        self.game.add_card(new_card, level)
        self.assertIn(new_card, self.game.cards[0])

    def test_add_noble(self):
        new_noble = Noble(points=3, colors=["red", "blue"], owner=None)
        self.game.add_noble(new_noble)
        self.assertIn(new_noble, self.game.nobles)

    def test_is_game_over(self):
        self.game.max_turns = 2
        self.assertFalse(self.game.is_game_over())
        self.game.num_turns = self.game.max_turns
        self.assertTrue(self.game.is_game_over())

    def test_can_buy_card(self):
        player = self.game.players[0]
        cost = copy(COLORS_DICT)
        cost["red"] = 1
        card = Card(points=1, color="red", level=1, cost=cost, owner=None)
        self.assertFalse(self.game.can_buy_card(player, card))
        player.add_coin(Coin(color="red", owner=player.name))
        self.assertTrue(self.game.can_buy_card(player, card))

    def test_take_next_coin(self):
        player = self.game.players[0]
        self.game.take_next_coin(player)
        self.assertEqual(len(player.coins), 1)
        self.assertEqual(len(self.game.coins["red"]), 5)

    def test_take_random_coin(self):
        player = self.game.players[0]
        
        initial_coin_count = len(player.coins)
        initial_game_coin_count = sum(len(coins) for coins in self.game.coins.values())

        self.game.take_random_coin(player, [])

        self.assertEqual(len(player.coins), initial_coin_count + 1)
        self.assertEqual(sum(len(coins) for coins in self.game.coins.values()), initial_game_coin_count - 1)

    def test_player_buys_card_using_coins_and_cards(self):
        game = Game(shuffle=False)

        self.assertTrue(game.validate_game_state())

        player = game.players[0]

        print(f"card: {game.cards[0][0]}")
        print(f"player: {player}")

        # take 3 green coins
        game.take_coin_of_color(player, "green")
        game.take_coin_of_color(player, "green")
        game.take_coin_of_color(player, "green")

        # black card costs 3 green
        card = game.cards[0][0]
        game.buy_card(player, card)

        self.assertTrue(game.validate_game_state())

        # for i in range(10):
            # print(f"card {i}: {game.cards[0][i]}")
        
        # black card costs 1 green, 3 red, 1 black
        nextCard = game.cards[0][4]
        print(f"next card: {nextCard}")

        # take what we need except a black coin
        game.take_coin_of_color(player, "green")
        game.take_coin_of_color(player, "red")
        game.take_coin_of_color(player, "red")
        game.take_coin_of_color(player, "red")

        # we can buy it because we have 1 black card
        self.assertTrue(game.can_buy_card(player, nextCard))

        game.buy_card(player, nextCard)

        self.assertTrue(game.validate_game_state())

        # we have bought two cards
        self.assertEqual(len(player.cards), 2)
        # and used up all our coins
        self.assertEqual(len(player.coins), 0)

    def test_buy_card(self):

        game = Game(shuffle=False)

        self.assertTrue(game.validate_game_state())

        card = game.cards[0][0]
        print(f"cards: {game.cards[0][:game.num_cards_visible]}")

        player = game.players[0]
        cost = copy(COLORS_DICT)
        cost["red"] = 1
        # card = Card(points=1, color="red", level=1, cost=cost, owner=None)
        
        # Player cannot buy the card initially
        self.assertFalse(game.buy_card(player, card))
        
        # Add coins to the player
        # player.add_coin(Coin(color="red", owner=player.name))
        for i in range(3):
            game.take_coin_of_color(player, "green")
        self.assertTrue(game.validate_game_state())

        # Player can now buy the card
        self.assertTrue(game.buy_card(player, card))
        self.assertTrue(game.validate_game_state())

        self.assertIn(card, player.cards)
        # self.assertEqual(card.owner, player.name)

        self.assertTrue(game.validate_game_state())

class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.player = Player(name="test_player")

    def test_add_coin(self):
        coin = Coin(color="red", owner=self.player.name)
        self.player.add_coin(coin)
        self.assertIn(coin, self.player.coins)

    def test_add_card(self):
        card = Card(points=1, color="red", level=1, owner=self.player.name)
        self.player.add_card(card)
        self.assertIn(card, self.player.cards)

    def test_add_noble(self):
        noble = Noble(points=3, colors=["red", "blue"], owner=self.player.name)
        self.player.add_noble(noble)
        self.assertIn(noble, self.player.nobles)

    def test_get_cost_difference(self):
        cost = copy(COLORS_DICT)
        cost["red"] = 1
        cost["green"] = 2
        card = Card(points=1, cost=cost, color="red", level=1, owner=self.player.name)

        self.player.add_coin(Coin("red"))
        self.player.add_coin(Coin("red"))
        self.player.add_coin(Coin("black"))

        diff = self.player.get_cost_difference(card)

        exp1 = {
            "red": -1,
            "blue": 0,
            "green": 2,
            "white": 0,
            "black": -1
        }
        self.assertEqual(diff, exp1)

        cost = copy(COLORS_DICT)
        cost["blue"] = 1
        cost["black"] = 2
        pcard = Card(points=1, cost=cost, color="green", level=1, owner=self.player.name)
        self.player.add_card(pcard)

        diff = self.player.get_cost_difference(card)

        exp1 = {
            "red": -1,
            "blue": 0,
            "green": 1,
            "white": 0,
            "black": -1
        }
        self.assertEqual(diff, exp1)

    def test_get_colors_dict(self):
        colors_dict = self.player.get_colors_dict()
        self.assertEqual(colors_dict["red"], 0)
        self.assertEqual(colors_dict["blue"], 0)
        self.assertEqual(colors_dict["green"], 0)
        self.assertEqual(colors_dict["white"], 0)
        self.assertEqual(colors_dict["black"], 0)   

    def test_get_coins_dict(self):
        coins_dict = self.player.get_coins_dict()
        self.assertEqual(coins_dict["red"], 0)
        self.assertEqual(coins_dict["blue"], 0)
        self.assertEqual(coins_dict["green"], 0)
        self.assertEqual(coins_dict["white"], 0)
        self.assertEqual(coins_dict["black"], 0)    

        coin = Coin(color="red", owner=self.player.name)
        self.player.add_coin(coin)
        coin = Coin(color="red", owner=self.player.name)
        self.player.add_coin(coin)
        coin = Coin(color="blue", owner=self.player.name)
        self.player.add_coin(coin)

        coins_dict = self.player.get_coins_dict()
        self.assertEqual(coins_dict["red"], 2)
        self.assertEqual(coins_dict["blue"], 1)
        self.assertEqual(coins_dict["green"], 0)
        self.assertEqual(coins_dict["white"], 0)
        self.assertEqual(coins_dict["black"], 0) 

    def test_get_cards_dict(self):  
        cards_dict = self.player.get_cards_dict()
        self.assertEqual(cards_dict["red"], 0)
        self.assertEqual(cards_dict["blue"], 0)
        self.assertEqual(cards_dict["green"], 0)
        self.assertEqual(cards_dict["white"], 0)
        self.assertEqual(cards_dict["black"], 0)   

        card = Card(points=1, color="red", level=1, owner=self.player.name)
        self.player.add_card(card)
        card = Card(points=1, color="red", level=1, owner=self.player.name)
        self.player.add_card(card)
        card = Card(points=1, color="blue", level=1, owner=self.player.name)
        self.player.add_card(card)

        cards_dict = self.player.get_cards_dict()
        self.assertEqual(cards_dict["red"], 2)
        self.assertEqual(cards_dict["blue"], 1)
        self.assertEqual(cards_dict["green"], 0)
        self.assertEqual(cards_dict["white"], 0)
        self.assertEqual(cards_dict["black"], 0)

    def test_get_total_points(self):
        self.assertEqual(self.player.get_total_points(), 0)

        card = Card(points=1, color="red", level=1, owner=self.player.name)
        self.player.add_card(card)
        card = Card(points=1, color="red", level=1, owner=self.player.name)
        self.player.add_card(card)
        card = Card(points=1, color="blue", level=1, owner=self.player.name)
        self.player.add_card(card)

        self.assertEqual(self.player.get_total_points(), 3)

    def test_can_afford_card(self):

        cost = copy(COLORS_DICT)
        cost["red"] = 2

        card = Card(points=1, color="red", level=1, cost=cost, owner=None)
        
        # Player cannot afford the card initially
        self.assertFalse(self.player.can_afford_card(card))

        # Add coins to the player
        self.player.add_coin(Coin(color="red", owner=self.player.name))
        self.player.add_coin(Coin(color="red", owner=self.player.name))
        self.player.add_coin(Coin(color="blue", owner=self.player.name))

        # Player can now afford the card
        self.assertTrue(self.player.can_afford_card(card))

class TestCard(unittest.TestCase):

    def setUp(self):
        self.card = Card(points=1, color="red", level=1, owner=None)

    def test_card_initialization(self):
        self.assertEqual(self.card.points, 1)
        self.assertEqual(self.card.color, "red")
        self.assertEqual(self.card.level, 1)
        self.assertIsNone(self.card.owner)

    def test_get_filtered_cost(self):
        cost = copy(COLORS_DICT)
        cost["red"] = 2
        self.card.cost = cost
        filtered_cost = self.card.get_filtered_cost()
        self.assertEqual(filtered_cost, {"red": 2})


    def test_cost_total_coin(self):
        cost = copy(COLORS_DICT)
        cost["red"] = 2
        cost["green"] = 3
        self.card.cost = cost
        self.assertEqual(self.card.get_cost_total_coins(), 5)

    def test_set_owner(self):
        self.card.owner = "player1"
        self.assertEqual(self.card.owner, "player1")

    def test_card_equality(self):
        card2 = Card(points=1, color="red", level=1, owner=None)
        self.assertEqual(self.card, card2)

    def test_card_inequality(self):
        card2 = Card(points=2, color="blue", level=2, owner=None)
        self.assertNotEqual(self.card, card2)

    def test_get_cost_total_num_colors(self):
        cost = COLORS_DICT.copy()
        cost["red"] = 2
        cost["green"] = 3
        self.card.cost = cost
        self.assertEqual(self.card.get_cost_total_num_colors(), 2)

    def test_get_weighted_cost(self):
        cost = COLORS_DICT.copy()
        cost["red"] = 2
        cost["green"] = 3
        self.card.cost = cost
        self.assertEqual(self.card.get_weighted_cost(), (2 + 3)/2.0)

if __name__ == "__main__":
    unittest.main()

    