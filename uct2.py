# File: uct2.py
# Date: December 18, 2023
# Description: Monte Carlo Search Tree with UCT2

import time
import random
import math
import connect4

class uct2implicit:
    def __init__(self, rootState):
        self.stateList = dict()
        self.stateList[rootState] = [[], 0, True if rootState.is_terminal()[0] == False else False, 0] 
        # array of visit count for each possible action, own visit count, expandable flag, state reward
        self.run(rootState)

    def ucb(self, parentState):
        """ Returns the child of the parent node with the maximum UCB value.
        If there are multiple children sharing the maximum value, one of them
        is randomly selected to be returned.

        parentState -- parent state
        """
        ucb, maxUCB, minUCB = 0, float('-inf'), float('inf')
        childIndexList = []
        childVisitList = self.stateList[parentState][0]
        actions = parentState.get_actions()
        if parentState.actor() == 1:
            for i in range(len(childVisitList)):
                ucb = ((self.stateList[parentState.successor(actions[i])][3])/childVisitList[i]) + math.sqrt(2 * math.log(self.stateList[parentState][3]) / childVisitList[i])
                if ucb > maxUCB:
                    maxUCB = ucb
                    childIndexList = [i]
                elif ucb == maxUCB:
                    childIndexList.append(i)
        else:
            for i in range(len(childVisitList)):
                ucb = ((self.stateList[parentState.successor(actions[i])][3])/childVisitList[i]) + math.sqrt(2 * math.log(self.stateList[parentState][3]) / childVisitList[i])
                if ucb < minUCB:
                    minUCB = ucb
                    childIndexList = [i]
                elif ucb == minUCB:
                    childIndexList.append(i)
        return random.choice(childIndexList)
    
    def run(self, state):
        """ Returns the payoff resulting from running MCTS with UCT2 from the
        given state.
        """
        if state.is_terminal()[0] == False and self.stateList[state][2] == False:
            index = self.ucb(state)
            newState = state.successor(state.get_actions()[index])
            reward = self.run(newState)
            stateVals = self.stateList[state]
            stateVals[3] += reward
            stateVals[0][index] += 1
            stateVals[1] += 1
            self.stateList[state] = stateVals
            return reward
        elif state.is_terminal()[0] == False:
            s_actions = state.get_actions()
            action = s_actions[len(self.stateList[state][0])] # is an index
            sp = state.successor(action)
            if self.stateList.get(sp) != None:
                reward = self.run(sp)
                stateVals = self.stateList[state]
                stateVals[1] += 1
                stateVals[0].append(1)
                stateVals[3] += reward
                if len(stateVals[0]) == len(s_actions):
                        stateVals[2] = False
                self.stateList[state] = stateVals
                return reward
            else:
                reward = self.simulate(sp)
                self.stateList[sp] = [[], 1, True if sp.is_terminal()[0] == False else False] 
                stateVals = self.stateList[state]
                stateVals[1] += 1
                stateVals[0].append(1)
                stateVals[3] += reward
                if len(stateVals[0]) == len(s_actions):
                        stateVals[2] = False
                self.stateList[state] = stateVals
                return reward
        else:
            return state.payoff()

        
    def simulate(self, state):
        """ Simulates a random playout to a terminal state from the given node.
        Returns the payoff to the player at the terminal position.
        """
        s = state
        while s.is_terminal()[0] == False:
            s = s.successor(random.choice(s.get_actions()))
        return s.payoff()
        

def uct2_policy(timeAllowed, cActor):
    """ Takes the allowed CPU time in seconds and returns a function that takes
    a position and returns the move suggested by running MCTS for that amount
    of time starting with that position.

    timeAllowed -- allowed CPU time in seconds
    """
    def uct2(state):
        timeout = time.time() + timeAllowed
        game = connect4.Connect4()
        st = game.State(state.board, state.actor1)

        while time.time() < timeout:
            imptree = uct2implicit(st)

        actions = st.get_actions()
        if st.actor() == cActor:
            maxReward = float('-inf')
            maxAction = 0
            rootVals = imptree.stateList[st][0]
            for i in range(len(rootVals)): 
                exp = imptree.stateList.get(st.successor(actions[i]))
                if exp != None:
                    exploit = exp[3] / rootVals[i]
                    if exploit > maxReward:
                        maxReward = exploit
                        maxAction = i
            return actions[maxAction]
        else:
            minReward = float('inf')
            minAction = None
            rootVals = imptree.stateList[st][0]
            for i in range(len(rootVals)):
                exp = imptree.stateList.get(st.successor(actions[i]))
                if exp != None:
                    exploit = exp[3] / rootVals[i]
                    if exploit < minReward:
                        minReward = exploit
                        minAction = i
            return actions[minAction]
        
    return uct2
