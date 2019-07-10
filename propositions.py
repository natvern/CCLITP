## Project  : CCLITP
## Propositions defined as classes
## Created  : 7/4/2019 - 19:52
## andrewID : srahmoun

# Propositions are building tiles for formula

class Prop:
    def __init__(self, name):
        self.state = True
        self.name = name

    # Get state of the proposition
    # Falsehood being False
    # Truthood being True
    def getState(self):
        return self.state

    # To print the Clause as its name
    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    def __len__(self):
        return 1

# Constants for falsehood and truthhood
class FalseHood(Prop):
    def __init__(self):
        Prop.__init__(self, "False")
        self.state = False

class TruthHood(Prop):
    def __init__(self):
        Prop.__init__(self, "True")


