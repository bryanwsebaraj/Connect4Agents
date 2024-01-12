# File: mcts.py
# Date: December 18, 2023
# Description: Pure Monte Carlo Search Tree

import time
import random
import connect4

class mctsNode:
    def __init__(self, parent, state):
        self.state = state
        self.parent = parent
        self.visits = 0
        self.reward = 0
        self.children = dict()
        self.expandable = True if state.is_terminal()[0] == False else False

class mctsTree:
    def __init__(self, root):
        sp = self.traverse2(root) 
        payoff = self.simulate(sp)
        self.update(sp, payoff)

    def traverse2(self, root):
        """ Traverses the tree, expanding nodes based on the actions available
        from that node. Returns a child from expansion or a terminal.
        """
        s = root
        while s.state.is_terminal()[0] == False:
            if s.expandable == False:
                s = random.choice(list(s.children.values()))
            elif s.expandable == True:
                s_actions = s.state.get_actions()
                action = random.choice(list(set(s_actions) - set(s.children.keys())))
                sp = mctsNode(s,s.state.successor(action))
                s.children[action] = sp
                if len(s.children) == len(s_actions):
                    s.expandable = False
                return sp
        return s

    def simulate(self, spNode):
        """ Simulates a random playout to a terminal state from the given node.
        Returns the payoff to the player at the terminal position.
        """
        sp = spNode.state
        while(sp.is_terminal() == False):
            sp = sp.successor(random.choice(sp.get_actions()))
        return sp.payoff()

    def update(self, pNode, payoff):
        """ Back propagates payoff up the tree by updating the total reward and
        number of visits.
        """
        current = pNode
        while current.parent != None:
            current.reward += payoff
            current.visits += 1
            current = current.parent
        current.visits += 1

def mcts_policy(timeAllowed, cActor):
    """ Takes the allowed CPU time in seconds and returns a function that takes
    a position and returns the move suggested by running MCTS for that amount
    of time starting with that position.

    timeAllowed -- allowed CPU time in seconds
    """
    def mcts(state):
        timeout = time.time() + timeAllowed
        game = connect4.Connect4()
        st = game.State(state.board, state.actor1)
        root = mctsNode(None, st)
        while time.time() < timeout:
            mctsTree(root)

        if root.state.actor() == cActor:
            maxReward = float('-inf')
            maxAction = None
            for action in root.children.keys(): 
                child = root.children.get(action)
                exploit = child.reward / child.visits
                if exploit > maxReward:
                    maxReward = exploit
                    maxAction = action
            return maxAction
        else:
            minReward = float('inf')
            minAction = None
            for action in root.children.keys(): 
                child = root.children.get(action)
                exploit = child.reward / child.visits
                if exploit < minReward:
                    minReward = exploit
                    minAction = action
            return minAction
        
    return mcts

