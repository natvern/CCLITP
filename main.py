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
#    05/12 15:23          05/12 23:10
#    07/12 15:32          07/12 16:32
#    08/12 15:39          08/12 21:22
#    08/12 23:10          09/12 04:10

#    20/06/2019 - 14:03

from engine import *
from GUI import *
import tkinter

# Testing input

A = Clause("Death")
B = Clause("CMU student")
C = Clause("CMU")

firstFormula = ( [ [ [B], [C], "imply"],   [ [C] , [A] , "imply"] ]  , [ [ [B] , [A] , "imply" ]  ]  )
statement = Formula(firstFormula)

root = tkinter.Tk()
root.configure(background="#062356")
frame = Menu(root, statement)
root.mainloop()