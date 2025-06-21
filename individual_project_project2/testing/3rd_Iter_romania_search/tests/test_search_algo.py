import pytest
from SimpleProblemSolvingAgent import SimpleProblemSolvingAgent


@pytest.fixture
# Provide a fresh SPSA agent instance for each test
def agent():
    return SimpleProblemSolvingAgent()


def test_greedy_best_first_search(agent):
    path, cost = agent.greedy_best_first_search("Arad", "Bucharest")
    assert path[0] == "Arad"
    assert path[-1] == "Bucharest"
    assert cost == agent.calculate_path_cost(path)


def test_astar_search(agent):
    path, cost = agent.astar_search("Arad", "Bucharest")
    assert path[0] == "Arad"
    assert path[-1] == "Bucharest"
    assert cost == agent.calculate_path_cost(path)


def test_hill_climbing(agent):
    path, cost = agent.hill_climbing("Arad", "Bucharest")
    assert path[0] == "Arad"
    assert path[-1] == "Bucharest"
    assert cost == agent.calculate_path_cost(path)


def test_simulated_annealing(agent):
    path, cost = agent.simulated_annealing("Arad", "Bucharest")
    assert path[0] == "Arad"
    assert path[-1] == "Bucharest"
    assert cost == agent.calculate_path_cost(path)
