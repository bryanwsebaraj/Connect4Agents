# File: alphabeta.py
# Date: December 18, 2023
# Description: Minimax algorithm with alpha-beta pruning

import time
import connect4
import numpy as np

class abTree:
    def __init__(self, rootState, depth):
        self.best_move = self.alphabeta(rootState, depth, float("-inf"), float("inf"), rootState.actor1)

    def heuristic(self, state):
        """ Returns the total score at the given state for the current actor.
        Increases/decreases score marginally to favor states with two or three
        consecutive discs adjacent to empty slots (allows a potential win).

        state -- game state
        """
        def check_line(line):
            score = 0
            actor = state.actor1
            otherActor = 2 if actor==1 else 1
            for i in range(len(line) - 3):
                window = line[i:i+4]
                if np.count_nonzero(window == actor) == 3 and np.count_nonzero(window == 0) == 1:  # Three red pieces with an empty slot
                    score += 0.7
                elif np.count_nonzero(window == actor) == 2 and np.count_nonzero(window == 0) == 2:  # Two red pieces with two empty slots
                    score += 0.4
                elif np.count_nonzero(window == otherActor) == 3 and np.count_nonzero(window == 0) == 1:  # Three black pieces with an empty slot
                    score -= 0.7
                elif np.count_nonzero(window == otherActor) == 2 and np.count_nonzero(window == 0) == 2:  # Two black pieces with two empty slots
                    score -= 0.4
            return score

        # Evaluate the board in all directions
        total_score = 0
        # Check horizontally
        board = state.board
        for row in board:
            total_score += check_line(row)
        # Check vertically
        for col in board.T:
            total_score += check_line(col)
        # Check diagonally (both directions)
        for i in range(3):
            for j in range(4):
                total_score += check_line(board[i:i+4, j:j+4].diagonal())
                total_score += check_line(np.fliplr(board[i:i+4, j:j+4]).diagonal())

        return total_score
    
    def alphabeta(self, state, depth, alpha, beta, cActor): # do not change passed cActor
        """ Returns the payoff for the best move found by minimax with alpha-
        beta pruning for the given state reaching the given depth.

        state -- game state
        depth -- maximum tree depth
        alpha -- maximizer's best value, initialized to neg inf
        beta -- minimizer's best value, initialized to pos inf
        curr_actor - current actor, Player 1 or Player 2
        """
        isTerm, val = state.is_terminal()
        if isTerm == True:
            return (val, 0)
        elif depth == 0:
            return (self.heuristic(state), 0)
        
        reachableStates = []
        stateactions = state.get_actions()
        for action in stateactions:
            reachableStates.append(state.successor(action))

        i = 0
        maxI = 0 
        if state.actor1 == cActor:
            a = float("-inf")
            while alpha < beta and i < len(reachableStates):
                ab, _ = self.alphabeta(reachableStates[i], depth-1, alpha, beta, cActor)
                if ab > a:
                    a = ab
                    maxI = i
                alpha = max(alpha, a)
                i += 1
            return (a, maxI)

        else:
            b = float("inf")
            while alpha < beta and i < len(reachableStates):
                ba, _ = self.alphabeta(reachableStates[i], depth-1, alpha, beta, cActor)
                if ba < b:
                    b = ba
                    maxI = i
                beta = min(beta, b)
                i += 1
            return (b, maxI)



def ab_policy(timeAllowed, cActor, depth):
    """ Takes the allowed CPU time in seconds and returns a function that takes
    a state and returns the move suggested by running minimax with alpha-beta
    pruning for that amount of time to the specified depth.

    time_allowed -- maximum CPU time in seconds
    depth -- maximum tree depth
    """
    def ab(state):
        timeout = time.time() + timeAllowed
        game = connect4.Connect4()
        st = game.State(state.board, state.actor1)
        
        while time.time() < timeout:
            tree = abTree(st, depth)
        return tree.best_move[1]

        
    return ab
