import unittest
from search_algorithms import greedy_best_first_search, a_star_search, hill_climbing, simulated_annealing

class TestRomaniaSearchAlgorithms(unittest.TestCase):
    def test_greedy_best_first(self):
        path = greedy_best_first_search("Arad", "Bucharest")
        self.assertIn("Bucharest", path)
        self.assertEqual(path[0], "Arad")

    def test_a_star(self):
        path = a_star_search("Arad", "Bucharest")
        self.assertIn("Bucharest", path)
        self.assertEqual(path[0], "Arad")

    def test_hill_climbing(self):
        path = hill_climbing("Arad", "Bucharest")
        self.assertTrue(path is None or path[0] == "Arad")

    def test_simulated_annealing(self):
        path = simulated_annealing("Arad", "Bucharest")
        self.assertTrue(isinstance(path, list) or path is None)

if __name__ == '__main__':
    unittest.main()
