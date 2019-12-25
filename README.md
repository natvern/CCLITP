# CCLITP
Classical and Constructive Logic Interactive Theorem Prover

<h1>I/ Description</h1>
<p>This project is a classical and constructive logic interactive theorem prover. It is meant to help introduce users to sequent calculus and Gentzen trees. Given a logical statement, the user can click on a compound proposition (formula) to derive a statement that can either be another compound proposition or an atomic formula. The process continues until we reach an axiom, hence proving the truth of the original statement. This means that the program can for example prove that there exists a path between a and c, given a graph a-b-c. The program does not handle quantifiers (yet).</p>

<h1>II/ Librairies & Features</h1>
<p>Tkinter used to provide the User Interface. The program uses sequent calculus to prove propositions.</p>

<h1>III/ User Interface</h1>
<p>The user interface will show a Gentzen tree, where you can click on a clause to derive another one. For every step, the inference rule used will be explained. Since the program is meant to introduce the user to sequent calculus and Gentzen trees, it will ease the understanding of such concepts.</p>

<h1>IV/ How</h1>
<p>To prove: "A or not A".<br>
In the main.py file, you can specify the hypothesis and conclusion to:<br>
  <code>hypothesis = translate("A or not A")</code><br> 
  <code>conclusion = translate("")</code><br>
In the global_logic.py, you can specify which logic you would like to use: <code>classical_calculus</code> or <code>constructive calculus</code>. Once this specified, you can run the main.py. Following instructions would depend on the global logic. Since the Prover is interactive, you can click on formulas and apply specific rules on them depending on their connective. (an AND formula would apply the conjunction rule). </p>
  </p>
  
<h1>V/ Internal Implementation</h1>
<p>The project is divided into 5 parts: <br>
  - Engine <br>
  - GUI <br>
  - Calculus (Classical and Constructive) <br>
  - Datatypes: Formulas/Propositions/(Quantifiers) <br>
  - Translation (Parsing) <br> </p>
  <h2> 1. Engine </h2>
  <p>Given a sequent, the engine sets up a Theorem. The Theorem keeps track of the subgoals (sub-sequents) and halts when    no sequents are left (assuming that is only reached if the initial sequent is true). The role of the engine is to get the input of the user (which formula to apply a rule to) and apply that rule to it, given the calculus that is set up.</p>
  <h2> 2. GUI </h2>
  <p> The GUI is handled by Tkinter. It only displays the sequents (with each formula as a button) and gets the input to send it to the engine. The GUI also offers a "help" function and explanation of rules applied.</p>
  <h2> 3. Calculus </h2>
  <p>A calculus is defined by its rules (disjunction, conjunction, implication, cut, contraction, negation) and axioms (indentity, falsehood). Hence, switching between two logics is only a chance of those rules. 
  Rules take as input the initial sequent, the side (hypothesis or conclusion) and the number of the formula (Sequents are represented internally as a list of two lists of formulas). Rules return a list of the new sequents while deleting the old formulas. </p>
  <h2> 4. Datatypes </h2>
  Due to the lack of type, defining new datatypes for CCLITP was done through the use of classes. <br>
  For example, connectives (AND, OR, etc.) have been defining as follows: <br>
  <code> class Conn(Enum):<br>
    AND = 4<br>
    OR = 3<br>
    IMPL = 2<br>
    NOT = 1<br>
    NONE = 0 <br></code><br>
  Formulas are a more complex datatype, that are defined by their connective and their args (list of two sub formulas if OR/AND/IMPL, one sub formula if NOT or NONE or empty if NONE). 
  For our formula class, we defined their equality, and some helpful functions to keep the class as private as possible. 
  Building tiles for formulas are propositions. (A is a proposition, not A is a formula). Falsehood and truthhood are similarly global datatype that use proposiitons to define themselves. </p>
  <h2>5. Translation </h2>
  <p>The translation takes in a string that represent some theorem to prove <code>(A and (B or C)) imply C</code>. It returns a formula <code>Formula(AND, [Prop(A), Formula(OR, [Prop(B), Prop(C)])])</code>. The parsing is inspired by CLAC: using stacks and precedence values to form the subparts. </p>
  
  
  <h1>VI/ Currently</h1> 
 <p>- Quantifiers as a datatype and predicates as extension of propositions.</p>
 <p>- Substitutions as a rule</p>
 <p>- Global Variables and Eigenvariables and variables as a type.</p> 
 
