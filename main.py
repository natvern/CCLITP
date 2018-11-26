#    15-112: Principles of Programming and Computer Science
#    Project: Implementing a First-Order logic interactive theorem prover
#    Name      : Samar Rahmouni
#    AndrewID  : srahmoun

#    File Created: 17th November 2018
#    Modification History:
#    Start                End
#    19/11 20:40          19/11 21:20
#    20/11 12:54          20/11 13:10
#    20/11 16:23          20/11 18:20
#    24/11 14:57          24/11 17:36

# Clauses are building tiles for formula
# They are objects which can either be True or False


class Clause:
    def __init__(self, name):
        self.state = True
        self.name = name

    # If dealing with NOT A, we will change the state
    def changeState(self):
        self.state = not self.state

    # To print the Clause as its name
    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

# We will define the inference rules that would apply
# They are directly derived from sequent calculus


class Rules:
    def __init__(self):
        self.axiom = [self.equality]
        self.rules = [self.disjunction]

    # The only axiom is when we have two atomic clauses on both sides
    def equality(self, A, B):
        for i in A:
            if i in B:
                return True
        return False

    # When facing a disjunction, we separate the formula into two new formula
    # That we define as new goals
    def disjunction(self, A, B):
        newGoals = []
        for i in range(2):
            newGoal = ([A[i]], B)
            newGoals.append(newGoal)
        return newGoals

    # A conjunction would create two new goals
    def conjunction(self, A, B):
        newGoals = []
        for i in range(2):
            newGoal = (A,[B[i]])
            newGoals.append(newGoal)
        return newGoals

    # If it is an implication, we can think of the A implies B as A a hypothesis
    # And B a conclusion, basically shifting the initial conclusion
    def implication(self, A, B):
        return [([A],[B])]


# Input the formula (Theorem to prove)
# A formula is based on a hypothesis and a conclusion
# We define them as an object


class Formula:
    def __init__(self, goals):
        self.goal = [goals]
        self.proof = Rules()

    # Prints the current state of the goals
    def showGoal(self):
        i = 0
        for form in self.goal:
            print(i, ": ", str(form[0]) + "|--" + str(form[1]))
            i =+ 1


    # Apply the rules on the specific goal the user chooses
    def applyRules(self, numGoal):
        # Our base case is when goal is empty (no more to prove)
        if self.goal == []:
            print("Reached an axiom. Exit.")
            return True

        # If there is an "and" on the left side, we delete it
        if len(self.goal[num][0]) > 2 and self.goal[num][0][2] == "and":
            del self.goal[num][0][2]

        # If there is an "or" on the right side, we delete it
        if len(self.goal[num][1]) > 2 and self.goal[num][1][2] == "or":
            del self.goal[num][1][2]

        # Check if there is a logical operator on the left side:
        if len(self.goal[num][0]) > 2:
            # If there is a disjunction on the left side, we get two new goals
            if self.goal[num][0][2] == "or":
                newGoal = self.proof.disjunction(self.goal[num][0][:2],self.goal[num][1])
                del self.goal[num]
                self.goal += newGoal

        # Check if there is a logical operator on the right side:
        elif len(self.goal[num][1]) > 2:
            # If it is an implication
            if self.goal[num][1][2] == "imply":
                newGoal = self.proof.implication(self.goal[num][1][0],self.goal[num][1][1])
                del self.goal[num]
                self.goal += newGoal

            elif self.goal[num][1][2] == "and":
                newGoal = self.proof.conjunction(self.goal[num][0][:2],self.goal[num][1][:2])
                del self.goal[num]
                self.goal += newGoal


        # If there is no logical operator, it might be an axiom
        elif self.proof.equality(self.goal[num][0], self.goal[num][1]):
            del self.goal[num]

        # If nothing is applied
        else:
            print("Found no inference rule to apply. Cannot prove any further. Check your initial statement.")



# Testing input
A = Clause("A")
B = Clause("B")


firstFormula = ([],[A,A,"imply"])
statement = Formula(firstFormula)

while statement.goal != []:
    # We ask for which formula we want to apply the rule to first
    statement.showGoal()
    num = -1
    while num not in range(0,len(statement.goal)):
        num = int(input("Enter a correct goal to apply the rule to: "))
    statement.applyRules(num)

print("Reached an axiom. Proof is over.")