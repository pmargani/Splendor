
from typing import Optional
import random
import copy

from CardsLevel0 import AllCardsLevel0
from CardsLevel1 import AllCardsLevel1
from CardsLevel2 import AllCardsLevel2

RANDOM_STRATEGY = "RANDOM"
CHEAPEST_STRATEGY = "CHEAPEST"
STRATEGIES = [RANDOM_STRATEGY, CHEAPEST_STRATEGY]

COLORS = ["red", "blue", "green", "white", "black"]

COLORS_DICT = {color: 0 for color in COLORS}

class Card:
    """
    Represents a card in the game Splendor.
    Attributes:
        points (int): The number of points the card is worth.
        color (str): The color of the card.
        level (int, optional): The level of the card. Defaults to 0.
        cost (dict, optional): The cost to acquire the card, represented as a dictionary where keys are colors and values are the number of coins required. Defaults to None.
        owner (str, optional): The owner of the card. Defaults to None.
    """    

    def __init__(self,  color: str, level: Optional[int]=0, points: Optional[int]=0, cost: Optional[dict]=None, owner: Optional[str] = None):
        self.points = points
        self.color = color
        self.level = level
        self.owner = owner
        self.cost = cost

    def get_filtered_cost(self):
        """
        Returns a dictionary of the cost items where the amount is greater than zero.
        Returns:
            dict: A dictionary with color as keys and positive amounts as values.
        """

        return {color: amount for color, amount in self.cost.items() if amount > 0}

    def get_cost_total_coins(self):
        """
        Calculate the total cost in coins.
        This method sums up the values of all the coins in the cost dictionary.
        Returns:
            int: The total amount of coins.
        """

        return sum(amount for amount in self.cost.values())

    def get_cost_total_num_colors(self):
        """
        Calculate the total number of different colors required for the cost.
        This method counts the number of different colors (or types of resources) 
        that have a cost greater than zero.
        Returns:
            int: The total number of different colors with a non-zero cost.
        """

        return len([amount for amount in self.cost.values() if amount > 0])
    
    def get_weighted_cost(self):
        """
        The ease of buying a card is not just the total coins it costs.
        It is also how that cost is distributed.  Since a player can only take
        a certain number of coins for each turn, that makes it harder to buy
        cards that don't have a wide cost distribution.
        In other words, it's easier to buy card A whose cost is 4, 1 per color, then 
        card B whose cost is 3, all just one color!  
        So how to represent this in just one number?
        card A: 4 cost / 4 colors = 1
        card B: 3 cost / 1 color = 3
        """
        return self.get_cost_total_coins() / self.get_cost_total_num_colors()

    def __repr__(self) -> str:
        return f"Card(points={self.points}, color={self.color}, level={self.level}, cost={self.get_filtered_cost()}, owner={self.owner})"

    def __eq__(self, other):
        if not isinstance(other, Card):
            return False
        return (self.points == other.points and
                self.color == other.color and
                self.level == other.level and
                self.owner == other.owner and
                self.cost == other.cost)

class Coin:

    """
    Represents a Coin in the game Splendor
    """

    def __init__(self, color: str, owner: Optional[str] = None, wild: bool = False):
        self.color = color
        self.owner = owner
        self.wild = wild

    def __repr__(self) -> str:
        return f"Coin(color={self.color}, owner={self.owner}, wild={self.wild})"


class Noble:

    """
    Represents a Noble in the game Splendor
    """
    
    def __init__(self, points: int, colors: list, owner: str):
        self.points = points
        self.colors = colors
        self.owner = owner

    def __repr__(self) -> str:
        return f"Noble(points={self.points}, colors={self.colors}, owner={self.owner})"
    
class Player:
    """
    Represents a player in the game Splendor.
    Attributes:
        name (str): The name of the player.
        strategy (str): The strategy used by the player.
        coins (list): The list of coins the player has.
        cards (list): The list of cards the player has.
        nobles (list): The list of nobles the player has.
        max_coins (int): The maximum number of coins a player can have.
    """

    
    def __init__(self, name: str, strategy: str = RANDOM_STRATEGY):
        self.name = name
        self.strategy = strategy
        self.coins = []
        self.cards = []
        self.nobles = []

        self.max_coins = 10

    def add_coin(self, coin: Coin):
        self.coins.append(coin)

    def add_card(self, card: Card):
        self.cards.append(card)

    def add_noble(self, noble: Noble):
        self.nobles.append(noble)

    def can_add_coin(self):
        """
        Check if a coin can be added to the collection.
        Returns:
            bool: True if the number of coins is less than the maximum allowed, False otherwise.
        """

        return len(self.coins) < self.max_coins

    def get_total_points(self):
        """
        Calculate the total points from cards and nobles.
        Returns:
            int: The total points accumulated from both cards and nobles.
        """

        return sum(card.points for card in self.cards) + sum(noble.points for noble in self.nobles)

    def get_coins_dict(self):
        """
        Generate a dictionary representing the count of each coin color.
        This method iterates through the list of coins and counts the number of coins for each color.
        The result is a dictionary where the keys are the colors and the values are the counts of coins of that color.
        Returns:
            dict: A dictionary with coin colors as keys and their respective counts as values.
        """

        coins_dict = {color: 0 for color in COLORS}
        for coin in self.coins:
            if coin.color in coins_dict:
                coins_dict[coin.color] += 1
            else:
                coins_dict[coin.color] = 1
        return coins_dict

    def get_cards_dict(self):
        """
        Generate a dictionary representing the count of cards for each color.
        This method iterates through the cards in the `self.cards` list and counts 
        the number of cards for each color defined in the `COLORS` list. The result 
        is a dictionary where the keys are colors and the values are the counts of 
        cards of that color.
        Returns:
            dict: A dictionary with colors as keys and the count of cards of each 
            color as values.
        """

        cards_dict = {color: 0 for color in COLORS}
        for card in self.cards:
            if card.color in cards_dict:
                cards_dict[card.color] += 1
            else:
                cards_dict[card.color] = 1
        return cards_dict       

    def get_colors_dict(self):
        """
        Generate a dictionary that combines the counts of cards and coins for each color.
        This method retrieves the counts of cards and coins for each color from their respective
        dictionaries and sums them up to create a combined dictionary.
        This is used as a way to know what the resources are that a player has
        for purchasing another Card.
        Returns:
            dict: A dictionary where the keys are colors and the values are the combined counts
                  of cards and coins for each color.
        """

        colors_dict = {}
        cards_dict = self.get_cards_dict()
        coins_dict = self.get_coins_dict()
        for color in COLORS:
            colors_dict[color] = cards_dict[color] + coins_dict[color]
        return colors_dict

    def get_cost_difference(self, card: Card):
        """
        Calculate the difference in cost between the player's available resources and the card's cost.
        Args:
            card (Card): The card for which the cost difference is being calculated.
        Returns:
            dict: A dictionary where the keys are the resource colors and the values are the differences 
              between the card's cost and the player's available resources for each color.
        """

        player = self.get_colors_dict()
        diff = {}
        for color, colorCost in card.cost.items():
            diff[color] = colorCost - player[color]
        return diff
        
    def can_afford_card(self, card: Card):
        """
        Determines if the player can afford a given card based on their current resources.
        Args:
            card (Card): The card to check affordability for. The card has a cost attribute which is a dictionary
                         mapping resource colors to their respective costs.
        Returns:
            bool: True if the player can afford the card, False otherwise.
        """

        colors_dict = self.get_colors_dict()
        for color, cost in card.cost.items():
            if colors_dict.get(color, 0) < cost:
                return False
        return True

    def can_take_coin(self):
        """
        Determines if a coin can be taken based on the current number of coins.
        Returns:
            bool: True if the number of coins is less than the maximum allowed, False otherwise.
        """

        return len(self.coins) < self.max_coins
    
    def __repr__(self) -> str:
        return f"Player(name={self.name}, coins={self.coins}, cards={self.cards}, nobles={self.nobles})"

    def description(self):
        coins_dict = self.get_coins_dict()
        total_points = self.get_total_points()
        return f"Player {self.name} has {coins_dict} coins, {len(self.cards)} cards, and {total_points} points."


class Game:

    """
    Represents a Splendor Game; that is, the 'board' (cards, coins, nobles)
    and the Players.  The game manages the flow of the game, including taking turns,
    and ending the game when certain states are reached.
    Attributes:
        num_players (int): The number of players in the game.
        winning_points (int): The number of points needed to win the game.
        shuffle (bool): Whether to shuffle the cards at the start of the game.
        strategy (str): The strategy used by the players.
    """
    def __init__(self, 
        num_players=4,
        max_turns=None,
        winning_points=15,
        shuffle=True,
        strategy=None
        ):

        self.num_players = num_players
        self.winning_points = winning_points
        self.shuffle = shuffle
        self.strategy = strategy

        self.cards = [[],[],[]]

        self.players = []
        self.nobles = []
        self.turn = 0
        self.num_turns = 0
        self.current_player = None
        self.final_state = None
        self.num_stuck_turns = 0
        
        self.max_turns = max_turns

        self.num_colors = 5
        self.num_coins_per_color = 6
        self.num_total_coins = self.num_colors * self.num_coins_per_color
        self.max_coins_per_turn = 3
        self.min_coins_for_two = 4
        self.num_turns_take_two_coins = 0

        self.num_card_levels = 3
  
        self.num_cards_visible = 4


        self.init_game()

    def init_game(self):

        # Create players based on self.num_players
        for i in range(self.num_players):
            player = Player(name=f"player{i + 1}", strategy=self.strategy)
            self.add_player(player)
        self.current_player = self.players[0]
        
        # make stacks of coins of each color
        self.colors = COLORS #["red", "blue", "green", "white", "black"]
        self.coins = {color: [Coin(color, None) for _ in range(self.num_coins_per_color)] for color in self.colors}

        allCardsLevel0 = copy.deepcopy(AllCardsLevel0)
        allCardsLevel1 = copy.deepcopy(AllCardsLevel1)
        allCardsLevel2 = copy.deepcopy(AllCardsLevel2)
        allCardLevels = [allCardsLevel0, allCardsLevel1, allCardsLevel2]
        for level, allCards in enumerate(allCardLevels):
            for color, costs in allCards.items():
                for cost in costs:
                    points = cost.pop("points", 0)
                    card = Card(color=color, level=level, points=points, cost=cost)
                    self.add_card(card, level)
        if self.shuffle:    
            for level in range(self.num_card_levels):    
                random.shuffle(self.cards[level])
        self.max_total_points = sum(card.points for level in self.cards for card in level)

        self.num_cards = len(self.cards[0]) + len(self.cards[1]) + len(self.cards[2])

    def get_winner(self):
        max_points = -1
        winner = None
        for player in self.players:
            player_points = player.get_total_points()
            if player_points > max_points:
                max_points = player_points
                winner = player
        return winner
        
    def next_turn(self):
        self.turn = (self.turn + 1) % len(self.players)
        self.num_turns += 1

    def get_current_player(self):
        return self.players[self.turn]
        
    def add_player(self, player: Player):
        self.players.append(player)

    def add_card(self, card: Card, level: int):
        self.cards[level].append(card)

    # def add_coin(self, coin: Coin):
        # self.coins.append(coin)

    def add_noble(self, noble: Noble):
        self.nobles.append(noble)

    def get_average_score(self):
        """
        Calculate the average score of all players in the game.

        Returns:
            float: The average score of all players.
        """
        total_points = sum(player.get_total_points() for player in self.players)
        return total_points / len(self.players) if self.players else 0
    
    def take_next_coin(self, current_player):
        took_coin = None
        for color, coins in self.coins.items():
            if coins:
                coin = coins.pop()
                coin.owner = current_player.name
                current_player.add_coin(coin)
                print(f"{current_player.name} takes a {color} coin")
                took_coin = coin
                break
        return took_coin

    def take_coins(self, current_player):
        took_coin = None
        for cointTake in range(self.max_coins_per_turn):
            if current_player.can_take_coin():
                # print(f"{current_player.name} takes a coin")
                took_coin = self.take_next_coin(current_player)
            else:
                break    
        return took_coin

    def num_coins_available(self):
        return sum([len(coinsOfColor) for _, coinsOfColor in self.coins.items()])
    
    def are_coins_available(self):
        return self.num_coins_available() > 0
    
    def take_two_coins_for_card(self, current_player, card):

        # should you take two?  can you?
        # what is the difference between what the player has and what the card costs?
        needs = current_player.get_cost_difference(card)
        print(f"needs {needs} for card {card}")
        for color, numCoins in needs.items():
            if numCoins >= 2 and len(self.coins[color]) >= self.min_coins_for_two:
                self.take_coin_of_color(current_player=current_player, color=color)
                self.take_coin_of_color(current_player=current_player, color=color)
                self.num_turns_take_two_coins += 1
                return False
            
        # if not
        return False
    
    def take_coins_for_card(self, current_player, card):
        print(f"take_coins_for_card {card}")
        took_coin = None
        took_colors = []
        if self.take_two_coins_for_card(current_player, card):
            return True
        for coinTake in range(self.max_coins_per_turn):
            print(f"coinTake: {coinTake}")
            if current_player.can_take_coin() and self.are_coins_available():
                # print(f"{current_player.name} takes a coin")
                took_coin = self.take_coin_for_card(current_player, card, took_colors)
                if took_coin is None:
                    took_coin = self.take_random_coin(current_player, took_colors)
                if took_coin is not None:
                    took_colors.append(took_coin.color)
            else:
                break    
        return took_coin

    def color_with_no_coins(self):
        return [color for color, coins in self.coins.items() if not coins]
    
    def take_random_coins(self, current_player: Player):
        """
        Allows the current player to take random coins up to the maximum allowed per turn.

        Args:
            current_player (Player): The player who is taking the coins.

        Returns:
            bool: True if a coin was successfully taken, False otherwise.
        """
        took_coin = None
        coins_taken = []
        for i in range(self.max_coins_per_turn):
            # print(f"coinTake: {i}")
            if current_player.can_take_coin():
                disallowed = self.color_with_no_coins() + coins_taken
                took_coin = self.take_random_coin(current_player, disallowed_colors=disallowed)
                # print(f"took_coin: {took_coin}")
                if not took_coin:
                    break
                # ensures we don't take that color again this turn
                coins_taken.append(took_coin.color)
            else:
                break
        return took_coin
    
    def take_random_coin(self, current_player: Player, disallowed_colors: list):
        available_colors = [color for color, coins in self.coins.items() if coins and color not in disallowed_colors]
        if not available_colors:
            return None
        color = random.choice(available_colors)
        return self.take_coin_of_color(current_player, color)
        

    def buy_random_card(self, current_player):
        """
        Attempts to buy a random card for the current player.
        This method iterates through the available card levels and visible cards,
        checking if the current player can buy any of the cards. If a card can be
        bought, it is purchased and a message is printed indicating the purchase.
        If the player cannot buy a card, a message is printed indicating the
        player's inability to buy the card.
        Args:
            current_player (Player): The player attempting to buy a card.
        Returns:
            bool: True if a card was successfully bought, False otherwise.
        """

        for level in range(self.num_card_levels):
            for card in self.cards[level][:self.num_cards_visible]:
                if self.can_buy_card(current_player, card):
                    bought_card = self.buy_card(current_player, card)
                    if bought_card:
                        print(f"{current_player.name} buys {card}")
                        return True
                else:
                    print(f"{current_player.name} {current_player.get_colors_dict()} cannot buy {card}")    
        return False

    def buy_cheapest_card(self, current_player):
        """
        Allows the current player to buy the cheapest available card from the visible cards.
        Args:
            current_player (Player): The player who is attempting to buy a card.
        Returns:
            cheapest_card: what card did they want to buy?
            bool: True if a card was successfully bought, False otherwise.
        The method finds the cheapest card that the current player can buy from the visible cards.
        If a card is bought, it is added to the player's collection, removed from the visible cards,
        and the corresponding coins are deducted from the player's coins and returned to the bank.
        """

        # well first just buy any card that can be afforded
        for level in range(self.num_card_levels):
            for card in self.cards[level][:self.num_cards_visible]:
                if current_player.can_afford_card(card):
                    self.buy_card(current_player, card)
                    return card, True 
            
        cheapest_card = None
        # what's the cheapest card?
        for level in range(self.num_card_levels):
            for card in self.cards[0][:self.num_cards_visible]:
                print(f"checking card {card} w/ weighted cost {card.get_weighted_cost()}")
                if cheapest_card is None or card.get_weighted_cost() < cheapest_card.get_weighted_cost():
                    cheapest_card = card

        if cheapest_card and current_player.can_afford_card(cheapest_card):
            self.buy_card(current_player, cheapest_card)
            print(f"{current_player.name} buys {cheapest_card}")
            return cheapest_card, True
        
        return cheapest_card, False
    
    def buy_most_expensive_card(self, current_player):
        # TBF: this does not buy most expensive card yet, just buys
        # first one it can afford starting at the most expensive level
        bought_card = False
        last_card = None
        for level in range(self.num_card_levels - 1, -1, -1):
            for card in self.cards[level][:self.num_cards_visible]:
                if self.can_buy_card(current_player, card):
                    # remove card from board and add to player
                    current_player.add_card(card)
                    self.cards[level].remove(card)
                    # remove coins from Player and add back to board
                    for color, amount in card.cost.items():
                        for _ in range(amount):
                            for coin in current_player.coins:
                                if coin.color == color:
                                    current_player.coins.remove(coin)
                                    self.coins[color].append(coin)
                                    break
                    print(f"{current_player.name} buys {card}")
                    bought_card = True
                    last_card = card
                    break
                else:
                    last_card = card
            if bought_card:
                break
        return bought_card, last_card

    def buy_card(self, player: Player, card: Card):
        """
        Allows a player to buy a card if they have the necessary resources.

        This method checks if the player can buy the specified card. If the player can buy the card,
        it deducts the required resources (first using cards, then using coins if necessary), 
        adds the card to the player's collection, and removes the card from the available cards.

        Args:
            player (Player): The player attempting to buy the card.
            card (Card): The card the player wants to buy.

        Returns:
            bool: True if the player successfully buys the card, False otherwise.
        """
        if self.can_buy_card(player, card):
            # add card to player and remove from game board
            player.add_card(card)
            self.cards[card.level].remove(card)
            # now pay for the card
            for color, amount in card.cost.items():
                needs_coins = amount
                for _ in range(amount):
                    # first pay using cards
                    for card in player.cards:
                        if card.color == color:
                            needs_coins -= 1
                # pay the reminaing balance in coins            
                if needs_coins > 0:
                    for _ in range(needs_coins):           
                        for coin in player.coins:
                            if coin.color == color:
                                print(f"{player.name} spends coin {color}")
                                # remove coin from player and give back to board
                                player.coins.remove(coin)
                                self.coins[color].append(coin)
                                break
            print(f"{player.name} buys {card}")
            return True
        return False
    
    def take_coin_for_card(self, current_player: Player, card: Card, disallowed_colors: list):

        took_coin = None

        # what is the difference between what the player has and what the card costs?
        needs = current_player.get_cost_difference(card)
        print(f"needs {needs} for card {card}")

        # for each color, try to get one of these
        for color, num in needs.items():
            if len(self.coins[color]) > 0 and color not in disallowed_colors and num > 0:
                took_coin = self.take_coin_of_color(current_player, color)
                if took_coin is not None:
                    return took_coin
                
        return took_coin        

    def take_coin_of_color(self, current_player, color):
        took_coin = None
        # t = sum([len(c) for c in self.coins.values()])
        # print(f"num coins on board: {t}")
        if self.coins[color]:
            
            # print(f"num coins {color} coins on baord: {len(self.coins[color])}")
            coin = self.coins[color].pop()
            # print(f"after pop num coins {color} coins on baord: {len(self.coins[color])}")

            coin.owner = current_player.name
            current_player.add_coin(coin)
            # print(f"{current_player.name} takes a {color} coin")
            took_coin = coin

        # t = sum([len(c) for c in self.coins.values()])
        # print(f"now num coins on board: {t}")

        return took_coin
    
    def take_turn(self):
        """
        Executes the actions for the current player's turn.
        The current player is determined and their turn is announced. 
        The player's strategy is checked, and the appropriate action is taken.
        Returns:
            None
        """

        current_player = self.get_current_player()
        self.current_player = current_player
        print(f"{current_player.name}'s turn")

        took_turn = False
        if current_player.strategy == RANDOM_STRATEGY:
            took_turn = self.take_turn_random_strategy(current_player)
        elif current_player.strategy == CHEAPEST_STRATEGY:
            took_turn = self.take_turn_cheapest_strategy(current_player)
        else:
            raise "Only one supported strategy currently"
        if not took_turn:
            self.num_stuck_turns += 1
        else:
            self.num_stuck_turns = 0    

    def take_turn_cheapest_strategy(self, current_player):
        """
        Executes a turn for the given player using the cheapest card strategy.

        The player will first attempt to buy the cheapest available card. If no card is bought,
        the player will then take coins needed for the cheapest card.

        Args:
            current_player (Player): The player whose turn it is to take an action.

        Returns:
            None
        """
        cheapest_card, bought_card = self.buy_cheapest_card(current_player)
        if not bought_card and cheapest_card:
            return self.take_coins_for_card(current_player, cheapest_card)
        return bought_card 
    
    def take_turn_random_strategy(self, current_player):
        """
        Executes a turn for the given player using a random strategy.

        The player will first attempt to buy a random card. If no card is bought,
        the player will then take random coins.

        Args:
            current_player (Player): The player whose turn it is to take an action.

        Returns:
            None
        """

        bought_card = self.buy_random_card(current_player)
        if not bought_card:
            return self.take_random_coins(current_player)
        return bought_card
    
    def play_game(self, interactive=True):
        """
        Play a game of Splendor.

        This method manages the flow of the game, including validating the game state,
        taking turns, and checking for game-over conditions. It can be run in interactive
        mode, where the user is prompted to press Enter to continue to the next turn.

        Args:
            interactive (bool): If True, the game will prompt the user to press Enter to
                                continue to the next turn. Default is True.

        Returns:
            None
        """

        if not self.validate_game_state():
            print("Game state is invalid.")
            return

        if interactive:
            input("Press Enter to continue to the next turn...")

        while not self.is_game_over():
            self.take_turn()
            if not self.validate_game_state():
                print("Game state is invalid.")
                break
            self.describe()

            if interactive:
                input("Press Enter to continue to the next turn...")
            self.next_turn()

    def is_game_over(self):
        """
        Checks if the game is over based on the maximum number of turns 
        or if any player has reached the winning points.

        Returns:
            bool: True if the game is over, False otherwise.
        """
        if self.max_turns is not None and self.num_turns >= self.max_turns:
            print("Game over: maximum number of turns reached.")
            self.final_state = "max_turns"
            return True
        # Example condition: game ends when a player has 15 points
        for player in self.players:
            if sum(card.points for card in player.cards) >= self.winning_points:
                print(f"{player.name} wins the game!")
                self.final_state = "winning_points"
                return True
        # if self.num_coins_available() == 0:
            # print("No coins left on the board.")
            # self.final_state = "no_coins"
            # return True
        if self.num_stuck_turns == self.num_players:
            print("every player is stuck")
            self.final_state = "players_stuck"
            return True   
        
        return False

    def can_buy_card(self, player: Player, card: Card):
        return player.can_afford_card(card)

    def __repr__(self) -> str:
        return f"Game(players={self.players}, cards={self.cards}, coins={self.coins}, nobles={self.nobles})"

    def describe_players(self):
        for player in self.players:
            print(player.description())

    def describe_coins(self):
        print("Board Coins:")
        for color, coins in self.coins.items():
            print(f"{color}: {len(coins)}")

    def describe_cards(self):
        print("Visible Cards:")
        for level, cards in enumerate(self.cards):
            print(f"Level {level}:")
            for card in cards[:self.num_cards_visible]:
                print(card)

    def describe(self):
        print(f"Game with {self.num_players} players and {self.num_turns} turns played.")
        self.describe_players()
        self.describe_coins()
        self.describe_cards()

    def validate_game_state(self):
        # Validate the total number of coins
        total_coins = sum(len(coins) for coins in self.coins.values())
        player_coins = sum(len(player.coins) for player in self.players)
        if total_coins + player_coins != self.num_total_coins:
            print(f"Coin count mismatch: board coins={total_coins} + player coins={player_coins} != {self.num_total_coins}")
            return False

        # Validate the total number of cards
        total_cards = sum(len(cards) for cards in self.cards)
        player_cards = sum(len(player.cards) for player in self.players)
        if total_cards + player_cards != self.num_cards:
            print(f"Card count mismatch: {total_cards + player_cards} != {self.num_cards}")
            return False

        # Validate the total number of nobles

        # Validate the total number of points
        total_points = sum(card.points for level in self.cards for card in level)
        player_points = sum(player.get_total_points() for player in self.players)
        assert self.max_total_points > 0
        if total_points + player_points != self.max_total_points:
            print(f"Point count mismatch: {total_points + player_points} != {self.max_total_points}")
            return False
        # else:
            # print(f"Point count match: {total_points} + {player_points} == {self.max_total_points}")

        print("Game state is valid.")
        return True


def main():
    game = Game()
    game.play_game()

if __name__ == "__main__":
    main()