import RomaniaCityApp
from RomaniaCityApp import main


def test_interactive_input_validation(monkeypatch, capsys):
    """
    Tests that the CLI reprompts on invalid inputs and exits cleanly.
    Sequence:
      1. Invalid origin ("Boston") → reprompt
      2. Valid origin ("Arad")
      3. Same-as-origin destination ("Arad") → reprompt
      4. Valid destination ("Bucharest")
      5. Exit command ("no")
    """
    # Prepare the input sequence
    inputs = iter(
        [
            "Boston",  # invalid origin
            "Arad",  # valid origin
            "Arad",  # invalid destination (same as origin)
            "Bucharest",  # valid destination
            "no",  # exit loop
        ]
    )

    # Fake input function prints the prompt then returns next value
    def fake_input(prompt=""):
        print(prompt, end="")  # ensure prompt is captured
        return next(inputs)

    # Override built-in input and the agent class
    monkeypatch.setattr("builtins.input", fake_input)
    monkeypatch.setattr(
        RomaniaCityApp,
        "SimpleProblemSolvingAgent",
        lambda: type(
            "A",
            (object,),
            {
                "graph": {"Arad": {}, "Bucharest": {}},
                "greedy_best_first_search": lambda self, s, g: ([s, g], 0),
                "astar_search": lambda self, s, g: ([s, g], 0),
                "hill_climbing": lambda self, s, g: ([s, g], 0),
                "simulated_annealing": lambda self, s, g: ([s, g], 0),
            },
        )(),
    )

    # Run the CLI
    main()

    # Capture printed output
    out = capsys.readouterr().out

    # Assertions
    assert "Could not find Boston" in out
    assert "The same city can't be both origin and destination" in out
    assert "Thank You for Using Our App" in out
