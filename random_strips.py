__author__ = 'tchajed'

from strips import *

random_domain = Domain("random-domain", [
    Operator("op1",
             parameters=["?x1", "?x2", "?x3"],
             preconditions=[Predicate("S", ["?x1", "?x2"]),
                            Predicate("R", ["?x3", "?x1"])],
             effect=[Predicate("S", ["?x2", "?x1"]),
                     Predicate("S", ["?x1", "?x3"]),
                     Predicate("R", ["?x3", "?x1"]).negate()]),
    Operator("op2",
             parameters=["?x1", "?x2", "?x3"],
             preconditions=[Predicate("S", ["?x3", "?x1"]),
                            Predicate("R", ["?x2", "?x2"])],
             effect=[Predicate("S", ["?x1", "?x3"]),
                     Predicate("S", ["?x3", "?x1"]).negate()]),
])

problem = Problem("random-pbl1", random_domain,
                  init=[Predicate("S", ["B", "B"]),
                        Predicate("S", ["C", "B"]),
                        Predicate("S", ["A", "C"]),
                        Predicate("R", ["B", "B"]),
                        Predicate("R", ["C", "B"])],
                  goal=[Predicate("S", ["A", "A"])])