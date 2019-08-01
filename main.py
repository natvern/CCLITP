#    15-112: Principles of Programming and Computer Science
#    Project: Implementing a First-Order logic interactive theorem prover
#    Name      : Samar Rahmouni
#    AndrewID  : srahmoun

#    File Created: 17th November 2018
#    Modification History:
#    Start                End
#    19/11/2018 20:40     21:20
#    20/11/2018 12:54     13:10
#    20/11/2018 16:23     18:20
#    24/11/2018 14:57     17:36
#    05/12/2018 15:23     23:10
#    07/12/2018 15:32     16:32
#    08/12/2018 15:39     21:22
#    08/12/2018 23:10     04:10
#    20/06/2019 14:03           
#    22/06/2019 22:50
#    23/06/2019 14:01
#    25/06/2019 21:12
#    26/06/2019 14:50
#    27/06/2019 17:29
#    01/07/2019 12:57
#    03/07/2019 17:04
#    04/07/2019 18:23
#    07/07/2019 15:00
#    10/07/2019 11:28
#    10/07/2019 15:24
#    11/07/2019 15:52
#    13/07/2019 13:33
#    14/07/2019 13:51
#    21/07/2019 13:10
#    22/07/2019 14:11
#    24/07/2019 13:30
#    25/07/2019 17:50
#    28/07/2019 16:18
#    30/07/2019 20:09
#    01/08/2019 15:00

from engine_v2 import *
from GUI import *
from translation import translate
import tkinter
from calculus import Calculus
from formula import *

# Main function to run CCLITP
def main(statement):
    root = tkinter.Tk()
    root.configure(background="#062356")
    frame = Menu(root, statement)
    root.mainloop()

# Testing input
green = Prop("Green")
red = Prop("Red")
Sideeg = Prop("Sideeg")
Ward = Prop("Ward")
Idiot = Prop("Idiot")
Idiot_1 = Prop("Idiot")


hypothesis = translate("Fayad or Red")
conclusion = translate("Red and Ward")
firstFormula = ([hypothesis], [conclusion])
statement = Theorem(firstFormula)

# Running CCLITP
#print(conclusion)
main(statement)
