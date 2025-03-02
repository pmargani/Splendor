import pygame
import sys

from Splendor import Game, Coin

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
CARD_WIDTH = 150
CARD_HEIGHT = 150
PLAYER_CARD_WIDTH = 25
PLAYER_CARD_HEIGHT = 25
COIN_RADIUS = 10
FONT_SIZE = 24

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
COLORS_MAP = {
    "red": RED,
    "blue": BLUE,
    "green": GREEN,
    "white": WHITE,
    "black": BLACK
}

# Initialize Pygame
pygame.init()



# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Splendor Game")

# Font
font = pygame.font.Font(None, FONT_SIZE)

def initPyGame():
    pass
    # game = Game(num_players=3, max_turns=None)
    # game.describe()
    # game.play_game()
    # game.describe()


def draw_text(text, x, y, color=BLACK):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def draw_card(card, x, y):
    pygame.draw.rect(screen, BLACK, (x - 2, y - 2, CARD_WIDTH + 4, CARD_HEIGHT + 4))  # Draw border
    pygame.draw.rect(screen, COLORS_MAP[card.color], (x, y, CARD_WIDTH, CARD_HEIGHT))

    offset = 20

    # Draw white rectangle underneath points and coins
    pygame.draw.rect(screen, WHITE, (x + offset, y + offset, CARD_WIDTH - 2*offset, 90))

    draw_text(f"Points: {card.points}", x + offset, y + offset)
    # draw_text(f"Cost: {card.get_filtered_cost()}", x + 5, y + 30)
    ci = 0

    coin_seperation = COIN_RADIUS * 2
    coin_y_offset = 60
    for color, numCoins in card.get_filtered_cost().items():
        cx = x + offset + (ci * coin_seperation)
        draw_coin(color, cx, y + 5 + coin_y_offset)
        draw_text(str(numCoins), cx, y + offset + coin_y_offset + COIN_RADIUS)
        ci += 1

def draw_coin(color, x, y):   
    pygame.draw.circle(screen, BLACK, (x, y), COIN_RADIUS + 2)  # Draw border
    pygame.draw.circle(screen, COLORS_MAP[color], (x, y), COIN_RADIUS)
    # draw_text(coin.color, x - COIN_RADIUS, y + COIN_RADIUS + 5)

def draw_player_card(color, card_count, x, y):
    pygame.draw.rect(screen, BLACK, (x - 2, y - 2, PLAYER_CARD_WIDTH + 4, PLAYER_CARD_HEIGHT + 4))  # Draw border
    pygame.draw.rect(screen, COLORS_MAP[color], (x, y, PLAYER_CARD_WIDTH, PLAYER_CARD_HEIGHT))
    text_color = BLACK if color == "white" else WHITE
    draw_text(str(card_count), x + PLAYER_CARD_WIDTH // 2, y + PLAYER_CARD_HEIGHT // 2, color=text_color)
        
def draw_player(player, x, y):
    pygame.draw.rect(screen, BLACK, (x - 2, y - 2, SCREEN_WIDTH // 4 + 4, 204))  # Draw border
    pygame.draw.rect(screen, WHITE, (x, y, SCREEN_WIDTH // 4, 200))
    draw_text(player.name, x, y)
    draw_text(f"Points: {player.get_total_points()}", x, y + 30)
    
    # Draw player's coins
    for i, (color, count) in enumerate(player.get_coins_dict().items()):
        draw_coin(color, x + i * (COIN_RADIUS * 2 + 10), y + 60) # + j * (COIN_RADIUS * 2 + 10))
        draw_text(str(count), x + i * (COIN_RADIUS * 2 + 10), y + 80)
        # print(f"coin {i}: {(color, count)}")
        # for j in range(count):
            # draw_coin(type('Coin', (object,), {'color': color}), x + i * (COIN_RADIUS * 2 + 10), y + 60 + j * (COIN_RADIUS * 2 + 10))
            # draw_coin(color, x + i * (COIN_RADIUS * 2 + 10), y + 60 + j * (COIN_RADIUS * 2 + 10))
    
    # Draw player's cards
    cnt = 0
    for i, (color, count) in enumerate(player.get_cards_dict().items()):
        if count > 0:
            draw_player_card(color, count, x + (cnt * PLAYER_CARD_WIDTH), y+120)
            cnt += 1
        # for j in range(count):
            # draw_player_card(type('Card', (object,), {'color': color, 'points': 0, 'get_filtered_cost': lambda: ''}), x + i * (CARD_WIDTH + 10), y + 120 + j * (CARD_HEIGHT + 10))

def draw_player_old(player, x, y):
    draw_text(player.name, x, y)
    draw_text(f"Points: {player.get_total_points()}", x, y + 30)
    draw_text(f"Coins: {player.get_coins_dict()}", x, y + 60)
    draw_text(f"Cards: {player.get_cards_dict()}", x, y + 90)

def playSplendorPyGame():
    game = Game(num_players=4, max_turns=None, winning_points=1)

    print(f"Players: {game.players}")
    initPyGame()

    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(WHITE)

        # Draw turn and active player
        draw_text(f"Turn: {game.turn}", 10, 10)
        draw_text(f"Num Turns: {game.num_turns}", 10, 40)
        draw_text(f"Current Player: {game.current_player.name}", 10, 70)

        # Draw "Take Turn" button
        button_rect = pygame.Rect(10, 100, 100, 40)
        pygame.draw.rect(screen, BLUE, button_rect)
        draw_text("Take Turn", 20, 110, WHITE)

        # Draw number of cards left
        draw_text(f"Cards Left: {sum(len(cards) for cards in game.cards)}", 10, 150)

        # Check if the game is over
        if game.is_game_over():
            draw_text("Game Over", 10, 180)
            winner = game.get_winner()
            if winner:
                draw_text(f"Winner: {winner.name}", 10, 210)
    
        # Draw players at the bottom in a horizontal line
        for i, player in enumerate(game.players):
            draw_player(player, 10 + i * 200, SCREEN_HEIGHT - 200)



        # Draw coins in the middle of the screen
        for i, (color, coins) in enumerate(game.coins.items()):
            draw_coin(color, SCREEN_WIDTH // 2 + i * (COIN_RADIUS * 2 + 10), SCREEN_HEIGHT // 2)
            draw_text(str(len(coins)), SCREEN_WIDTH // 2 + i * (COIN_RADIUS * 2 + 10) - 10, SCREEN_HEIGHT // 2 + COIN_RADIUS + 5)


        # Draw visible cards
        for level, cards in enumerate(game.cards):
            for j, card in enumerate(cards[:game.num_cards_visible]):
                draw_card(card, 300 + j * (CARD_WIDTH + 10), 10 + level * (CARD_HEIGHT + 10))


        # Check for button click
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos) and can_take_turn and not game_over:
                game.take_turn()
                game.next_turn()
                game.describe()
                can_take_turn = False
                if not game.validate_game_state():
                    print("Game state is invalid.")
                    return
                if game.is_game_over():
                    print("Game Over")
                    game_over = True
        else:
            can_take_turn = True        

        pygame.display.flip()

def main():
    playSplendorPyGame()

if __name__ == "__main__":
    main()