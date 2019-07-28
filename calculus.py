## Project  : CCLITP
## Sequent Calculus Rules constructed as a class
## Created  : 7/4/2019 - 19:42
## andrewID : srahmoun

## NOTES FROM 7/10/2019
## Rules are independant of the engine, hence changing the logic
## would mean writing a new file for different inference rules

from propositions import FalseHood
from formula import *

# We will define the inference rules that would apply
# They are directly derived from sequent calculus
class Calculus:
    def __init__(self):
        self.axiom = [self.identity, self.found_falsehood]
        self.rules = [self.disjunction, self.conjunction, self.implication, self.negation]
        #self.mainGoal = []
        self.Falsehood = Formula(Conn.NONE, FalseHood())

    # One axiom is when we have the same atomic clauses on both sides
    def identity(self, A, B):
        for i in A:
            if i in B:
                return True
        return False

    # Another axiom is when falsehood is found in the hypothesis
    def found_falsehood(self, hypothesis):
        for f in hypothesis:
            if f.getConn() == Conn.NONE and f.getAtom() != []:
                if f.getAtom().getState() == False:
                    return True
        return False

    # When facing a disjunction, we separate the formula into two new formula
    # That we define as new goals
    def disjunction(self, sequent, side, num_formula):
        formula = sequent[side][num_formula]
        if side == 0:
            new_sequents = []
            del sequent[side][num_formula]
            for f in [formula.getLeft(),formula.getRight()]:
                new_sequent = (sequent[0]+[f], sequent[1])
                new_sequents.append(new_sequent)
            return new_sequents
        elif side == 1:
            # If there is an "or" on the right side, we delete it
            A = formula.getLeft()
            B = formula.getRight()
            del sequent[side][num_formula]
            sequent[side].append(A)
            sequent[side].append(B)
            return [sequent]
        raise "Disjunction: Error choosing the side (not 0 or 1)"

    # A conjunction would create two new goals
    def conjunction(self, sequent, side, num_formula):
        formula = sequent[side][num_formula]
        A = formula.getLeft()
        B = formula.getRight()
        del sequent[side][num_formula]
        if side == 0:
            sequent[side].append(A)
            sequent[side].append(B)
            return [sequent]
        elif side == 1: 
            new_sequents = []
            for i in [A,B]:
                new_sequent = (sequent[0],sequent[1]+[i])
                new_sequents.append(new_sequent)
            return new_sequents
        return "Conjunction: Error choosing the side (not 0 or 1)"

    # If it is an implication (A -> B), we get two new goals
    # One for which A is part of the conclusion,
    # The other is when B is part of the hypothesis
    def implication(self, sequent, side, num_formula):
        formula = sequent[side][num_formula]
        if side == 0:
            del sequent[side][num_formula]
            new_sequent_1 = (sequent[0], sequent[1] + [formula.getLeft()])
            new_sequent_2 = (sequent[0] + [formula.getRight()], sequent[1])
            return [new_sequent_1, new_sequent_2]
        elif side == 1:
            A = formula.getLeft()
            B = formula.getRight()
            del sequent[side][num_formula]
            sequent[0].append(A)
            sequent[1].append(B)
            return [sequent]
        return "Implication: Error choosing the side (not 0 or 1)"

    # Negation is equivalent to A imply Falsehood
    def negation(self, sequent, side, num_formula):
        formula = sequent[side][num_formula]
        print(formula)
        A = formula.getLeft()
        sequent[side][num_formula] = Formula(Conn.IMPL, [A, self.Falsehood])
        #[A, [self.Falsehood], "imply"]
        return [sequent]

    # Cut breaks the main goal into smaller goals that
    # make it easier to prove
    # Delta and Gamma are lists of formula
    # Make sure that Delta U Gamma = Hypothesis
    def cut(self, mainGoal, delta, gamma, prop):
        self.mainGoal = mainGoal
        C = self.mainGoal[1]
        newGoal_1 = (gamma,[prop])
        newGoal_2 = ([prop, delta],C)
        return [newGoal_1, newGoal_2]

