# File: connect4.py
# Date: December 18, 2023
# Description: Creates a standard Connect 4 game board

import numpy as np
from game import Game, State

class Connect4(Game):
    def __init__(self):
        """ Creates a standard Connect 4 board with six rows and seven columns.
        """
        self.rows = 6
        self.columns = 7 

    def initial_state(self):
        """ Creates the initial state for this board.
        """
        board = np.zeros((6, 7), dtype=int)
        return Connect4.State(board, 1)

    class State(State):
        def __init__(self, board, turn):
            self.board = board
            self.actor1 = turn

        def is_terminal(self):
            """ Checks if a given state is terminal. A state is terminal if
            either player has won (there are four consecutive same-player discs
            on the game board), or if there are no more available moves.
            """
            x = self.payoff()
            if x != 0:
                return (True, x)
            elif self.get_actions() == []:
                return (True, 0)
            else:
                return (False, 0)


        def payoff(self):
            """ Checks if a player has gotten four in a row at the given state.
            The payoff for Player 1 winning is 1, for Player 2 winning is -1,
            and for no win is 0.
            """
            # Check rows
            for row in self.board:
                for i in range(len(row) - 3):
                    if row[i] == row[i + 1] == row[i + 2] == row[i + 3] and row[i] != 0:
                        #print(row, self.board)
                        return 1 if row[i] == 1 else -1

            # Check columns
            for col in range(self.board.shape[1]):
                for i in range(self.board.shape[0] - 3):
                    if self.board[i, col] == self.board[i + 1, col] == self.board[i + 2, col] ==self.board[i + 3, col] and self.board[i, col] != 0:
                        #print(row, self.board)
                        return 1 if self.board[i, col] == 1 else -1

            # Check diagonals (positive slope)
            for i in range(self.board.shape[0] - 3):
                for j in range(self.board.shape[1] - 3):
                    if self.board[i, j] == self.board[i + 1, j + 1] == self.board[i + 2, j + 2] == self.board[i + 3, j + 3] and self.board[i, j] != 0:
                        #print(row, self.board)
                        return 1 if self.board[i, j] == 1 else -1

            # Check diagonals (negative slope)
            for i in range(3, self.board.shape[0]):
                for j in range(self.board.shape[1] - 3):
                    if self.board[i, j] == self.board[i - 1, j + 1] == self.board[i - 2, j + 2] == self.board[i - 3, j + 3] and self.board[i, j] != 0:
                        #print(row, self.board)
                        return 1 if self.board[i, j] == 1 else -1

            # If no winner is found
            return 0
            

        def actor(self):
            return self.actor1


        def get_actions(self):
            """ Returns a list of legal moves from the current state.
                The list of moves is given as a list of columns in which to
                drop a disc. Columns are indexed from left to right.
            """
            actions = []
            for i in range(7):
                if self.is_legal(i):
                    actions.append(i)
            return actions

        def is_legal(self, action):
            """ Determines if dropping a disc in the given column is legal
            from this state. An action won't be legal if a column is full.

            action -- index of column
            """
            if self.board[0,action] == 0:
                return True
            else:
                return False

        def successor(self, action): # should only take valid actions
            """ Returns the state that results from dropping a disc in the
            given column. Only handles valid actions.
            
            action -- index of column
            """
            suc = Connect4.State(self.board.copy(), (2 if self.actor1 == 1 else 1))
            for i in range(6):
                if suc.board[(5-i), action] == 0:
                    suc.board[(5-i), action] = self.actor1
                    break
            return suc
        