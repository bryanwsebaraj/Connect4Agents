# CPSC 474 Final Project
# Date: December 18, 2023
# Description: We're using MCTS (UCT0, UCT1, UCT2) and Minimax with alpha-beta
# pruning to play Connect 4. All agents may be compared individually to each other. 
# To compare all agents against pure MCTS at various times, use the command: ./Connect4 
# all number_of_games e.g. ./Connect4 all 1000 displays the results for all agents over 1000 games.
# For more details, run ./Connect 4

import sys
import numpy as np
import time
import uct0
import uct1
import uct2
import mcts
import alphabeta
import connect4

def compare_policies(p1_policy_fxn, p2_policy_fxn, time_limit, num_games):
    p1_wins, p2_wins, ties, p1_time, p2_time = 0, 0, 0, 0, 0
    game = connect4.Connect4()
    p1WinMoves, p2WinMoves = 0, 0

    for _ in range(num_games):
        p1_policy, p2_policy = p1_policy_fxn(), p2_policy_fxn()
        pos = game.initial_state()
        moveCounterP1, moveCounterP2 = 0, 0

        while not pos.is_terminal()[0]:
            move = None
            if pos.actor() == 1:
                # comment out why I have try block
                '''
                start = time.time()
                move = p1_policy(pos)
                p1_time = max(p1_time, time.time() - start)
                moveCounterP1 += 1
                '''
                while move == None:
                    try:
                        start = time.time()
                        move = p1_policy(pos)
                        p1_time = max(p1_time, time.time() - start)
                    except:
                        pass
                moveCounterP1 += 1
                
                
            else:
                while move == None:
                    try:
                        start = time.time()
                        move = p2_policy(pos)
                        p2_time = max(p2_time, time.time() - start)
                    except:
                        pass
                moveCounterP2 += 1
            pos = pos.successor(move)
            #print(pos.board)

        if pos.payoff() == 0: # if tie is reached aka board is full
            ties += 1
        if pos.actor() == 2: # if someone won and state is terminal, actor of current position is the loser
            p1WinMoves += moveCounterP1
            p1_wins += 1
        else:
            p2WinMoves += moveCounterP2
            p2_wins += 1
    '''
    if p1_time > time_limit * 1.01:
        print("WARNING: max time for P1 =", p1_time)
    if p2_time > time_limit * 1.01:
        print("WARNING: max time for P2 =", p2_time)
    '''

    return p1_wins/num_games, p2_wins/num_games, ties/num_games, (p1WinMoves/p1_wins if p1_wins != 0 else 0), (p2WinMoves/p2_wins if p2_wins != 0 else 0)


def test_connect_4(p1_agent_name, p1_policy_fxn, p2_agent_name, p2_policy_fxn, time_limit, num_games):
    p1_win_prob, p2_win_prob, tie_prob, avg_moves_p1, avg_moves_p2 = compare_policies(p1_policy_fxn, p2_policy_fxn, time_limit, num_games)
    print(p1_agent_name.upper(), "(P1) - WINS: ", p1_win_prob, "; AVG MOVES TO WIN: ", round(avg_moves_p1, 4))
    print(p2_agent_name.upper(), "(P2) - WINS: ", p2_win_prob, "; AVG MOVES TO WIN: ", round(avg_moves_p2, 4))
    print("TIES: ", tie_prob)

if __name__ == '__main__':
    validAgents = ['mcts','uct0','uct1','uct2','alphabeta']
    if len(sys.argv) == 3 and sys.argv[1] == 'test' and int(sys.argv[2]) > 0:
        times = [0.0001, 0.0002, 0.0003, 0.0008]
        numgames = int(sys.argv[2])
        print("We are using a multitude of agents, each running uct0, uct1, uct2, or minimax with alpha-beta pruning, to play Connect4 against an MCTS agent. Here are various statistics demonstrating their performance.")
        print("It should take a few minutes to complete, so feel free to scroll tiktok while you wait.")
        print("When t=", times[0], " and n=", numgames,":")
        test_connect_4(validAgents[1], lambda: uct0.uct0_policy(times[0], 1), validAgents[0], lambda: mcts.mcts_policy(times[0], 2), times[0], numgames)
        print("\n")
        test_connect_4(validAgents[0], lambda: mcts.mcts_policy(times[0], 1), validAgents[1], lambda: uct0.uct0_policy(times[0], 2), times[0], numgames)
        print("\n")
        test_connect_4(validAgents[2], lambda: uct1.uct1_policy(times[0], 1), validAgents[0], lambda: mcts.mcts_policy(times[0], 2), times[0], numgames)
        print("\n")
        test_connect_4(validAgents[0], lambda: mcts.mcts_policy(times[0], 1), validAgents[2], lambda: uct1.uct1_policy(times[0], 2), times[0], numgames)
        print("\n")
        test_connect_4(validAgents[3], lambda: uct2.uct2_policy(times[0], 1), validAgents[0], lambda: mcts.mcts_policy(times[0], 2), times[0], numgames)
        print("\n")
        test_connect_4(validAgents[0], lambda: mcts.mcts_policy(times[0], 1), validAgents[3], lambda: uct2.uct2_policy(times[0], 2), times[0], numgames)
        print("\n\n")
        print("When t=", times[1], " and n=", numgames,":")
        test_connect_4(validAgents[1], lambda: uct0.uct0_policy(times[1], 1), validAgents[0], lambda: mcts.mcts_policy(times[1], 2), times[1], numgames)
        print("\n")
        test_connect_4(validAgents[0], lambda: mcts.mcts_policy(times[1], 1), validAgents[1], lambda: uct0.uct0_policy(times[1], 2), times[1], numgames)
        print("\n")
        test_connect_4(validAgents[2], lambda: uct1.uct1_policy(times[1], 1), validAgents[0], lambda: mcts.mcts_policy(times[1], 2), times[1], numgames)
        print("\n")
        test_connect_4(validAgents[0], lambda: mcts.mcts_policy(times[1], 1), validAgents[2], lambda: uct1.uct1_policy(times[1], 2), times[1], numgames)
        print("\n")
        test_connect_4(validAgents[3], lambda: uct2.uct2_policy(times[1], 1), validAgents[0], lambda: mcts.mcts_policy(times[1], 2), times[1], numgames)
        print("\n")
        test_connect_4(validAgents[0], lambda: mcts.mcts_policy(times[1], 1), validAgents[3], lambda: uct2.uct2_policy(times[1], 2), times[1], numgames)
        print("\n\n")
        print("When t=", times[2], " and n=", numgames,":")
        test_connect_4(validAgents[1], lambda: uct0.uct0_policy(times[2], 1), validAgents[0], lambda: mcts.mcts_policy(times[2], 2), times[2], numgames)
        print("\n")
        test_connect_4(validAgents[0], lambda: mcts.mcts_policy(times[2], 1), validAgents[1], lambda: uct0.uct0_policy(times[2], 2), times[2], numgames)
        print("\n")
        test_connect_4(validAgents[2], lambda: uct1.uct1_policy(times[2], 1), validAgents[0], lambda: mcts.mcts_policy(times[2], 2), times[2], numgames)
        print("\n")
        test_connect_4(validAgents[0], lambda: mcts.mcts_policy(times[2], 1), validAgents[2], lambda: uct1.uct1_policy(times[2], 2), times[2], numgames)
        print("\n")
        test_connect_4(validAgents[3], lambda: uct2.uct2_policy(times[2], 1), validAgents[0], lambda: mcts.mcts_policy(times[2], 2), times[2], numgames)
        print("\n")
        test_connect_4(validAgents[0], lambda: mcts.mcts_policy(times[2], 1), validAgents[3], lambda: uct2.uct2_policy(times[2], 2), times[2], numgames)
        print("\n\n")
        print("When t=", times[3], " and n=", numgames,":")
        test_connect_4(validAgents[1], lambda: uct0.uct0_policy(times[3], 1), validAgents[0], lambda: mcts.mcts_policy(times[3], 2), times[3], numgames)
        print("\n")
        test_connect_4(validAgents[0], lambda: mcts.mcts_policy(times[3], 1), validAgents[1], lambda: uct0.uct0_policy(times[3], 2), times[3], numgames)
        print("\n")
        test_connect_4(validAgents[2], lambda: uct1.uct1_policy(times[3], 1), validAgents[0], lambda: mcts.mcts_policy(times[3], 2), times[3], numgames)
        print("\n")
        test_connect_4(validAgents[0], lambda: mcts.mcts_policy(times[3], 1), validAgents[2], lambda: uct1.uct1_policy(times[3], 2), times[3], numgames)
        print("\n")
        test_connect_4(validAgents[3], lambda: uct2.uct2_policy(times[3], 1), validAgents[0], lambda: mcts.mcts_policy(times[3], 2), times[3], numgames)
        print("\n")
        test_connect_4(validAgents[0], lambda: mcts.mcts_policy(times[3], 1), validAgents[3], lambda: uct2.uct2_policy(times[3], 2), times[3], numgames)
        print("\n\n")
        print("alphabeta tests:")
        print("when t = 0.0003, d = 2, and n =", int(numgames/10))
        test_connect_4(validAgents[4], lambda: alphabeta.ab_policy(times[0], 1, 2), validAgents[0], lambda: mcts.mcts_policy(times[0], 2), 0.0003, int(numgames/10))
        print("\n")
        test_connect_4(validAgents[0], lambda: mcts.mcts_policy(times[0], 1), validAgents[4], lambda: alphabeta.ab_policy(times[0], 2, 2), 0.0003, int(numgames/10))
        print("\nwhen t = 0.0006, d = 2, and n =", int(numgames/10))
        test_connect_4(validAgents[4], lambda: alphabeta.ab_policy(times[0], 1, 2), validAgents[0], lambda: mcts.mcts_policy(times[0], 2), 0.0006, int(numgames/10))
        print("\n")
        test_connect_4(validAgents[0], lambda: mcts.mcts_policy(times[0], 1), validAgents[4], lambda: alphabeta.ab_policy(times[0], 2, 2), 0.0006, int(numgames/10))
        print("\nwhen t = 0.0003, d = 3, and n =", int(numgames/10))
        test_connect_4(validAgents[4], lambda: alphabeta.ab_policy(times[0], 1, 3), validAgents[0], lambda: mcts.mcts_policy(times[0], 2), 0.0003, int(numgames/10))
        print("\n")
        test_connect_4(validAgents[0], lambda: mcts.mcts_policy(times[0], 1), validAgents[4], lambda: alphabeta.ab_policy(times[0], 2, 3), 0.0003, int(numgames/10))
        print("\nwhen t = 0.0006, d = 3, and n =", int(numgames/10))
        test_connect_4(validAgents[4], lambda: alphabeta.ab_policy(times[0], 1, 3), validAgents[0], lambda: mcts.mcts_policy(times[0], 2), 0.0006, int(numgames/10))
        print("\n")
        test_connect_4(validAgents[0], lambda: mcts.mcts_policy(times[0], 1), validAgents[4], lambda: alphabeta.ab_policy(times[0], 2, 3), 0.0006, int(numgames/10))
        print("\nwhen t = 0.0003, d = 4, and n =", int(numgames/10))
        test_connect_4(validAgents[4], lambda: alphabeta.ab_policy(times[0], 1, 4), validAgents[0], lambda: mcts.mcts_policy(times[0], 2), 0.0003, int(numgames/10))
        print("\n")
        test_connect_4(validAgents[0], lambda: mcts.mcts_policy(times[0], 1), validAgents[4], lambda: alphabeta.ab_policy(times[0], 2, 4), 0.0003, int(numgames/10))
        print("\nwhen t = 0.0006, d = 4, and n =", int(numgames/10))
        test_connect_4(validAgents[4], lambda: alphabeta.ab_policy(times[0], 1, 4), validAgents[0], lambda: mcts.mcts_policy(times[0], 2), 0.0006, int(numgames/10))
        print("\n")
        test_connect_4(validAgents[0], lambda: mcts.mcts_policy(times[0], 1), validAgents[4], lambda: alphabeta.ab_policy(times[0], 2, 4), 0.0006, int(numgames/10))


    elif len(sys.argv) == 6 and float(sys.argv[3]) > 0 and int(sys.argv[4]) > 0 and (sys.argv[1].lower() in validAgents) and (sys.argv[2].lower() in validAgents) and int(sys.argv[5]) > 0:
        # tried storing lambda functions as values in a dictionary to make it more legible but was difficult to return a function for each agent
        a1, a2, t, n, d = sys.argv[1].lower(), sys.argv[2].lower(), float(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
        if a1 == validAgents[0]: # mcts first agent
            if a2 == validAgents[0]:
                test_connect_4(validAgents[0], lambda: mcts.mcts_policy(t, 1), validAgents[0], lambda: mcts.mcts_policy(t, 2),  t, n)
            elif a2 == validAgents[1]:
                test_connect_4(validAgents[0], lambda: mcts.mcts_policy(t, 1), validAgents[1], lambda: uct0.uct0_policy(t, 2),  t, n)
            elif a2 == validAgents[2]:
                test_connect_4(validAgents[0], lambda: mcts.mcts_policy(t, 1), validAgents[2], lambda: uct1.uct1_policy(t, 2),  t, n)
            elif a2 == validAgents[3]:
                test_connect_4(validAgents[0], lambda: mcts.mcts_policy(t, 1), validAgents[3], lambda: uct2.uct2_policy(t, 2),  t, n)
            elif a2 == validAgents[4]:
                test_connect_4(validAgents[0], lambda: mcts.mcts_policy(t, 1), validAgents[4], lambda: alphabeta.ab_policy(t, 2, d),  t, n)
        elif a1 == validAgents[1]: # uct0 first agent
            if a2 == validAgents[0]:
                test_connect_4(validAgents[1], lambda: uct0.uct0_policy(t, 1), validAgents[0], lambda: mcts.mcts_policy(t, 2),  t, n)
            elif a2 == validAgents[1]:
                test_connect_4(validAgents[1], lambda: uct0.uct0_policy(t, 1), validAgents[1], lambda: uct0.uct0_policy(t, 2),  t, n)
            elif a2 == validAgents[2]:
                test_connect_4(validAgents[1], lambda: uct0.uct0_policy(t, 1), validAgents[2], lambda: uct1.uct1_policy(t, 2),  t, n)
            elif a2 == validAgents[3]:
                test_connect_4(validAgents[1], lambda: uct0.uct0_policy(t, 1), validAgents[3], lambda: uct2.uct2_policy(t, 2),  t, n)
            elif a2 == validAgents[4]:
                test_connect_4(validAgents[1], lambda: uct0.uct0_policy(t, 1), validAgents[4], lambda: alphabeta.ab_policy(t, 2, d),  t, n)
        elif a1 == validAgents[2]: # utc1 first agent
            if a2 == validAgents[0]:
                test_connect_4(validAgents[2], lambda: uct1.uct1_policy(t, 1), validAgents[0], lambda: mcts.mcts_policy(t, 2),  t, n)
            elif a2 == validAgents[1]:
                test_connect_4(validAgents[2], lambda: uct1.uct1_policy(t, 1), validAgents[1], lambda: uct0.uct0_policy(t, 2),  t, n)
            elif a2 == validAgents[2]:
                test_connect_4(validAgents[2], lambda: uct1.uct1_policy(t, 1), validAgents[2], lambda: uct1.uct1_policy(t, 2),  t, n)
            elif a2 == validAgents[3]:
                test_connect_4(validAgents[2], lambda: uct1.uct1_policy(t, 1), validAgents[3], lambda: uct2.uct2_policy(t, 2),  t, n)
            elif a2 == validAgents[4]:
                test_connect_4(validAgents[2], lambda: uct1.uct1_policy(t, 1), validAgents[4], lambda: alphabeta.ab_policy(t, 2, d),  t, n)
        elif a1 == validAgents[3]: # uct2 first agent
            if a2 == validAgents[0]:
                test_connect_4(validAgents[3], lambda: uct2.uct2_policy(t, 1), validAgents[0], lambda: mcts.mcts_policy(t, 2),  t, n)
            elif a2 == validAgents[1]:
                test_connect_4(validAgents[3], lambda: uct2.uct2_policy(t, 1), validAgents[1], lambda: uct0.uct0_policy(t, 2),  t, n)
            elif a2 == validAgents[2]:
                test_connect_4(validAgents[3], lambda: uct2.uct2_policy(t, 1), validAgents[2], lambda: uct1.uct1_policy(t, 2),  t, n)
            elif a2 == validAgents[3]:
                test_connect_4(validAgents[3], lambda: uct2.uct2_policy(t, 1), validAgents[3], lambda: uct2.uct2_policy(t, 2),  t, n)
            elif a2 == validAgents[4]:
                test_connect_4(validAgents[3], lambda: uct2.uct2_policy(t, 1), validAgents[4], lambda: alphabeta.ab_policy(t, 2, d),  t, n)
        elif a1 == validAgents[4]: # ab first agent
            if a2 == validAgents[0]:
                test_connect_4(validAgents[4], lambda: alphabeta.ab_policy(t, 1, d), validAgents[0], lambda: mcts.mcts_policy(t, 2),  t, n)
            elif a2 == validAgents[1]:
                test_connect_4(validAgents[4], lambda: alphabeta.ab_policy(t, 1, d), validAgents[1], lambda: uct0.uct0_policy(t, 2),  t, n)
            elif a2 == validAgents[2]:
                test_connect_4(validAgents[4], lambda: alphabeta.ab_policy(t, 1, d), validAgents[2], lambda: uct1.uct1_policy(t, 2),  t, n)
            elif a2 == validAgents[3]:
                test_connect_4(validAgents[4], lambda: alphabeta.ab_policy(t, 1, d), validAgents[3], lambda: uct2.uct2_policy(t, 2),  t, n)
            elif a2 == validAgents[4]:
                test_connect_4(validAgents[4], lambda: alphabeta.ab_policy(t, 1, d), validAgents[4], lambda: alphabeta.ab_policy(t, 2, d),  t, n)

    else: 
        print("To compare all agents against baseline MCTS at various times: \n./Connect4 all number_of_games")
        print("\te.g. ./Connect4 all 1000")
        print("\nTo compare individual agents: \n./Connect4 agent1 agent2 t n d")
        print("\te.g. ./Connect4 uct2 alphabeta 0.0004 1000 4")
        print("\tagents 1/2 - strings corresponding desired agents utilizing the following algorithms: 'mcts', 'uct0', 'uct1', 'uct2', 'alphabeta'")
        print("\tt - double value representing the time in seconds allowed for each tree search. greater than 0. recommended between 0.0002 to 0.001")
        print("\tn - integer value representing the number of games played by agents. greater than 0. recommended between 100 to 1000")
        print("\td - interger value representing max searchable depth for alphabeta, enter arbitrary integer when not comparing alphabeta")
    