#    Name      : Samar Rahmouni
#    AndrewID  : srahmoun
#    Representing formulas by their connectives, and sub_formulas
#    We are making the representation independant of python representation 
#    (Previously lists)

#    NOTES FROM 7/24/2019
#    Recursion to print formulas is missing a base case for 
#    empty formulas. Find how to define "empty" rather that 
#    NONE which indicates an atom

from enum import Enum
from propositions import Prop

class Conn(Enum):
    AND = 4
    OR = 3
    IMPL = 2
    NOT = 1
    NONE = 0 

class Formula:
    def __init__(self, connective, args):
        self.conn = connective
        self.sub_forms = args

    ## Equality of formulas
    def __eq__(self, f2):
        if self.conn == f2.conn:
            if self.conn.value >= 2:
                return (self.sub_forms[0] == f2.sub_forms[0]) and (self.sub_forms[1] == f2.sub_forms[1])
            if self.conn.value == 1:
                return self.sub_forms[0] == f2.sub_forms[0]
            if self.conn.value == 0:
                return self.sub_forms == f2.sub_forms
        return False

    def getAtom(self):
        if self.conn.value == 0:
            return self.sub_forms  
        else:
            raise "Error: Not atomic"

    def getLeft(self):
        if self.conn.value >= 1:
            return self.sub_forms[0]
        else:
            raise "Error: Atom has no connective"

    def getRight(self):
        if self.conn.value > 1:
            return self.sub_forms[1]
        else:
            raise "Error: Not binary connective"

    def getConn(self):
        return self.conn

    def isProp(self):
        return False

    # To print formulas
    def __str__(self):
        return self.print_formula(self)

    def print_formula(self, f):
        if f.getConn().value == 0:
            return str(f.getAtom())
        if f.getConn().value == 1:
            return str(f.getConn()) + " " + self.print_formula(f.getLeft())
        return self.print_formula(f.getLeft()) + " " + str(f.getConn()) + " " + self.print_formula(f.getRight())

    # To iterate over a formula
    def __len__(self):
        return len(self.sub_forms)


