import unittest

__author__ = 'tchajed'

import puzzle
import search


class AstarNodesTest(unittest.TestCase):
    def test_priority_ordering(self):
        nodes = search.AstarNodes()
        self.assertTrue(nodes.isEmpty())
        nodes.add(search.SearchNode(None, "a", 2, 0), 1)
        nodes.add(search.SearchNode(None, "b", 1, 0), 1)
        self.assertFalse(nodes.isEmpty())
        self.assertEqual(nodes.select().action, "b")
        nodes.add(search.SearchNode(None, "c", 0, 0), 4)
        self.assertEqual(nodes.select().action, "a")
        nodes.add(search.SearchNode(None, "d", 2, 0), 2)
        self.assertIn(nodes.select().action, ["c", "d"])
        self.assertIn(nodes.select().action, ["c", "d"])
        self.assertTrue(nodes.isEmpty())
        nodes.add(search.SearchNode(None, "e", 4, 0), 1)
        nodes.add(search.SearchNode(None, "f", 0, 0), 6)
        self.assertEqual(nodes.select().action, "e")
        self.assertFalse(nodes.isEmpty())


class AstarSearchTest(unittest.TestCase):
    def test_simple_start(self):
        p3 = puzzle.EightPuzzle([1, 2, 5, 3, 4, 0, 6, 7, 8])
        soln = search.graph_search(p3, search.AstarNodes())
        self.assertEqual(len(soln), 3)
        self.assertEqual(["up", "left", "left"], [a.type for a in soln])

    def test_intermediate_length(self):
        p2 = puzzle.EightPuzzle([0, 1, 2, 4, 3, 5, 7, 6, 8])
        soln = search.graph_search(p2, search.AstarNodes())
        self.assertEqual(len(soln), 18)
