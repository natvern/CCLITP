#    15-112: Principles of Programming and Computer Science
#    Project: Implementing a First-Order logic interactive theorem prover
#    Name      : Samar Rahmouni
#    AndrewID  : srahmoun
#    Graphical user interface that displays the proof


#import engine
import tkinter
from tkinter import messagebox
import engine

class Menu:
    def __init__(self, root, formula):
        # Description of the program
        self.explain = "This program is part of a project for a programming course in CMU-Q. It is meant to prove" \
        " logical statements, such as proving that there exists a path between a and c if there exists a " \
        " path between a and b and b and c. It uses sequent calculus rules to derive formulas. The proof is " \
        " point-and-click where every click applies an inference rule that is explained." \
        " Check the menu at the right to start proving the statement in the bottom."
        self.formula = formula
        self.root = root
        self.frame = tkinter.Frame(self.root, bg="#062356", height=400)
        self.root.title("Menu")
        self.title = tkinter.Label(text="First Order Logic Interactive Theorem Prover", bg="#6B030B", fg="#062356", font=("",44), width=40)
        self.explanation = tkinter.Message(self.frame,text=self.explain, width="300", bg="#6B030B", pady=100)
        self.statement = tkinter.Label(text=self.formula.showStatement(),  bg="#6B030B", fg="#062356", font=("",20), width=90)
        # Buttons
        self.proof = tkinter.Button(self.frame, text="Start Proving", highlightbackground="#062356", pady=40, command=self.startProof)
        self.guideline = tkinter.Button(self.frame, text="Input Guidelines", highlightbackground="#062356", pady=20, command=self.startGuideline)
        # Displaying 
        self.title.pack()
        self.explanation.pack(side="left", padx=20)
        self.proof.pack()
        self.guideline.pack(side="top")
        self.statement.pack(side="bottom")
        self.frame.pack()

    # Changes Frame to Proof
    def startProof(self):
        self.frame.destroy()
        newFrame = Proof(self.root, self.formula)

    # Changes Frame to Guidlines
    def startGuideline(self):
        self.frame.destroy()
        self.title.destroy()
        self.statement.destroy()
        newFrame = Guideline(self.root, self.formula)

class Guideline:
    # Guidlines to how to handle input
    def __init__(self, root, formula):
        self.explain = "To change the input, modifications to the code is necessary. To make the change, we" \
        " will first understand how the input works. To do so, we will take the statement '((A imply B) imply A) imply A " \
        " Surprisingly, a true statement. First, how sequent calculus works is that there is a hypothesis and a conclusion." \
        " We express the statement as a tuple : (hypothesis, conclusion).Since this case is always true, it does not have a hypothesis. " \
        " Both hypothesis and conclusion are lists. There is no hypothesis so, it is an empty list: ([], [conclusion])." \
        " Now, looking at the conclusion, there is 3 compounds statements so three lists + conclusion list. The first one would be" \
        " [ (A imply B) imply A , [A] ,'imply' ], and we follow the same logic for the rest. Hence: [[[[A],[B],'imply'],[A],'imply'], [A], 'imply']]." \
        " Therefore, we will have: ([], [[[[A],[B],'imply'],[A],'imply'], [A], 'imply']]). One just needs to remind that everything is a list." \
        " From simple atomic clauses to complex compound statements. The possible logical operations are: 'imply', 'and', 'or'."
        self.formula = formula
        self.root = root
        self.frame = tkinter.Frame(self.root, bg="#062356", height=400)
        self.root.title("Guidelines")
        self.title = tkinter.Label(text="Input Guidelines", bg="#6B030B", fg="#062356", font=("",44), width=40)
        self.explanation = tkinter.Message(self.frame,text=self.explain, width="300", bg="#6B030B", pady=100)
        # Buttons
        self.menu = tkinter.Button(self.frame, text="Go back to Menu", highlightbackground="#062356", pady=40, command=self.startMenu)
        # Displaying 
        self.title.pack()
        self.explanation.pack(side="left", padx=20)
        self.menu.pack()
        self.frame.pack()
    def startMenu(self):
        self.frame.destroy()
        self.title.destroy()
        newFrame = Menu(self.root, self.formula)



class Proof:
    def __init__(self,root, formula):
        # List of the goals
        self.formula = formula
        # Options is a list of the clauses we can click (to apply rules to)
        self.options = []
        # Window and Frame
        self.root = root
        self.root.title("First Order Logic Interactive Theorem Prover")
        self.frame = tkinter.Frame(self.root, bg="#062356")
        # Every Frame is a step of the proof
        self.frames = []
        self.displayFormula()
        self.frame.pack()
        # Added to apply cut
        self.give_A = tkinter.Entry(self.frames[-1])
        self.contraction = False

    def buttonClicked(self, goal, statement, clause):
        if goal == -2 and statement == -2 and clause == -2:
            self.contraction = True
            return 0

        if self.formula.inProgress == "A":
            self.give_A = tkinter.Entry(self.frames[-1])
            self.formula.inProgress = "give_A"
            self.give_A.pack()
            return 0

        if self.formula.inProgress == "give_A":
            print(self.give_A.get())
            message = self.formula.applyRules(goal, statement, clause, self.give_A.get())
            self.formula.inProgress = "Cut"
        elif self.contraction:
            message = self.formula.applyRules(goal, statement, clause, "Contraction")
            self.contraction = False
        else:
            message = self.formula.applyRules(goal, statement, clause)

        messagebox.showinfo("Rule applied",message)
        if message == "You just clicked on something that did not do much. Try playing with another button.":
            return 0
        if self.formula.sequents != []:
            self.displayFormula()
        else:
            end = tkinter.Label(text = "Reached an axiom. Proof is done.")
            end.pack()

    # Displaying Formula
    def displayFormula(self):
        self.frames.append(tkinter.Frame(self.frame, bg="#062356"))
        j = len(self.frames)
        i = len(self.options)
        for goal in range(len(self.formula.sequents)):
            for statement in range(2):
                for clause in range(len(self.formula.sequents[goal][statement])):
                    self.options.append(tkinter.Button(self.frames[j-1], text=self.formula.toString(self.formula.sequents[goal][statement][clause]), highlightbackground="#062356", command=lambda x=goal, y=statement, z=clause: self.buttonClicked(x,y,z)))
                    if goal != 0 and statement == 0 and clause == 0:
                        newGoal = tkinter.Label(self.frames[j-1], bg="#062356", fg="#062356", text="//////")
                        newGoal.pack(side="left")

                    self.options[i].pack(side="left")
                    i += 1
                # Separate the hypothesis from the conclusion
                if statement == 0:
                    separation = tkinter.Label(self.frames[j-1],bg="#062356", fg="#FFFFFF", text = "|--")
                    separation.pack(side="left")
        # Add button to apply cut at any point in the proof
        self.options.append(tkinter.Button(self.frames[j-1], text=self.formula.inProgress, highlightbackground="#062356", command=lambda x=-1, y=0, z=-1: self.buttonClicked(x, y, z)))
        self.options.append(tkinter.Button(self.frames[j-1], text="Contraction", highlightbackground="#062356", command=lambda x=-2, y=-2, z=-2: self.buttonClicked(x, y, z)))
        self.options[-1].pack(side="right")
        self.frames[j-1].pack(side="top")