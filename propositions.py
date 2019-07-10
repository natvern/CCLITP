## Project  : CCLITP
## Propositions defined as classes
## Created  : 7/4/2019 - 19:52
## andrewID : srahmoun

# Propositions are building tiles for formula

class Prop:
    def __init__(self, name):
        self.state = True
        self.name = name

    # If dealing with NOT A, we will change the state
    def getState(self):
        self.state = not self.state

    # To print the Clause as its name
    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

# Constants for falsehood and truthhood
class FalseHood(Prop):
    def __init__(self):
        Prop.__init__(self, "False")
        self.state = False
        
class TruthHood(Prop):
    def __init__(self):
        Prop.__init__(self, "True")


