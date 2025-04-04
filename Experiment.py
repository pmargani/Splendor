import copy
import os
import json

import matplotlib.pyplot as plt

from Splendor import Game
from Splendor import RANDOM_STRATEGY, CHEAPEST_STRATEGY, POINTS_STRATEGY


class Experiment:
    """
    A class to represent an experiment for running multiple games and analyzing the results.
    Attributes:
    -----------
    name : str
        The name of the experiment.
    game_class : class
        The class representing the game to be played.
    num_games : int
        The number of games to be played in the experiment.
    max_turns : int, optional
        The maximum number of turns allowed in each game (default is None).
    winning_points : int, optional
        The number of points required to win the game (default is 15).
    strategy : function, optional
        The strategy function to be used by the players (default is RANDOM_STRATEGY).
    results : list
        A list to store the results of each game played.
    Methods:
    --------
    run():
        Runs the experiment by playing the specified number of games.
    get_results():
        Returns the results of the experiment.
    analyze_results():
        Analyzes and visualizes the results of the experiment.
    """



    def __init__(self, name, game_class, num_games, max_turns=None, num_players=4, winning_points=15, strategy=RANDOM_STRATEGY, strategies=None):
        self.name = name
        self.game_class = game_class
        self.num_games = num_games
        self.num_players = num_players
        self.max_turns = max_turns
        self.winning_points = winning_points
        self.strategies = strategies
        self.strategy = strategy
        self.results = []

    def run(self):
        """
        Executes a series of games and stores the results.
        This method runs a loop for the number of games specified by `self.num_games`.
        For each iteration, it initializes a game using the provided game class and
        parameters such as `max_turns`, `winning_points`, and `strategy`. The game is
        then played in non-interactive mode, and the result is appended to the `self.results`
        list.
        Returns:
            None
        """

        for igame in range(self.num_games):
            game = self.game_class(
                max_turns=self.max_turns, 
                num_players=self.num_players,
                winning_points=self.winning_points,
                strategy=self.strategy,
                strategies=self.strategies
            )
            # game = self.game_class(max_turns=100, winning_points=1, strategy=RANDOM_STRATEGY)
            game.play_game(interactive=False)
            # input(f"finished game {igame}")
            self.results.append(copy.copy(game))

    def get_results(self):
        return self.results
    

    def analyze_results(self):
        """
        Analyzes the results of the games and generates various histograms and bar charts.
        This method performs the following analyses:
        1. Histogram of the number of turns played in each game.
        2. Histogram of the percentage of turns where two coins were taken.
        3. Histogram of the number of turns played in games where players got stuck.
        4. Bar chart of the final states of the games.
        5. Histogram of the average scores in games that ended with winning points.
        The histograms and bar charts are displayed using matplotlib.
        Returns:
            None
        """

        # Create a directory based on the name of the experiment to store the results
        results_dir = os.path.join(os.getcwd(), self.name)
        if not os.path.exists(results_dir):
            os.makedirs(results_dir)

        # Write the attributes of the Experiment class to a JSON file

        experiment_attributes = {
            "name": self.name,
            "game_class": self.game_class.__name__,
            "num_games": self.num_games,
            "max_turns": self.max_turns,
            "winning_points": self.winning_points,
            "strategy": self.strategy, 
            "strategies": self.strategies,
            # "results": [game.__dict__ for game in self.results]
        }

        with open(os.path.join(results_dir, 'experiment_attributes.json'), 'w') as json_file:
            json.dump(experiment_attributes, json_file, indent=4)

        num_turns = [game.num_turns for game in self.results]
        plt.hist(num_turns, bins=range(min(num_turns), max(num_turns) + 1), edgecolor='black')
        title = f"{self.name}: Number of Turns Played"
        plt.title(title)
        plt.xlabel('Number of Turns')
        plt.ylabel('Frequency')
        plt.savefig(os.path.join(results_dir, f"{title}.png"))
        plt.show()

        num_turns = [int(100*(game.num_turns_take_two_coins / game.num_turns)) for game in self.results]
        plt.hist(num_turns, bins=range(min(num_turns), max(num_turns) + 1), edgecolor='black')
        title = f"{self.name}: Number of Turns Take Two div Played"
        plt.title(title)
        plt.xlabel('Number of Turns')
        plt.ylabel('Frequency')
        plt.savefig(os.path.join(results_dir, f"{title}.png"))
        plt.show()

        num_turns = [game.num_turns for game in self.results if game.final_state=="players_stuck"]
        plt.hist(num_turns, bins=range(min(num_turns), max(num_turns) + 1), edgecolor='black')
        title = f"{self.name}: Number of Turns Played (stuck)"
        plt.title(title)
        plt.xlabel('Number of Turns')
        plt.ylabel('Frequency')
        plt.savefig(os.path.join(results_dir, f"{title}.png"))
        plt.show()

        final_states = [game.final_state for game in self.results]
        unique_states = list(set(final_states))
        state_counts = {state: final_states.count(state) for state in unique_states}

        plt.bar(state_counts.keys(), state_counts.values(), edgecolor='black')
        title =f"{self.name}: Final States"
        plt.title(title)
        plt.xlabel('Final State')
        plt.ylabel('Frequency')
        plt.xticks(rotation=45)
        plt.savefig(os.path.join(results_dir, f"{title}.png"))
        plt.show()

        average_scores = [game.get_average_score() for game in self.results if game.final_state == "winning_points"]
        plt.hist(average_scores, bins=20, edgecolor='black')
        title = f"{self.name}: Average Scores (winning)"
        plt.title(title)
        plt.xlabel('Average Score')
        plt.ylabel('Frequency')
        plt.savefig(os.path.join(results_dir, f"{title}.png"))
        plt.show()

        # Plot the number of wins for each player
        player_wins = {}
        for game in self.results:
            if game.winner is None:
                continue
            winner = game.winner.name + "=" + game.winner.strategy
            if winner not in player_wins:
                player_wins[winner] = 0
            player_wins[winner] += 1

        plt.bar(player_wins.keys(), player_wins.values(), edgecolor='black')
        title = f"{self.name}: Player Wins"
        plt.title(title)
        plt.xlabel('Player')
        plt.ylabel('Number of Wins')
        plt.xticks(rotation=45)
        plt.savefig(os.path.join(results_dir, f"{title}.png"))
        plt.show()


def main():

    # experiment = Experiment2("Experiment2", Game, 1000)  # Replace GameClass with the actual game class name
    # experiment = Experiment("RandomStrategy", Game, 1000, strategy=RANDOM_STRATEGY)
    # experiment = Experiment("CheapestStrategy", Game, 1000, strategy=CHEAPEST_STRATEGY)
    # strategies = [RANDOM_STRATEGY, RANDOM_STRATEGY, POINTS_STRATEGY, POINTS_STRATEGY]
    # strategies = [CHEAPEST_STRATEGY, CHEAPEST_STRATEGY, POINTS_STRATEGY, POINTS_STRATEGY]
    # strategies = [POINTS_STRATEGY, POINTS_STRATEGY, POINTS_STRATEGY, POINTS_STRATEGY]
    strategies = [RANDOM_STRATEGY, CHEAPEST_STRATEGY, POINTS_STRATEGY]
    # experiment = Experiment("MixedStrategy", Game, 1000, strategies=strategies, winning_points=1)
    # experiment = Experiment("MixedStrategy2", Game, 1000, strategies=strategies, winning_points=1)
    # experiment = Experiment("MixedStrategy3", Game, 1000, strategies=strategies, winning_points=15)
    # experiment = Experiment("PointsStrategy", Game, 1000, strategies=strategies, winning_points=15)
    experiment = Experiment("AllStrategy", Game, 100, strategies=strategies, num_players=3, winning_points=15)
    experiment.run()
    print(experiment.get_results())
    experiment.analyze_results()

if __name__ == "__main__":
    main()