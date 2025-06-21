import pytest
from SimpleProblemSolvingAgent import SimpleProblemSolvingAgent

@pytest.fixture
def agent():
    return SimpleProblemSolvingAgent("Arad", "Bucharest")

@pytest.mark.parametrize("method,expected_cost", [
    ("run_greedy", 450),
    ("run_astar", 418),
    ("run_hill_climbing", 450),
])
def test_search_cost(agent, method, expected_cost):
    result = getattr(agent, method)()
    assert result.path_cost == expected_cost

def test_solution_path(agent):
    for method in ["run_greedy", "run_astar", "run_hill_climbing", "run_simulated_annealing"]:
        result = getattr(agent, method)()
        path = result.solution_path()
        assert isinstance(path, list)
        assert path[0] == "Arad"
        assert path[-1] == "Bucharest"
