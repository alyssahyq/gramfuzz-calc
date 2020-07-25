from gramfuzz.fields import *

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

Def("name",
    Join(
        NRef("number"),
        NRef("left_associative_operator"),
        NRef("number"),
    sep=" "),
    cat="name"
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
NDef("left_associative_operator",Or('||','&&','<','<=','>','>=','==','!=','+','-','*','%','/'))
NDef("right_associative", Or('='))
