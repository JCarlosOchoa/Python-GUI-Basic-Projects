import math
import random

class Player:
    def __init__(self, letter):
        # letter is x or o
        self.letter = letter

    # we want all players to get their next move
    def get_move(self, game):
        pass

class RandomComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        square = random.choice(game.available_moves())
        return square

class HumanPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)
    
    # have to ensure that the player chooses a valid next move
    def get_move(self, game):
        valid_square = False
        val = None
        while not valid_square:
            square = input(self.letter + "\'s turn. Input move (0-8): ") # x or o player
            # we're going to check that the input value is a valid input by
            # casting to an integer. anything that is not an integer is invalid.
            # if the input spot is not available on the board, also invalid
            try:
                val = int(square)
                if val not in game.available_moves():
                    raise ValueError
                valid_square = True
            except ValueError:
                print ("Invalid square. Try again.")

        return val


class GeniusComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)
    
    def get_move(self, game):
        if len(game.available_moves()) == 9:
            square = random.choice(game.available_moves()) # if computer goes first, randomly choose a square

        else:
            # player will choose a move based on the minimax algorithm
            square = self.minimax(game, self.letter)
        
        # square is the dictionary output for minimax(). we only want the move's position from that dictionary here
        return square['position']

    def minimax(self, state, player):
        # implement minimax to decide optimal move recursively based on decision trees
        # trying to maximize odds of winning while opponent is trying to minimize their odds of losing

        # INPUTS: a game state and the player being simulated
        # OUTPUTS: a dictionary with the best scoring and the position that it corresponds to

        max_player = self.letter # the player's letter a.k.a. yourself
        other_player = "O" if player == "X" else "X" # check to see if player is X, if not then they must be O

        # first, we want to check if the previous move was a winner.
        # BASE CASE:

        if state.current_winner == other_player:
            # we should return position AND scoring because we will need to track scoring for the algorithm
            return {'position': None,
                    'score': 1 * (state.num_empty_squares() + 1) 
                    if other_player == max_player else -1 * (state.num_empty_squares() + 1)
                    }

        elif not state.num_empty_squares(): # if no squares are empty. this means a tie.
            return {'position': None, 'score': 0}

        if player == max_player: # turn player is trying to maximize their winning odds
            best = {'position': None, 'score': -math.inf} # each score should maximize. initializing at -inf to ensure this.
        
        else:

            best = {'position': None, 'score': math.inf} # each score should minimize. initializing at highest possible value.
        
        # RECURSIVE CASE

        # This will create a tree of all possible game moves to make after each move.
        # Once all nodes terminate with a winner or with a tie, algorithm traces back up each minimax call,
        # choosing the best move based on the minimizing/maximizing at each turn.
        for possible_move in state.available_moves():
            # step 1: make a move to try that spot
            state.make_move(possible_move, player)

            # step 2: recurse using minimax to simulate a game after making that move
            sim_score = self.minimax(state, other_player) # this is where players are alternated in the sim
            # note that sim_score is a dictionary

            # step 3: undo the move
            state.board[possible_move] = " "

            state.current_winner = None
            sim_score['position'] = possible_move # otherwise this will get messy during recursion

            # step 4: update the dictionaries if necessary
            if player == max_player: # maximizing max player
                if sim_score['score'] > best['score']:
                    best = sim_score
                
            else: # minimizing min player 
                if sim_score['score'] < best['score']:
                    best = sim_score

        return best