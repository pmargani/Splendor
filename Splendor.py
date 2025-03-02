
from typing import Optional
import random
import copy

from CardsLevel0 import AllCardsLevel0


COLORS = ["red", "blue", "green", "white", "black"]

COLORS_DICT = {color: 0 for color in COLORS}

class Card:
    def __init__(self,  color: str, level: Optional[int]=0, points: Optional[int]=0, cost: Optional[dict]=None, owner: Optional[str] = None):
        self.points = points
        self.color = color
        self.level = level
        self.owner = owner
        self.cost = cost

    def get_filtered_cost(self):
        return {color: amount for color, amount in self.cost.items() if amount > 0}

    def get_cost_total_coins(self):
        return sum(amount for amount in self.cost.values())

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
    def __init__(self, color: str, owner: Optional[str] = None, wild: bool = False):
        self.color = color
        self.owner = owner
        self.wild = wild

    def __repr__(self) -> str:
        return f"Coin(color={self.color}, owner={self.owner}, wild={self.wild})"


class Noble:
    def __init__(self, points: int, colors: list, owner: str):
        self.points = points
        self.colors = colors
        self.owner = owner

    def __repr__(self) -> str:
        return f"Noble(points={self.points}, colors={self.colors}, owner={self.owner})"
    
class Player:
    def __init__(self, name: str):
        self.name = name
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
        return len(self.coins) < self.max_coins

    def get_total_points(self):
        return sum(card.points for card in self.cards) + sum(noble.points for noble in self.nobles)

    def get_coins_dict(self):
        coins_dict = {color: 0 for color in COLORS}
        for coin in self.coins:
            if coin.color in coins_dict:
                coins_dict[coin.color] += 1
            else:
                coins_dict[coin.color] = 1
        return coins_dict

    def get_cards_dict(self):
        cards_dict = {color: 0 for color in COLORS}
        for card in self.cards:
            if card.color in cards_dict:
                cards_dict[card.color] += 1
            else:
                cards_dict[card.color] = 1
        return cards_dict       

    def get_colors_dict(self):
        colors_dict = {}
        cards_dict = self.get_cards_dict()
        coins_dict = self.get_coins_dict()
        for color in COLORS:
            colors_dict[color] = cards_dict[color] + coins_dict[color]
        return colors_dict

    def get_cost_difference(self, card: Card):
        player = self.get_colors_dict()
        diff = {}
        for color, colorCost in card.cost.items():
            diff[color] = colorCost - player[color]
        return diff
        
    def can_afford_card(self, card: Card):
        colors_dict = self.get_colors_dict()
        for color, cost in card.cost.items():
            if colors_dict.get(color, 0) < cost:
                return False
        return True

    def can_take_coin(self):
        return len(self.coins) < self.max_coins
    
    def __repr__(self) -> str:
        return f"Player(name={self.name}, coins={self.coins}, cards={self.cards}, nobles={self.nobles})"

    def description(self):
        coins_dict = self.get_coins_dict()
        total_points = self.get_total_points()
        return f"Player {self.name} has {coins_dict} coins, {len(self.cards)} cards, and {total_points} points."


class Game:

    def __init__(self, 
        num_players=4,
        max_turns=None,
        winning_points=15,
        shuffle=True
        ):

        self.num_players = num_players
        self.winning_points = winning_points
        self.shuffle = shuffle

        self.cards = [[],[],[]]

        self.players = []
        self.nobles = []
        self.turn = 0
        self.num_turns = 0
        self.current_player = None
        self.final_state = None
        
        self.max_turns = max_turns

        self.num_colors = 5
        self.num_coins_per_color = 6
        self.num_total_coins = self.num_colors * self.num_coins_per_color
        self.max_coins_per_turn = 3

        self.num_card_levels = 3
  
        self.num_cards_visible = 4


        self.init_game()

    def init_game(self):

        # Create players based on self.num_players
        for i in range(self.num_players):
            player = Player(name=f"player{i + 1}")
            self.add_player(player)
        self.current_player = self.players[0]
        
        # make stacks of coins of each color
        self.colors = COLORS #["red", "blue", "green", "white", "black"]
        self.coins = {color: [Coin(color, None) for _ in range(self.num_coins_per_color)] for color in self.colors}

        level = 0 

        allCardsLevel0 = copy.deepcopy(AllCardsLevel0)
        for color, costs in allCardsLevel0.items():
            for cost in costs:
                points = cost.pop("points", 0)
                card = Card(color=color, level=level, points=points, cost=cost)
                self.add_card(card, level)
        if self.shuffle:        
            random.shuffle(self.cards[0])
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
    
    def take_coins_for_card(self, current_player, card):
        took_coin = None
        took_colors = []
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
        for _ in range(self.max_coins_per_turn):
            if current_player.can_take_coin():
                
                took_coin = self.take_random_coin(current_player, self.color_with_no_coins())
                if not took_coin:
                    break
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
        cheapest_card = None
        bought_card = False
        for card in self.cards[0][:self.num_cards_visible]:
            # if self.can_buy_card(current_player, card):
            if 1:
                if cheapest_card is None or card.get_cost_total_coins() < cheapest_card.get_cost_total_coins():
                    cheapest_card = card

        if cheapest_card:
            current_player.add_card(cheapest_card)
            self.cards[0].remove(cheapest_card)
            for color, amount in cheapest_card.cost.items():
                for _ in range(amount):
                    for coin in current_player.coins:
                        if coin.color == color:
                            current_player.coins.remove(coin)
                            self.coins[color].append(coin)
                            break
            print(f"{current_player.name} buys {cheapest_card}")
            return True
        return False
    
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
    
    def take_coin_for_card_old(self, current_player, card):
        took_coin = False
        for color, amount in card.cost.items():
            if amount > 0:
                for _ in range(amount):
                    if current_player.can_take_coin() and len(self.coins[color]) > 0:
                        took_coin = self.take_coin_of_color(current_player, color)
                        if took_coin:
                            return took_coin
                    else:
                        break
        return took_coin
    
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
        The current player is determined and their turn is announced. The player
        will attempt to buy the most expensive card possible. If they cannot buy
        a card, they will take coins instead.
        Strategy:
        - Buy the most expensive card possible.
        - If unable to buy a card, take coins for the card last viewed.
        Returns:
            None
        """

        current_player = self.get_current_player()
        self.current_player = current_player
        print(f"{current_player.name}'s turn")

        # Here is where strategy comes into play.  
        # For now we are taking the simplest strategy
        # of always buying the most expensive card possible,
        # otherwise taking coins (strategy TBD)
        # bought_card, last_card_viewed = self.buy_most_expensive_card(current_player)
        bought_card = self.buy_random_card(current_player)
        # print(f"last card viewed: {last_card_viewed}")
        took_coin = False
        if not bought_card:
            # took_coin = self.take_coins(current_player)
            # took_coin = self.take_coins_for_card(current_player, last_card_viewed)
            took_coin = self.take_random_coins(current_player)
    
  
        # Example action: player buys a card if they have enough coins
        # if not took_coin:
        #     for card in self.cards:
        #         if self.can_buy_card(current_player, card):
        #             current_player.add_card(card)
        #             self.cards.remove(card)
        #             print(f"{current_player.name} buys {card}")
        #             break


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
        if self.num_coins_available() == 0:
            print("No coins left on the board.")
            self.final_state = "no_coins"
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