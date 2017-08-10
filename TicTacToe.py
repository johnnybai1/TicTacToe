# Minimax will pick a move that maximizes the move of the computer
# TODO: modify minimax to determine the best move for either "X" or "O"
# Easy to implement, instead of defining "X" win as +1 and "O" win as -1,
# associate +1 to a state that is a win for the player who is currently moving
# TODO: Figure out the minimax values for each game state (board configuration)
import random

# Returns a tuple [minimax value, best move] that can be made
def minimax(state):
    choices = []
    # Initialize best to -2 since we are maximizing and values can be either 1, 0, or -1
    best = -2
    for pos in state.valid_moves():
        next_state = state.move(pos)
        value = min_value(next_state)
        if value > best:
            best = value
            choices = [pos]
        if value == best:
            choices.append(pos)
    return [best, random.choice(choices)]

def max_value(state):
    # Is the game over?
    status = state.game_over()
    if status is not None:
        return status
    # Maximize, therefore start with -2
    v = -2
    for pos in state.valid_moves():
        next_state = state.move(pos)
        v = max(v, min_value(next_state))
    return v

def min_value(state):
    # Is the game over?
    status = state.game_over()
    if status is not None:
        return status
    # Minimize, therefore start with 2
    v = 2
    for pos in state.valid_moves():
        next_state = state.move(pos)
        v = min(v, max_value(next_state))
    return v

# Class to represent our game states
# Simple implementation of an Tic Tac Toe game that has a perfect computer player
# The game is played on a 1D array representation of the board
# [0][1][2]
# [3][4][5]
# [6][7][8]
# The player is always O and the computer is always X
class State:
    CROSS = 1
    CIRCLE = -1
    EMPTY = 0

    # Winning combinations
    goals = (
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6])

    def __init__(self, current_player=CROSS, board=[EMPTY] * 9):
        self.current_player = current_player
        self.board = board

    # Returns a list of indices for where the board is empty
    def valid_moves(self):
        return [i for i, v in enumerate(self.board) if v == 0]

    # Returns a list of indices where the player has a mark
    def get_player_tiles(self, player):
        return [i for i, v in enumerate(self.board) if v == player]

    # Returns a new State representing the game after the move has been made
    def move(self, pos):
        board = self.board[:]
        board[pos] = self.current_player
        # Return a State representing the new board and changing turns
        return State(-self.current_player, board)

    # Returns +1 for CROSS winner, -1 for CIRCLE winner, or None for no winner
    def winner(self):
        # Check if each player won
        for player in (self.CROSS, self.CIRCLE):
            # Get the player's tiles
            tiles = self.get_player_tiles(player)
            for goal in self.goals:
                # Check every winning config
                hasWon = True
                for pos in goal:
                    if pos not in tiles:
                        # If a position in the winning config is not present in the player's
                        # list of tiles, not a win by this winning config
                        hasWon = False
                if hasWon:
                    return player
        # None indicates no winner, not necessarily a draw
        return None

    # Returns the winner if there is a winner, 0 if there is a draw, or None if the game is not over
    def game_over(self):
        winner = self.winner()
        if winner is not None:
            return winner
        if len(self.valid_moves()) == 0:
            return 0
        return None

    def symbol(self, pos):
        if self.board[pos] == -1:
            return 'O'
        if self.board[pos] == 1:
            return 'X'
        else:
            return pos

    def display(self):
        print("|-----|")
        print("|%s|%s|%s|" % (self.symbol(0), self.symbol(1), self.symbol(2)))
        print("|-----|")
        print("|%s|%s|%s|" % (self.symbol(3), self.symbol(4), self.symbol(5)))
        print("|-----|")
        print("|%s|%s|%s|" % (self.symbol(6), self.symbol(7), self.symbol(8)))
        print("|-----|")

# TODO: add check to make sure player inputs a valid move (empty tile)
# Easy to implement, add a while loop to keep asking for input until player
# inputs a valid tile
if __name__ == "__main__":
    game = int(input("Game starting, who goes first? '1' for you, '2' for Computer: "))
    if game == 1:
        print("You start first!")
        game = State(State.CIRCLE)
        game.display()
        while True:
            player = int(input("Choose move: "))
            game = game.move(player)
            game.display()
            status = game.game_over()
            if status is not None:
                break
            print("Computer's turn...")
            computer = minimax(game)
            game = game.move(computer[1])
            game.display()
            print("The minimax of this board is %i" %computer[0])
            print("Computer moved to: %i" %computer[1])
            status = game.game_over()
            if status is not None:
                break
    else:
        print("Computer starts first!")
        game = State()
        while True:
            print("Computer's turn...")
            computer = minimax(game)
            game = game.move(computer[1])
            game.display()
            print("The minimax of this board is %i" %computer[0])
            print("Computer moved to: %i" %computer[1])
            status = game.game_over()
            if status is not None:
                break
            player = int(input("Choose move: "))
            game = game.move(player)
            game.display()
            status = game.game_over()
            if status is not None:
                break
    if status == 1:
        print("Winner is X")
    elif status == -1:
        print("Winner is O")
    else:
        print("Draw!")
