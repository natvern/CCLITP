# First-Order-Logic-Theorem-Prover
Final Project for 15-112

<h1>I/ Description</h1>
<p>This project is a First-Order logic interactive theorem prover. It is meant to help introduce users to sequent calculus and Gentzen trees. Given a logical statement, the user can click on a compound proposition (clause) to derive a statement that can either be another compound proposition or an atomic formula. The process continues until we reach an axiom, hence proving the truth of the original statement. This means that the program can for example prove that there exists a path between a and c, given a graph a-b-c. The program does not handle quantifiers.</p>

<h1>II/ Librairies & Features</h1>
<p>I  will be using Coq Proof Assistant, and Tkinter. The program uses sequent calculus to prove propositions.</p>

<h1>III/ User Interface</h1>
<p>The user interface will show a Gentzen tree, where you can click on a clause to derive another one. For every step, the inference rule used will be explained. Since the program is meant to introduce the user to sequent calculus and Gentzen trees, it will ease the understanding of such concepts.</p>

<h1>IV/ First Milestone</h1>
<p>Coq Proof Assistant will be translated to Python by then. The program will be able to prove atomic formulas, without GUI.</p>

<h1>V/ Final Submission</h1>
<p>The program will handle compound propositions, show the inference rule with explanation, along with a user-friendly GUI. </p>
