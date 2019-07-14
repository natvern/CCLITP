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
from translation import translate

# Input the formula (Theorem to prove)
# A formula is based on a hypothesis and a conclusion
# We define them as an object

class Formula:
    def __init__(self, goals, props):
        self.goals = [goals]
        self.proof = Calculus()
        self.goal = []
        self.mainGoal = []
        self.propositions = props
        self.str_propositions = toString(props)
        self.inProgress = []

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
        elif len(goal) == 2:
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

    def getCut(self, num):
        goal = self.mainGoal
        delta = self.inProgress[0]
        delta_goal = goal[delta[1]][delta[2]]
        gamma = self.inProgress[1]
        gamma_goal = goal[gamma[1]][gamma[2]]
        prop = self.inProgress[2]
        if prop in self.str_propositions:
            for real_prop in self.propositions:
                if real_prop.getName() == prop:
                    prop = [real_prop]
                    print("Yes real prop")
        else:
            prop = Prop(prop)
        del self.goals[num]
        newGoal = self.proof.cut(goal, delta_goal, gamma_goal, prop)
        #print(newGoal)
        self.goals += newGoal
        return "Applied cut"

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
            self.goals += newGoal
            return "Disjunction found"

        elif logical_connective == "and":
            newGoal = self.proof.conjunction(self.mainGoal, side, numGoal)
            del self.goals[num]
            self.goals += newGoal
            return "Conjunction found"

        elif logical_connective == "imply":
            newGoal = self.proof.implication(self.mainGoal, side, numGoal)
            del self.goals[num]
            self.goals += newGoal
            return "Implication found"

        # If there is no logical operator, it might be an axiom
        if self.proof.identity(self.mainGoal[0], self.mainGoal[1]):
            del self.goals[num]
            return "An axiom was found. The only axiom in sequent calculus is when the same atomic clauses are" \
            " present in both sides. An atomic clause is something that is not defined by a logical operator." \
            " for instance, '15-112' is an atomic clause, '15-112 is the best' is a compound statement."

        elif self.proof.found_falsehood(self.mainGoal[0]):
            del self.goals[num]
            return "Falsehood in the hypothesis found"

        return "You just clicked on something that did not do much. Try playing with another button."