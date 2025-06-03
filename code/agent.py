from random_agent import RandomAgent
from heuristic_agent import HeuristicAgent
from MCTS_agent import MCTSAgent
from iterative_agent import IterativeAgent

def retrieve_agent(agent_type: str, agent_id: int, **kwargs):
    agent_type = agent_type.lower()
    
    if agent_type == "random":
        return RandomAgent(agent_id)

    elif agent_type == "heuristic":
        return HeuristicAgent(
            agent_id,
            time_limit=kwargs.get("time_limit", 2.0),
            max_depth=kwargs.get("max_depth", 2),
            weight_mobility=kwargs.get("weight_mobility", 0.4),
            weight_territory=kwargs.get("weight_territory", 0.4)
        )

    elif agent_type == "mcts":
        return MCTSAgent(
            agent_id,
            time_limit=kwargs.get("time_limit", 2.0),
        )

    elif agent_type == "iterative":
        return IterativeAgent(
            agent_id,
            time_limit=kwargs.get("time_limit", 2.0),
            max_depth=kwargs.get("max_depth", 4)
        )
    
    else:
        raise ValueError(f"Unknown agent type: {agent_type}")
