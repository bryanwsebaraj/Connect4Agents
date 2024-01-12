# Connect 4 Agents

Play agents against each other in Connect 4, with each agent employing either mcts, uct0, uct1, uct2, or minimax with alpha-beta pruning to choose an optimal move. 

## Testing

- Build the executable script
    - 'make Connect4'

- To compare all agents against each other
    - './Connect4 test n' 
    - n represents the number of games (integer) each comparison is played. Recommend between 100 and 1000

- To compare individual agents
     - './Connect4 agent1 agent2 t n d' 
     - agent1/agent2 can be either 'mcts', 'uct0', 'uct1', 'uct2', or 'alphabeta'
     - t represents the time (double) each position has to search its game tree (recommended between 0.0002 to 0.001)
     - n represents the number of games (integer) each comparison is played
     - d represents the max searchable depth (integer) before alpha-beta relies on its simple heuristic. 