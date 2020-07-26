from gramfuzz.fields import *
from random import randrange

'''bc Precedence
https://www.gnu.org/software/bc/manual/html_mono/bc.html
The expression precedence is as follows: (lowest to highest)

|| operator, left associative
&& operator, left associative
! operator, nonassociative
Relational operators, left associative
Assignment operator, right associative
+ and - operators, left associative
*, / and % operators, left associative
^ operator, right associative
unary - operator, nonassociative
++ and -- operators, nonassociative'''


class NRef(Ref):
    cat = "name_def"
class NDef(Def):
    cat = "name_def"

left_number = Join(NRef("left_associative_operator"),NRef("number"), sep=" ")
test = Join(left_number, max=5, sep=" ")

Def("bc_input",
    Join(
        NRef("number"),
        test,
        Opt(NRef("relational_expressions")),
        NRef("number"),
        test,
    sep=" "),
    cat="bc_input"
)
'''class Float(Int):
    """Defines a float ``Field`` with odds that define float
    values
    """
    odds = [
        (0.75,    [-100.0,100.0]),
        (0.05,    0),
        (0.10,    [100.0, 1000.0]),
        (0.10,    [-1000.0, 100.0]),
        (0.10,    [1000.0, 100000.0]),
        (0.10,    [-100000.0, -1000.0]),
    ]'''
NDef("number",Float(value=None))
NDef("left_associative_operator",Or('+','-','*','%','/'))
NDef("right_associative", Or('='))
NDef("relational_expressions",Or('<','<=','>','>=','==','!='))
NDef("boolean_expressions",Or('||','&&'))
