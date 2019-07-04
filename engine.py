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

from calculus import Calculus
from propositions import *

# Input the formula (Theorem to prove)
# A formula is based on a hypothesis and a conclusion
# We define them as an object


class Formula:
    def __init__(self, goals):
        self.goals = [goals]
        self.proof = Calculus()
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
                hypothesis_text += self.toString(hypo[0]) + " " + hypo[2] + " " + self.toString(hypo[1]) +","
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
    def toString(self, goal):
        text = ""
        if len(goal) > 2:
                text = text + str(goal[0]) + " " + str(goal[2]) + " " + str(goal[1])
        if len(goal) == 2:
                text = text + str(goal[1]) + " " + str(goal[0])
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
    # We keep track of the side : 
    #           0 - choose a proposition from the hypothesis
    #           1 - choose a proposition from the conclusion
    # The num goal is the position of the proposition in the list 
    # representing the formula

    def applyRules(self, num, side, numGoal):
        # This is the chosen proposition 
        self.mainGoal = self.goals[num]

        # Our base case is when goal is empty (no more to prove)
        if self.goals == []:
            print("Reached an axiom. Exit.")
            return True

        if not self.atomic():
            self.goal = self.mainGoal[side][numGoal]
        else:
            side = -1
 
        logical_connective = self.mainGoal[side][numGoal][-1]

        ## APPLY RULES ACCORDING TO THE LOGICAL CONNECTIVE
        if logical_connective == "not":
            self.proof.negation(self.mainGoal, side, numGoal)
            return "We make the not equivalent to an implication for falsehood."

        elif logical_connective == "or":
            newGoal = self.proof.disjunction(self.mainGoal, side, numGoal)
            del self.goals[num] 
            self.goals += [newGoal]
            print(self.goals)
            return "Disjunction found"

        #elif logical_connective == "and":
        #    newGoal = self.proof.conjunction(self.mainGoal, side, numGoal)

        #else:
        #    return ""

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
        if self.proof.identity(self.mainGoal[0], self.mainGoal[1]):
            del self.goals[num]
            return "An axiom was found. The only axiom in sequent calculus is when the same atomic clauses are" \
            " present in both sides. An atomic clause is something that is not defined by a logical operator." \
            " for instance, '15-112' is an atomic clause, '15-112 is the best' is a compound statement."

        return "You just clicked on something that did not do much. Try playing with another button."