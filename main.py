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
#    05/12 15:23          05/12

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
        self.mainGoal = []

    # The only axiom is when we have two atomic clauses on both sides
    def equality(self, A, B):
        for i in A:
            if i in B:
                return True
        return False

    # When facing a disjunction, we separate the formula into two new formula
    # That we define as new goals
    def disjunction(self, A, B, goal):
        self.mainGoal = goal
        newGoals = []
        for i in [A,B]:
            newGoal = (self.mainGoal[0]+[i], self.mainGoal[1])
            newGoals.append(newGoal)
        return newGoals

    # A conjunction would create two new goals
    def conjunction(self, A, B, goal):
        self.mainGoal = goal
        newGoals = []
        for i in [A,B]:
            newGoal = (self.mainGoal[0],self.mainGoal[1]+[i])
            newGoals.append(newGoal)
        return newGoals

    # If it is an implication (A -> B), we get two new goals
    # One for which A is part of the conclusion,
    # The other is when B is part of the hypothesis
    def implication(self, A, B, goal):
        self.mainGoal = goal
        newGoal_1 = (self.mainGoal[0], self.mainGoal[1] + [A])
        newGoal_2 = (self.mainGoal[0] + [B], self.mainGoal[1])
        return [newGoal_1, newGoal_2]


# Input the formula (Theorem to prove)
# A formula is based on a hypothesis and a conclusion
# We define them as an object


class Formula:
    def __init__(self, goals):
        self.goals = [goals]
        self.proof = Rules()
        self.goal = []
        self.mainGoal = []

    # Prints the current state of the goals
    def showGoal(self):
        for i in range(len(self.goals)):
            print(i, ": ", str(self.goals[i][0]) + "|--" + str(self.goals[i][1]))

    # Define which part of the goal we are applying the rule to
    def defineGoal(self,num):
        numGoal = -1
        side = -1
        while side not in [0,1]:
            side = int(input("Enter 0 for left, 1 for right side: "))
        while numGoal not in range(len(self.goals[num][side])):
            numGoal = int(input("Enter a correct goal to apply the rule to: "))
        return numGoal, side

    # Checks if the statement is only composed of atomic clauses
    def atomic(self):
        hypothesis = self.mainGoal[0]
        conclusion = self.mainGoal[1]
        for statement in hypothesis:
            if len(statement) > 1:
                return False
        for statement in conclusion:
            if len(statement) > 1:
                return False
        return True

    # Apply the rules on the specific goal the user chooses
    def applyRules(self, num):
        self.mainGoal = self.goals[num]

        # Our base case is when goal is empty (no more to prove)
        if self.goals == []:
            print("Reached an axiom. Exit.")
            return True

        if not self.atomic():
            numGoal, side = self.defineGoal(num)
            self.goal = self.mainGoal[side][numGoal]
        else:
            side = -1

        # If the user selects a statement from the conclusion
        if side == 1 and len(self.goal) > 2:
            # If there is an "or" on the right side, we delete it
            if self.goal[2] == "or":
                del self.goal[2]
                return 0
            # If there is an "and" on the right side, we create two new goals
            elif self.goal[2] == "and":
                A = self.goal[0]
                B = self.goal[1]
                del self.mainGoal[side][numGoal]
                newGoal = self.proof.conjunction(A, B, self.mainGoal)
                del self.goals[num]
                self.goals += newGoal
                return 0
            # if there is an "imply" on the right side, we add A to the hypothesis
            elif self.goal[2] == "imply":
                A = self.goal[0]
                B = self.goal[1]
                del self.mainGoal[side][numGoal]
                self.mainGoal[0].append(A)
                self.mainGoal[1].append(B)
                return 0


        # If the user selects a statement from the hypothesis
        elif side == 0 and len(self.goal) > 2:
            # If there is an "and" on the right side, we delete it
            if self.goal[2] == "and":
                del self.goal[2]
                return 0
            # If there is an "or" on the right side, we create two new goals
            elif self.goal[2] == "or":
                A = self.goal[0]
                B = self.goal[1]
                del self.mainGoal[side][numGoal]
                newGoal = self.proof.disjunction(A, B, self.mainGoal)
                del self.goals[num]
                self.goals += newGoal
                return 0
            # If it is an implication, we create two new goals
            elif self.goal[2] == "imply":
                A = self.goal[0]
                B = self.goal[1]
                del self.mainGoal[side][numGoal]
                newGoal = self.proof.implication(A,B,self.mainGoal)
                del self.goals[num]
                self.goals += newGoal
                return 0

        # If there is no logical operator, it might be an axiom
        if self.proof.equality(self.mainGoal[0], self.mainGoal[1]):
            del self.goals[num]



# Testing input
A = Clause("Human")
B = Clause("Socrates")
C = Clause("Death")


firstFormula = ([[[A],[C],"imply"],[[B],[A],"imply"]],[[[B],[C],"imply"]])
statement = Formula(firstFormula)

while statement.goals != []:
    # We ask for which formula we want to apply the rule to first
    statement.showGoal()
    num = -1
    while num not in range(0,len(statement.goals)):
        num = int(input("Enter the number of the goal: "))
    statement.applyRules(num)

print("Reached an axiom. Proof is over.")