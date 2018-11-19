#    15-112: Principles of Programming and Computer Science
#    Project: Implementing a First-Order logic interactive theorem prover
#    Name      : Samar Rahmouni
#    AndrewID  : srahmoun

#    File Created: 17th November 2018
#    Modification History:
#    Start                End
#    20:40                


# Clauses are building tiles for formula
# They are objects which can either be True or False


class Clause:
    def __init__(self):
        self.state = True

# We will define the inference rules that would apply
# They are directly derived from sequent calculus


class Rules:
    def __init__(self):
        self.
        self.axioms = [Formula(Clause(), Clause())]

# Input the formula (Theorem to prove)
# A formula is based on a hypothesis and a conclusion
# We define them as an object


class Formula:
    def __init__(self, leftSide, rightSide):
        self.hypothesis = leftSide
        self.conclusion = rightSide
        self.form = (self.hypothesis, self.conclusion)
