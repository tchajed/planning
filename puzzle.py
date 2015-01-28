__author__ = 'tchajed'

import search


class State:
    def __init__(self, nums):
        self.nums = tuple(nums)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __hash__(self):
        return hash(self.nums)

    def __repr__(self):
        nums = [str(i) for i in self.nums]
        return "\n".join([
            "".join(nums[0:3]),
            "".join(nums[3:6]),
            "".join(nums[6:9])])


class EightPuzzle(search.Problem):
    def __init__(self, start):
        should_have = set(range(9))
        has = set(start)
        if should_have != has:
            missing = should_have - has
            extra = has - should_have
            raise ValueError(
                "invalid state: missing {}, extra {}".format(missing, extra))
        self.start = State(start)

    def initial_state(self):
        return self.start

    def isGoal(self, state):
        return state.nums == tuple(range(9))

    @classmethod
    def swap(cls, old_state, index1, index2):
        nums = list(old_state.nums)
        nums[index1], nums[index2] = nums[index2], nums[index1]
        return State(nums)

    def applicable_actions(self, state):
        """
        :type state: State
        """
        zero = state.nums.index(0)
        actions = []
        if (zero - 3) >= 0:
            up = EightPuzzle.swap(state, zero, zero - 3)
            actions.append(search.Action("up", 1, up))
        if zero % 3 > 0:
            left = EightPuzzle.swap(state, zero, zero - 1)
            actions.append(search.Action("left", 1, left))
        if zero % 3 < 2:
            right = EightPuzzle.swap(state, zero, zero + 1)
            actions.append(search.Action("right", 1, right))
        if (zero + 3) < 9:
            down = EightPuzzle.swap(state, zero, zero + 3)
            actions.append(search.Action("down", 1, down))
        return actions

    @classmethod
    def manhattan(cls, index1, index2):
        x1, x2 = index1 % 3, index2 % 3
        y1, y2 = index1 // 3, index2 // 3
        return abs(x1-x2) + abs(y1-y2)

    def heuristic(self, state):
        """
        :type state: State
        """
        distance = 0
        for loc, actualLoc in enumerate(state.nums):
            distance += EightPuzzle.manhattan(loc, actualLoc)
        return distance

