import copy

import matplotlib.pyplot as plt

from Splendor import Game

class Experiment:
    def __init__(self, game_class, num_games):
        self.game_class = game_class
        self.num_games = num_games
        self.results = []

    def run(self):
        for igame in range(self.num_games):
            game = self.game_class(max_turns=100, winning_points=1)
            game.play_game(interactive=False)
            input(f"finished game {igame}")
            self.results.append(copy.copy(game))

    def get_results(self):
        return self.results
    

    def analyze_results(self):
        num_turns = [game.num_turns for game in self.results]
        plt.hist(num_turns, bins=range(min(num_turns), max(num_turns) + 1), edgecolor='black')
        plt.title('Histogram of Number of Turns Played')
        plt.xlabel('Number of Turns')
        plt.ylabel('Frequency')
        plt.show()

def main():
    experiment = Experiment(Game, 10)  # Replace GameClass with the actual game class name
    experiment.run()
    print(experiment.get_results())
    experiment.analyze_results()

if __name__ == "__main__":
    main()