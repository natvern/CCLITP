#    Name      : Samar Rahmouni
#    AndrewID  : srahmoun
#    Representing formulas by their connectives, and sub_formulas
#    We are making the representation independant of python representation 
#    (Previously lists)

from enum import Enum
from propositions import Prop

class Conn(Enum):
    AND = 2
    OR = 2
    IMPL = 2
    NOT = 1
    NONE = 0 

class Formula:
    def __init__(self, connective, args):
        self.conn = connective
        self.sub_forms = args

    def getAtom(self):
        if self.conn.value == 0:
            return self.sub_forms  
        else:
            raise "Error: Not atomic"

    def getLeft(self):
        if self.conn.value == 2:
            return self.sub_forms[0]
        else:
            raise "Error: Not binary connective"

    def getRight(self):
        if self.conn.value == 2:
            return self.sub_forms[1]
        else:
            raise "Error: Not binary connective"

    def getConn(self):
        return self.conn


