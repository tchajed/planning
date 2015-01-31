__author__ = 'tchajed'


class Domain:
    def __init__(self, name, operators):
        """
        :param name: The name of this domain
        :param operators: a list of symbolic operators that define the domain
        :type operators: list[Operator]
        """
        self.name = name
        self.operators = operators


class Operator:
    @classmethod
    def is_symbol(cls, name):
        """
        :type name: string
        :return: True if name is a valid symbol name
        """
        return name.startswith("?")

    def __init__(self, name, parameters, preconditions, effect):
        """
        :param name: name of this operator
        :param parameters: symbolic parameters this operator takes
        :type parameters: list[string]
        :param preconditions: conjunction of precondition predicates in terms
        of the operator parameters
        :type preconditions: list[Predicate]
        :param effect: predicates that hold after executing the operator in
        terms of the operator parameters
        :type effect: list[Predicate]
        """
        for param in parameters:
            if not Operator.is_symbol(param):
                raise ValueError("param {} is not a valid symbol".format(param))
        params = set(parameters)
        for cond in preconditions:
            for arg in cond.arguments:
                if arg not in params:
                    raise ValueError("precondition {} refers to non-existent "
                                     "parameter {}".format(cond, arg))
        for effect in effect:
            for arg in effect.arguments:
                if arg not in params:
                    raise ValueError("effect {} refers to non-existent "
                                     "parameter {}".format(effect, arg))
        self.name = name
        self.parameters = parameters
        self.preconditions = preconditions
        self.effect = effect


class Predicate:
    def __init__(self, head, arguments, negated=False):
        self.head = head
        self.arguments = arguments
        self.negated = negated

    def negate(self):
        return Predicate(self.head, self.arguments, negated=True)


class Action:
    def __init__(self, head, arguments):
        self.head = head
        self.arguments = arguments


class Problem:
    def __init__(self, name, domain, init, goal):
        """
        :param name: The name of this problem
        :type domain: Domain
        :param init: initial state
        :type init: list[Predicate]
        :param goal: goal state
        :type goal: list[Predicate]
        """
        self.name = name
        self.domain = domain
        self.init = init
        self.goal = goal
