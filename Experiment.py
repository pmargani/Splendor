import copy

import matplotlib.pyplot as plt

from Splendor import Game
from Splendor import RANDOM_STRATEGY, CHEAPEST_STRATEGY
import os
import json

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


    def __init__(self, name, game_class, num_games, max_turns=None, winning_points=15, strategy=RANDOM_STRATEGY):
        self.name = name
        self.game_class = game_class
        self.num_games = num_games
        self.max_turns = max_turns
        self.winning_points = winning_points
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
            game = self.game_class(max_turns=self.max_turns, winning_points=self.winning_points, strategy=self.strategy)
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
        plt.show()
        plt.savefig(os.path.join(results_dir, f"{title}.png"))

        num_turns = [int(100*(game.num_turns_take_two_coins / game.num_turns)) for game in self.results]
        plt.hist(num_turns, bins=range(min(num_turns), max(num_turns) + 1), edgecolor='black')
        title = f"{self.name}: Number of Turns Take Two div Played"
        plt.title(title)
        plt.xlabel('Number of Turns')
        plt.ylabel('Frequency')
        plt.show()
        plt.savefig(os.path.join(results_dir, f"{title}.png"))

        num_turns = [game.num_turns for game in self.results if game.final_state=="players_stuck"]
        plt.hist(num_turns, bins=range(min(num_turns), max(num_turns) + 1), edgecolor='black')
        plt.title(title)
        title = f"{self.name}: Number of Turns Played (stuck)"
        plt.xlabel('Number of Turns')
        plt.ylabel('Frequency')
        plt.show()
        plt.savefig(os.path.join(results_dir, f"{title}.png"))

        final_states = [game.final_state for game in self.results]
        unique_states = list(set(final_states))
        state_counts = {state: final_states.count(state) for state in unique_states}

        plt.bar(state_counts.keys(), state_counts.values(), edgecolor='black')
        title =f"{self.name}: Final States"
        plt.title(title)
        plt.xlabel('Final State')
        plt.ylabel('Frequency')
        plt.xticks(rotation=45)
        plt.show()
        plt.savefig(os.path.join(results_dir, f"{title}.png"))

        average_scores = [game.get_average_score() for game in self.results if game.final_state == "winning_points"]
        plt.hist(average_scores, bins=20, edgecolor='black')
        title = f"{self.name}: Average Scores (winning)"
        plt.title(title)
        plt.xlabel('Average Score')
        plt.ylabel('Frequency')
        plt.show()
        plt.savefig(os.path.join(results_dir, f"{title}.png"))


def main():

    # experiment = Experiment2("Experiment2", Game, 1000)  # Replace GameClass with the actual game class name
    # experiment = Experiment("Random Strategy", Game, 100, strategy=RANDOM_STRATEGY)
    experiment = Experiment("CheapestStrategy", Game, 100, strategy=CHEAPEST_STRATEGY)
    experiment.run()
    print(experiment.get_results())
    experiment.analyze_results()

if __name__ == "__main__":
    main()