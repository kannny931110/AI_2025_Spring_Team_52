from agent import retrieve_agent
from game import Game
import random
from tqdm import trange

def battle(agent1_type: str, agent2_type: str, games: int = 10, size: int = 10, seed: int = None, **agent_kwargs):
    agent_1_wins = 0
    agent_2_wins = 0

    if seed is not None:
        random.seed(seed)

    for i in trange(games, desc="Simulating battles"):
        if random.random() < 0.5:
            first_agent_type, second_agent_type = agent1_type, agent2_type
            is_agent1_first = True
        else:
            first_agent_type, second_agent_type = agent2_type, agent1_type
            is_agent1_first = False

        agent_first = retrieve_agent(first_agent_type, 1, **agent_kwargs)
        agent_second = retrieve_agent(second_agent_type, 2, **agent_kwargs)

        game = Game(agent_first, agent_second)
        winner = game.run(verbose=False, return_winner=True)

        if (winner == 1 and is_agent1_first) or (winner == 2 and not is_agent1_first):
            agent_1_wins += 1
        else:
            agent_2_wins += 1

    print(f"\nSummary after {games} games:")
    print(f"Agent 1 ({agent1_type}) wins: {agent_1_wins}")
    print(f"Agent 2 ({agent2_type}) wins: {agent_2_wins}")

if __name__ == "__main__":
    print("Please uncomment the battle function calls to run the simulations.")
    # Random vs. MCTS
    #battle("random", "mcts", games=50, size=15, max_depth=4, time_limit=1.0)
    #battle("random", "mcts", games=100, size=15, max_depth=4, time_limit=1.0)
    #battle("random", "mcts", games=500, size=15, max_depth=4, time_limit=1.0)

    # Random vs. Iterative
    #battle("random", "iterative", games=50, size=15, max_depth=4, time_limit=1.0)
    #battle("random", "iterative", games=100, size=15, max_depth=4, time_limit=1.0)
    #battle("random", "iterative", games=500, size=15, max_depth=4, time_limit=1.0)

    # Heuristic vs. MCTS
    #battle("heuristic", "mcts", games=50, size=15, max_depth=4, time_limit=1.0)
    #battle("heuristic", "mcts", games=100, size=15, max_depth=4, time_limit=1.0)
    #battle("heuristic", "mcts", games=500, size=15, max_depth=4, time_limit=1.0)

    # Heuristic vs. Iterative
    #battle("heuristic", "iterative", games=50, size=15, max_depth=4, time_limit=1.0)
    #battle("heuristic", "iterative", games=100, size=15, max_depth=4, time_limit=1.0)
    #battle("heuristic", "iterative", games=500, size=15, max_depth=4, time_limit=1.0)
