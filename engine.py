#    15-112: Principles of Programming and Computer Science
#    Project: Implementing a First-Order logic interactive theorem prover
#    Name      : Samar Rahmouni
#    AndrewID  : srahmoun
#    Clauses, Rules and Formula are defined as classes that apply rules

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

    # Shows the first statement that we are proving
    def showStatement(self):
        statement = self.goals[0]
        hypothesis = statement[0]
        conclusion = statement[1]
        hypothesis_text = ""
        conclusion_text = ""
        for hypo in hypothesis:
            if len(hypo) > 2:
                hypothesis_text += self.translate(hypo[0]) + " " + hypo[2] + " " + self.translate(hypo[1]) +","
            else:
                hypothesis_text += str(hypo)

        for conc in conclusion:
            if len(conc) > 2:
                conclusion_text += str(conc[0]) + " " + conc[2] + " " + str(conc[1])
            else:
                conclusion_text += str(conc)

        if hypothesis == []:
            return conclusion_text
        return "If " + hypothesis_text + " then " + conclusion_text

    # Translates from List to a readable Statement
    def translate(self, goal):
        text = ""
        if len(goal) > 2:
                text = text + str(goal[0]) + " " + str(goal[2]) + " " + str(goal[1])
        else:
                text = text + str(goal)
        return text

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
    def applyRules(self, num, side, numGoal):
        self.mainGoal = self.goals[num]

        # Our base case is when goal is empty (no more to prove)
        if self.goals == []:
            print("Reached an axiom. Exit.")
            return True

        if not self.atomic():
            self.goal = self.mainGoal[side][numGoal]
        else:
            side = -1

        # If the user selects a statement from the conclusion
        if side == 1 and len(self.goal) > 2:
            # If there is an "or" on the right side, we delete it
            if self.goal[2] == "or":
                A = self.goal[0]
                B = self.goal[1]
                del self.mainGoal[side][numGoal]
                self.mainGoal[0].append(A)
                self.mainGoal[0].append(B)
                return "We applied the 'or' rule on the right side. Basically, an or in the conclusion does not matter." \
                "Hence, we can delete it and take the statements as separates."
            # If there is an "and" on the right side, we create two new goals
            elif self.goal[2] == "and":
                A = self.goal[0]
                B = self.goal[1]
                del self.mainGoal[side][numGoal]
                newGoal = self.proof.conjunction(A, B, self.mainGoal)
                del self.goals[num]
                self.goals += newGoal
                return "We applied the 'and' rule on the right side. In other words, we define two new goals. First," \
                "if we have 'A and B', then we need to prove the conclusion for both A and B."
            # if there is an "imply" on the right side, we add A to the hypothesis
            elif self.goal[2] == "imply":
                A = self.goal[0]
                B = self.goal[1]
                del self.mainGoal[side][numGoal]
                self.mainGoal[0].append(A)
                self.mainGoal[1].append(B)
                return "We applied the 'imply' rule on the right side. If we have 'A imply B' then we consider A as" \
                " part of the hypothesis and B the conclusion for everything."


        # If the user selects a statement from the hypothesis
        elif side == 0 and len(self.goal) > 2:
            # If there is an "and" on the left side, we delete it and shift other statements
            if self.goal[2] == "and":
                A = self.goal[0]
                B = self.goal[1]
                del self.mainGoal[side][numGoal]
                self.mainGoal[0].append(A)
                self.mainGoal[0].append(B)
                return "We applied the 'and' rule on the left side. Basically, an 'and' on the hypothesis does not" \
                " matter. So we consider the statements as separates."
            # If there is an "or" on the right side, we create two new goals
            elif self.goal[2] == "or":
                A = self.goal[0]
                B = self.goal[1]
                del self.mainGoal[side][numGoal]
                newGoal = self.proof.disjunction(A, B, self.mainGoal)
                del self.goals[num]
                self.goals += newGoal
                return "We applied the 'or' rule on the left side. We do so by considering two new goals. One for" \
                " every part of the 'or' statement as part of the hypothesis."
            # If it is an implication, we create two new goals
            elif self.goal[2] == "imply":
                A = self.goal[0]
                B = self.goal[1]
                del self.mainGoal[side][numGoal]
                newGoal = self.proof.implication(A,B,self.mainGoal)
                del self.goals[num]
                self.goals += newGoal
                return "We applied the 'imply' rule on the left side. We consider two new goals. Example: A->B" \
                " Then we get two new goals, one for which A is part of the conclusion and the other where B is" \
                " in the hypothesis."

        # If there is no logical operator, it might be an axiom
        if self.proof.equality(self.mainGoal[0], self.mainGoal[1]):
            del self.goals[num]
            return "An axiom was found. The only axiom in sequent calculus is when the same atomic clauses are" \
            " present in both sides. An atomic clause is something that is not defined by a logical operator." \
            " for instance, '15-112' is an atomic clause, '15-112 is the best' is a compound statement."

        return "You just clicked on something that did not do much. Try playing with another button."