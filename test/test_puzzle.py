__author__ = 'tchajed'

import unittest
import search
import puzzle
from puzzle import State


def create():
    return puzzle.EightPuzzle([1, 6, 0, 2, 7, 8, 3, 4, 5])


class ProblemDefinitionTest(unittest.TestCase):
    def test_initial_state(self):
        initial = [1, 6, 0, 2, 7, 8, 3, 4, 5]
        p = puzzle.EightPuzzle(initial)
        self.assertEquals(p.initial_state(), State(initial))

    def test_is_goal(self):
        initial = [1, 6, 0, 2, 7, 8, 3, 4, 5]
        p = puzzle.EightPuzzle(initial)
        self.assertFalse(p.isGoal(State(initial)))
        self.assertTrue(p.isGoal(State([0, 1, 2, 3, 4, 5, 6, 7, 8])))

    def test_next_actions(self):
        p = create()
        actions = p.applicable_actions(State([1, 6, 0, 2, 7, 8, 3, 4, 5]))
        self.assertEqual(len(actions), 2)
        self.assertEqual(actions,
                         [search.Action("left", 1,
                                       State([1, 0, 6, 2, 7, 8, 3, 4, 5])),
                          search.Action("down", 1,
                                       State([1, 6, 8, 2, 7, 0, 3, 4, 5]))])

        actions = p.applicable_actions(State([1, 6, 2, 0, 7, 8, 3, 4, 5]))
        self.assertEqual(len(actions), 3)

        actions = p.applicable_actions(State([1, 6, 2, 7, 0, 8, 3, 4, 5]))
        self.assertEqual(len(actions), 4)

    def test_heuristic(self):
        p = create()
        h = p.heuristic(State([1, 6, 0, 2, 7, 8, 3, 4, 5]))
        # 160    012
        # 278 -> 345
        # 345    678
        self.assertEqual(h,
                         1 + 3 + 2 +
                         3 + 1 + 1 +
                         1 + 1 + 1)
        h = p.heuristic(State([0, 1, 2, 4, 3, 5, 7, 6, 8]))
        # 012    012
        # 435 -> 345
        # 768    678
        self.assertEqual(h,
                         0 + 0 + 0 +
                         1 + 1 + 0 +
                         1 + 1 + 0)

        final = State([0, 1, 2, 3, 4, 5, 6, 7, 8])
        self.assertTrue(p.isGoal(final))
        self.assertEqual(0, p.heuristic(final))

