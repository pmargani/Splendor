import copy

import matplotlib.pyplot as plt

from Splendor import Game
from Splendor import RANDOM_STRATEGY, CHEAPEST_STRATEGY

class Experiment:
    def __init__(self, name, game_class, num_games):
        self.name = name
        self.game_class = game_class
        self.num_games = num_games
        self.results = []

    def run(self):
        for igame in range(self.num_games):
            game = self.game_class(max_turns=100, winning_points=1, strategy=RANDOM_STRATEGY)
            game.play_game(interactive=False)
            # input(f"finished game {igame}")
            self.results.append(copy.copy(game))

    def get_results(self):
        return self.results
    

    def analyze_results(self):
        num_turns = [game.num_turns for game in self.results]
        plt.hist(num_turns, bins=range(min(num_turns), max(num_turns) + 1), edgecolor='black')
        plt.title(f"{self.name}: Number of Turns Played")
        plt.xlabel('Number of Turns')
        plt.ylabel('Frequency')
        plt.show()

        final_states = [game.final_state for game in self.results]
        unique_states = list(set(final_states))
        state_counts = {state: final_states.count(state) for state in unique_states}

        plt.bar(state_counts.keys(), state_counts.values(), edgecolor='black')
        plt.title(f"{self.name}: Final States")
        plt.xlabel('Final State')
        plt.ylabel('Frequency')
        plt.xticks(rotation=45)
        plt.show()

class Experiment2(Experiment):
    def run(self):
        for igame in range(self.num_games):
            game = self.game_class(max_turns=100, winning_points=1, strategy=CHEAPEST_STRATEGY)
            game.play_game(interactive=False)
            print(f"Finished game {igame}")
            self.results.append(copy.copy(game))

def main():
    experiment = Experiment("Experiment", Game, 1000)  # Replace GameClass with the actual game class name
    experiment.run()
    print(experiment.get_results())
    experiment.analyze_results()

if __name__ == "__main__":
    main()