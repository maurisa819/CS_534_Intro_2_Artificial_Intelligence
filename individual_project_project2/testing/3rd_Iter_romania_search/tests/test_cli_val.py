import RomaniaCityApp
from RomaniaCityApp import main


class StubAgent:
    """Stub agent that returns a trivial path for any search method and minimal graph for validation."""

    def __init__(self):
        # Provide minimal graph keys for input validation
        self.graph = {"Arad": {}, "Bucharest": {}}

    def greedy_best_first_search(self, start, goal):
        return [start, goal], 0

    def astar_search(self, start, goal):
        return [start, goal], 0

    def hill_climbing(self, start, goal):
        return [start, goal], 0

    def simulated_annealing(self, start, goal):
        return [start, goal], 0


def test_interactive_input_validation(monkeypatch, capsys):
    # Sequence: invalid origin, valid origin; same-as-origin dest, valid dest; exit
    inputs = iter(
        [
            "Boston",  # invalid origin
            "Arad",  # valid origin
            "Arad",  # invalid dest (same as origin)
            "Bucharest",  # valid dest
            "no",  # exit loop
        ]
    )

    # Define a fake input that prints the prompt before returning the next test value
    def fake_input(prompt=""):
        print(prompt, end="")  # ensure the prompt is written to stdout
        return next(inputs)

    # Monkey-patch built-in input
    monkeypatch.setattr("builtins.input", fake_input)
    # Monkey-patch the agent class used in the app to our stub
    monkeypatch.setattr(RomaniaCityApp, "SimpleProblemSolvingAgent", StubAgent)

    # Run the application entry point
    main()

    # Capture printed output
    captured = capsys.readouterr()
    out = captured.out

    # Verify that invalid origin was reprompted
    assert "Could not find Boston" in out
    # Verify that same-city destination was reprompted
    assert "The same city can't be both origin and destination" in out
    # Verify that the app thanked the user at the end
    assert "Thank You for Using Our App" in out
