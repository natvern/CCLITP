## Project  : CCLITP
## Sequent Calculus Rules for Constructive Logic
## The rules are constructed as a class
## Created  : 8/3/2019 - 20:05
## andrewID : srahmoun

from propositions import FalseHood
from formula import *
import copy

# We define the inference rules of the sequent calculus for
# intuitionistic logic as a class
# note: inference rules take a sequent, the side of the formula and its number
#       they return a list of the new sequents
class Calculus:
    def __init__(self):
        ## List of axioms
        self.axiom = [self.identity]
        ## List of inference rules (note: found_falsehood is a rule rather than an axiom)
        self.rules = [self.disjunction, self.conjunction, self.implication, self.negation, self.found_falsehood]
        self.Falsehood = Formula(Conn.NONE, FalseHood())

    ## Identity is when P, atomic formula is found on both sides
    ## Atomic formula is defined as: "no logical connectives or no strict subformulas" //wiki
    ## input: A is the hypothesis (list of sequents) B is the conclusion (list of one formula)
    ## output: True iff axiom is found, otherwise, False.
    def identity(self, A, B):
        for i in A:
            ## Only one possible formula in the conclusion
            if i == B[0]:
                return True
        return False

    ## If falsehood is found in the hypothesis, the sequent is true
    def found_falsehood(self, hypothesis):
        for f in hypothesis:
            if f.getConn() == Conn.NONE and f.getAtom() != []:
                if f.getAtom().getState() == False:
                    return True
        return False

    ## Disjunction on the left creates two new sequents, where A -> and B ->
    ## Disjunction on the right creates one sequent where either A or B as conclusion
    def disjunction(self, sequent, side, num_formula):
        formula = sequent[side][num_formula]
        A = formula.getLeft()
        B = formula.getRight()
        del sequent[side][num_formula]
        if side == 0:
            new_sequents = []
            for f in [A, B]:
                new_sequent = (sequent[0]+[f], copy.deepcopy(sequent[1]))
                new_sequents.append(new_sequent)
            return new_sequents
        elif side == 1:
            A_or_B = input("Type 0 to select A (r or1) and 1 to select B (r or2)\n")
            if not A_or_B in ["0","1"]:
                raise "Error: did not type 0 or 1"
            conclusion = [A, B][int(A_or_B)]
            new_sequent = (sequent[0], [conclusion])
            return [new_sequent]
        raise "Disjunction: Error choosing side (not 0 or 1)"

    ## Conjunction on the left side disconnects A and B
    ## Conjunction on the right side creates two new sequents where -> A and -> B
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
            for i in [A, B]:
                new_sequent = (copy.deepcopy(sequent[0]), sequent[1] + [i])
                new_sequents.append(new_sequent)
            return new_sequents
        return "Conjunction: Error choosing the side (not 0 or 1)"

    ## Implication of the left side creates two new sequents such that
    ##             implication is kept (contraction is implicit)
    ## Implication of the right side takes A as part of the hypothesis,
    ##             and B as the only conclusion
    def implication(self, sequent, side, num_formula):
        formula = sequent[side][num_formula]
        A = formula.getLeft()
        B = formula.getRight()
        del sequent[side][num_formula]
        if side == 0:
            new_sequent_1 = ([formula] + sequent[0], [A])
            new_sequent_2 = ([B] + sequent[0], sequent[1])
            return [new_sequent_1, new_sequent_2]
        elif side == 1:
            sequent[0].append(A)
            sequent[1].append(B)
            return [sequent]
        return "Implication: Error choosing side (not 0 or 1)"

    ## Negation of A is equivalent to A imply falsehood
    def negation(self, sequent, side, num_formula):
        formula = sequent[side][num_formula]
        A = formula.getLeft()
        sequent[side][num_formula] = Formula(Conn.IMPL, [A, self.Falsehood])
        return [sequent]

    ## Cut breaks the sequent into two new sequents
    ## Delta and Gamma are selected such that Delta U Gamma = Hypothesis
    ## User can select new "A" formula to divide the original sequent
    def cut(self, sequent, cut_l):
        gamma = cut_l[0]
        delta = cut_l[1]
        A = cut_l[2]
        C = sequent[1]
        if delta == []:
            new_sequent_2 = ([gamma, A], C)
        else:
            new_sequent_2 = ([A, delta], C)
        new_sequent_1 = ([gamma], [A])
        return [new_sequent_1, new_sequent_2]
