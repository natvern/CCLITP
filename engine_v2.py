#    15-112: Principles of Programming and Computer Science
#    Project: Implementing a First-Order logic interactive theorem prover
#    Name      : Samar Rahmouni
#    AndrewID  : srahmoun
#    Clauses, Rules and Formula are defined as classes that apply rules


#    NOTES FROM 7/1/2019
#    Clauses as defined are atoms, rather than clauses. 
#    Disjunction and conjunction rules are basically the same, change to "left_side" vs. "right_side"

#    NOTES FROM 7/4/2019 
#    Rules have been changed to a new file specific to sequent calculus

#    NOTES FROM 7/15/2019
#    Change formula (change parse_f function)

#    NOTES FROM 7/22/2019 
#    Rewrite engine file to match the new representation of formulas

from calculus import Calculus
from propositions import *
from formula import *

# Theorem class takes as input a sequent represented as :
# a tuple defined (formula_1, formula_2)
# Where formula_1 is the hypothesis, formula_2 is the conclusion
# Formulas are represented as objects 

class Theorem:
    def __init__(self, sequent):
        self.sequents = [sequent]
        self.proof = Calculus() 
        self.propositions = self.getProps(sequent[0][0]) + self.getProps(sequent[1][0])

    def getProps(self, f, atoms = []):
        if f.getConn().value == 0:
            if f.getAtom() != []:
                if not f.getAtom() in atoms:
                    return atoms + [f.getAtom()]
        elif f.getConn().value == 1:
            return self.getProps(f.getLeft(), atoms)
        elif f.getConn().value >= 2:
            return self.getProps(f.getLeft(), atoms)
            return self.getProps(f.getRight(), atoms)
        else:
            raise "Error: invalid enumeration for connective"
        return atoms

    def showStatement(self):
        return "If " + str(self.sequents[0][0][0]) + " then " + str(self.sequents[0][1][0])

    def toString(self, formula):
        return str(formula)

    # There might be multiple sequents to prove, num_sequent indicates 
    # which one we selected to apply Rules on
    # The side can be 0 (hypothesis) or 1 (conclusion)
    # The num_formula is to choose which sub_formula we apply the rule to
    def applyRules(self, num_sequent, side, num_formula):
        
        # Base case: no sequent to prove
        if self.sequents == []:
            print("Reached an axiom.")
            return True

        sequent = self.sequents[num_sequent]
        logical_connective = sequent[side][num_formula].getConn()

        # We check for an axiom
        if self.proof.identity(sequent[0], sequent[1]):
            del self.sequents[num_sequent]
            return "Identity found"
        if self.proof.found_falsehood(sequent[0]):
            del self.sequents[num_sequent]
            return "Falsehood found in hypothesis"

        # We apply the rules according to the logical connective
        if logical_connective == Conn.NOT:
            self.proof.negation(sequent, side, num_formula)
            return "Negation found"

        if logical_connective == Conn.OR:
            new_sequent = self.proof.disjunction(sequent, side, num_formula)
            del self.sequents[num_sequent]
            self.sequents += new_sequent
            return "Disjunction found"

        if logical_connective == Conn.AND:
            new_sequent = self.proof.conjunction(sequent, side, num_formula)
            del self.sequents[num_sequent]
            self.sequents += new_sequent
            return "Conjunction found"

        if logical_connective == Conn.IMPL:
            new_sequent = self.proof.implication(sequent, side, num_formula)
            del self.sequents[num_sequent]
            self.sequents += new_sequent
            return "Implication found"

        if logical_connective == Conn.NONE:
            return "No axiom found"

        raise "Error: Connective is inexistant"


        

    