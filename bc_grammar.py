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

#arith = arithmetic
#repeating patterns for arithmetic operation
arith = Join(NRef("arithmetic_operator"),NRef("number"), sep=" ")
arith_patterns = Join(arith, max=3, sep=" ")
#adding parenthesis for rithmetic operation
arith_paren = Join("(",NRef("number"),arith_patterns,")", sep=" ")
arith_number_paren = Join(NRef("arithmetic_operator"),Or(arith_paren,NRef("number")), sep=" ")
arith_number_paren_patterns = Join(arith_number_paren, max=5, sep=" ")
#stack to process parenth
Def("bc_input",
    Join(
        Or(arith_paren,NRef("number")),
        arith_number_paren_patterns,
        Opt(Join(NRef("relational_operator"),Or(arith_paren,NRef("number")), sep=" ")),
        arith_number_paren_patterns,
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
NDef("arithmetic_operator",Or('+','-','*','%','/'))
NDef("relational_operator",Or('<','<=','>','>=','==','!='))
NDef("boolean_operator",Or('||','&&'))
NDef("assignment_operators", Or('='))