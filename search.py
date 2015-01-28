import time

__author__ = 'tchajed'

import heapq
import random


class Action:
    def __init__(self, type, cost, next_state):
        self.type = type
        self.cost = cost
        self.next_state = next_state

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __repr__(self):
        return "Action({} {} ->\n{})".format(self.type,
                                             self.cost,
                                             self.next_state)

    @classmethod
    def initial(cls, state):
        return Action("initial", 0, state)


class SearchNode:
    def __init__(self, parent, action, path_cost, depth):
        """

        :param parent: the SearchNode this node came from. None for the initial
        state.
        :type parent: SearchNode
        :param action: the action taken in parent to obtain this node
        :type action: Action
        :param path_cost: the sum of action costs from the root to this node.
        Always 0 for the root.
        :param depth: the number of nodes on the path from the root to this
        node. The depth of the root node is defined to be 0.
        """
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = depth

    def __repr__(self):
        return "{} g={} depth={}".format(self.action,
                                         self.path_cost,
                                         self.depth)

    @property
    def state(self):
        return self.action.next_state

    def path(self):
        """
        Compute the sequence of actions that achieved this node.

        :return: a list of actions to take, starting with the initial state
        action.
        :rtype : list[Action]
        """
        actions = []
        state = self
        while state.parent is not None:
            actions.append(state.action)
            state = state.parent
        return list(reversed(actions))


class Problem:
    """
    An abstract problem.
    """

    def initial_state(self):
        return None

    def applicable_actions(self, state):
        """
        Determine actions applicable in a given state.

        :return: a list of actions applicable from the given node
        :rtype: list[Action]
        """
        return []

    def heuristic(self, state):
        return 0

    def isGoal(self, state):
        return self.heuristic(state) == 0

    def repr(self, state):
        return repr(state)


class SearchNodes:
    """
    An abstract container for search nodes. The mechanism by which the
    strategy selects nodes determines a search strategy.
    """

    def isEmpty(self):
        return True

    def select(self):
        """
        Select a node from the set of search nodes. This is the crucial
        method that determines how nodes will be searched as they are
        discovered.

        :return: the selected node
        :rtype: SearchNode
        """
        return None

    def add(self, node, h=0):
        """
        Add a node to the fringe.

        :type node: SearchNode
        :param h: the value of the heuristic function evaluated at node
        """
        pass


class AstarNodes(SearchNodes):
    def __init__(self):
        self.nodes = []

    def isEmpty(self):
        if self.nodes:
            return False
        return True

    def select(self):
        _, _, n = heapq.heappop(self.nodes)
        return n

    def add(self, node, h=0):
        """
        :type node: SearchNode
        """
        f = node.path_cost + h
        tie_breaker = random.random()
        heapq.heappush(self.nodes, (f, tie_breaker, node))

    def __repr__(self):
        return repr(self.nodes)


def graph_search(problem, nodes):
    """
    Search for a goal node in the problem. Returns the sequence of actions.

    :type problem: Problem
    :param nodes: an initially empty set of nodes that will determine the
    search strategy
    :type nodes: SearchNodes
    """
    initial = problem.initial_state()
    nodes.add(SearchNode(None, Action.initial(initial), 0, 0))
    cost_so_far = {initial: 0}
    while True:
        if nodes.isEmpty():
            return None
        node = nodes.select()
        if problem.isGoal(node.state):
            return node.path()
        for a in problem.applicable_actions(node.state):
            next_node = SearchNode(parent=node, action=a,
                                   path_cost=node.path_cost + a.cost,
                                   depth=node.depth + 1)
            g = next_node.path_cost
            h = problem.heuristic(a.next_state)
            f = g + h
            if (a.next_state not in cost_so_far or
                    f < cost_so_far[a.next_state]):
                nodes.add(next_node, h)
                cost_so_far[a.next_state] = f


def total_states(problem, max_depth):
    frontier = [problem.initial_state()]
    states = set(frontier)
    for depth in range(1, max_depth+1):
        new_frontier = []
        for start in frontier:
            for a in problem.applicable_actions(start):
                if a.next_state not in states:
                    new_frontier.append(a.next_state)
                    states.add(a.next_state)
        frontier = new_frontier
    return len(states)
