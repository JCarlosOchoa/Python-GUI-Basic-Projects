from player import RandomComputerPlayer, HumanPlayer, GeniusComputerPlayer
import time

class TicTacToe:
    def __init__(self):
        self.board = [" " for _ in range(9)] #the index of this list will represent a 3x3 board
        self.current_winner = None # keep track of winner!

    def print_board(self):
        # the board has indeces 0 - 8. each i would refer to indeces 0-2, 3-5, 6-8, which are the rows of length 3
        for row in [self.board[i*3: (i+1) * 3] for i in range(3)]:
            print ("| " + " | ".join(row) + " |")
    
    @staticmethod # static method bc it does not refer to any specific board, meaning we don't have to pass in self
    def print_board_nums():
        # 0 | 1 | 2, etc -- tells us what number corresponds to which box
        # an array containing arrays. j counts each subarray. i will populate each subarray with the numbers
        number_board = [ [str(i) for i in range(j*3, (j+1)*3)] for j in range(3)]
        for row in number_board:
            print ("| " + " | ".join(row) + " |")
    
    def available_moves(self):
        # list comprehension of below loop
        return [i for (i, spot) in enumerate(self.board) if spot == " "]

        # elongated iteration
        # moves = []
        # for (i, spot) in enumerate(self.board):
        #     # enumerate makes a list of tuples (index, value at index)
        #     # row in board may look like [x, x, o] --> [(0, 'x'), (1, 'x'), (2, 'o')]
        #     if spot = " ":
        #         moves.append(i)
        # return moves

    def game_empty_squares(self):
        # returns Boolean value confirming if game board has empty spaces
        return " " in self.board
    
    def num_empty_squares(self):
        # let's us know how many moves are left in the game, counting the spaces.
        return self.board.count(" ")

    def make_move(self, square, letter):
        # we must know where to place player input (square) and who made the move (letter)
        # if valid move, we will return true
        # if invalid move, return false
        if self.board[square] == " ":
            self.board[square] = letter

            # the winner should be indicated after the winning move is made!
            if self.winner(square, letter):
                self.current_winner = letter

            return True
        return False

    def winner(self, square, letter):
        # we must be able to check if there is a winner!
        # 3 in a row anywhere, so all possiblities must be checked

        # checking 3 in a row horizontally
        row_ind = square // 3
        row = self.board[row_ind*3 : (row_ind + 1) *3]
        if all([spot == letter for spot in row]):
            return True
        
        # checking 3 in a row vertically
        col_ind = square % 3
        column = [self.board[col_ind+i*3] for i in range(3)]
        if all([spot == letter for spot in column]):
            return True
        
        # checking diagonals
        # only check if the square is an even number, since these are the numbers on the diagonals
        if square % 2 == 0:
            diagonal1 = [self.board[i] for i in [0, 4, 8]] #top left to bottom right
            if all([spot == letter for spot in diagonal1]):
                return True
            diagonal2 = [self.board[i] for i in [2, 4, 6]] #top right to bottom left
            if all([spot == letter for spot in diagonal2]):
                return True
        
        # if all the win conditions fail, return false since there is not a winner
        return False

# this function will actually play the game
def play (game, x_player, o_player, print_game=True):
    # Inputs: a Game object, two Player objects, and whether you want to 
    # see the game board output every turn. This may be unnecessary when two computer players
    # are up against each other.
    # Outputs: winner of the game (letter) or "tie" if tied
    if print_game:
        game.print_board_nums()
    
    letter = "X" # starting letter

    # iterate while game stil has empty squares
    # (we don't have to worry about winner because we'll return that, which breaks loop)

    while game.game_empty_squares():
        # add in a small pause so the program looks better
        # time.sleep(0.8)

        # get the move fro m the appropriate player
        if letter == "O":
            square = o_player.get_move(game)
        else:
            square = x_player.get_move(game)
        
        # we defined a function that makes a move!
        if game.make_move(square, letter):
            if print_game:
                print(letter + f" makes a move to square {square}")
                game.print_board()
                print (" ") # empty line for spacing

            if game.current_winner:
                if print_game:
                    print (letter + " wins!")
                return letter
        
            # after making move, must alternate letters for next player
            letter = "O" if letter == "X" else "X"

            # how do we know if we won? we should indicate a winner after the winning move is made.
    
    # if the while loop breaks, then there are no moves left. This is a tie.
    if print_game:
        print ("It\'s a tie!")


# if __name__ == "__main__":
#     x_player = HumanPlayer("X")
#     # o_player = RandomComputerPlayer("O")
#     # o_player = HumanPlayer("O")
#     o_player = GeniusComputerPlayer("O")
#     t = TicTacToe()
#     play(t, x_player, o_player, print_game=True)

# To show the improvement between RandomComputerPlayer and GeniusComputerPlayer, comment out the above if statement
# and uncomment the below

if __name__ == "__main__":
    x_wins = 0
    o_wins = 0
    ties = 0
    for simulations in range(1000): # --> this is the number of simulated games
        x_player = RandomComputerPlayer("X")
        o_player = GeniusComputerPlayer("O")
        t = TicTacToe()
        result = play(t, x_player, o_player, print_game=False)
        if result == "X":
            x_wins += 1
        elif result == "O":
            o_wins += 1
        else:
            ties += 1
    print (f"After 1000 simulations, we see {x_wins} X wins, {o_wins} O wins, and {ties} ties.")