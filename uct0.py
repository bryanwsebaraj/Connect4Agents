# File: uct0.py
# Date: December 18, 2023
# Description: Monte Carlo Search Tree with UCT0

import time
import random
import math
import connect4

class uct0Node:
    def __init__(self, parent, state):
        self.state = state
        self.parent = parent
        self.visits = 0
        self.reward = 0
        self.children = dict()
        self.expandable = True if state.is_terminal()[0] == False else False

class uct0Tree:
    def __init__(self, root):
        sp = self.traverse2(root) 
        payoff = self.simulate(sp)
        self.update(sp, payoff)

    def ucb(self, parent):
        """ Returns the child of the parent node with the maximum UCB value.
        If there are multiple children sharing the maximum value, one of them
        is randomly selected to be returned.

        parent -- parent node
        """
        ucb, maxUCB, minUCB = 0, float('-inf'), float('inf')
        returnChild = []
        # if p1
        if parent.state.actor() == 1:
            for child in parent.children.values():
                ucb = (child.reward/child.visits) + math.sqrt(2 * math.log(parent.visits) / child.visits)
                if ucb > maxUCB:
                    maxUCB = ucb
                    returnChild = [child]
                elif ucb == maxUCB:
                    returnChild.append(child)
        # if p2
        else:
            for child in parent.children.values():
                ucb = (child.reward/child.visits) - math.sqrt(2 * math.log(parent.visits) / child.visits) 
                if ucb < minUCB:
                    minUCB = ucb
                    returnChild = [child]
                elif ucb == minUCB:
                    returnChild.append(child)
        return random.choice(returnChild) # returns child of passed parent node

    def traverse2(self, root):
        """ Traverses the tree, expanding nodes based on the actions available
        from that node. Returns a child from expansion or a terminal.
        """
        s = root
        while s.state.is_terminal()[0] == False:
            if s.expandable == False:
                s = self.ucb(s)
            elif s.expandable == True:
                s_actions = s.state.get_actions()
                action = random.choice(list(set(s_actions) - set(s.children.keys())))
                sp = uct0Node(s,s.state.successor(action))
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

def uct0_policy(timeAllowed, cActor):
    """ Takes the allowed CPU time in seconds and returns a function that takes
    a position and returns the move suggested by running MCTS for that amount
    of time starting with that position.

    timeAllowed -- allowed CPU time in seconds
    """
    def uct0(state):
        timeout = time.time() + timeAllowed
        game = connect4.Connect4()
        st = game.State(state.board, state.actor1)
        root = uct0Node(None, st)
        
        while time.time() < timeout:
            uct0Tree(root)

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
        
    return uct0
